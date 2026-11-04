/**
 * CINTA & Co. — Ecosystem Mapping booking endpoint
 * Replaces the n8n "Workflow A v3" using only Google Workspace services.
 *
 * On a website booking it will:
 *   1. Normalize the submission and derive persona + priority tier
 *   2. Prevent a same-domain double-booking within the next 14 days (idempotency)
 *   3. Find the first free 90-minute slot on your calendar (business hours)
 *   4. Create the Calendar event (with Google Meet) and invite the contact
 *   5. (optional) Log the client to a Google Sheet
 *   6. (optional) Create the client's Drive folder and copy your templates
 *   7. Email the contact a confirmation, and notify you internally
 *
 * DEPLOY:  Extensions/▶ script.google.com → paste this → Deploy → New deployment
 *          → Web app → Execute as: Me → Who has access: Anyone → copy the /exec URL.
 *          Paste that URL into the website (BOOKING_WEBHOOK). Full steps in
 *          BOOKING-SETUP.md.
 */

// ─────────────────────────────────────────────────────────────────────────────
// CONFIG — fill the optional IDs when ready; the calendar booking works without
// them. Leave an ID blank ('') to skip that step.
// ─────────────────────────────────────────────────────────────────────────────
var CONFIG = {
  CALENDAR_ID:        'unika@cintaconsulting.com', // or 'primary'
  TIMEZONE:           'America/Toronto',
  SESSION_MINUTES:    90,
  SEARCH_DAYS:        14,          // how far ahead to look for a slot
  DAY_START_HOUR:     9,           // earliest start (local)
  DAY_END_HOUR:       16,          // latest start (so a 90-min ends by ~17:30)
  SLOT_STEP_MINUTES:  30,          // granularity when scanning for free time
  SKIP_WEEKENDS:      true,
  ADD_MEET:           true,
  ORG_LABEL:          'CoCr8 x CINTA',
  PRIORITY_SECTORS:   ['Ministry','School Board','Hospital/Health','Municipality','Crown Agency'],

  // Routing: PRIORITY sectors are auto-booked into the first free slot.
  // Everyone else gets a "pick a slot" email with proposed times (no event yet).
  SLOT_OPTIONS:       3,           // how many times to propose to non-priority leads
  PICK_A_SLOT_URL:    '',          // optional self-serve booking page (e.g. a Google
                                   // Calendar appointment page). Blank = reply-to-choose.

  NOTIFY_EMAIL:       'info@cintaconsulting.com', // internal copy + failure alerts
  REPLY_TO:           'info@cintaconsulting.com',

  // Optional — paste IDs to enable, leave '' to skip ───────────────────────────
  CLIENT_SHEET_ID:        '',   // a Google Sheet ID for the client log
  CLIENT_SHEET_TAB:       'Clients',
  CLIENTS_ROOT_FOLDER_ID: '',   // a Drive folder ID; each client gets a subfolder
  INTAKE_TEMPLATE_ID:     '',   // Drive file ID to copy into the client folder
  MAPPING_TEMPLATE_ID:    ''    // Drive file ID to copy into the client folder
};

var TAG = '[CINTA-BOOKING]'; // marker written into event descriptions for idempotency

// ─────────────────────────────────────────────────────────────────────────────
// HTTP entry points
// ─────────────────────────────────────────────────────────────────────────────
function doGet() {
  return json_({ ok: true, service: 'CINTA Ecosystem Mapping booking' });
}

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); }
      catch (_) { data = (e.parameter || {}); }   // fallback: form-encoded
    } else {
      data = (e && e.parameter) || {};
    }
    var result = handleBooking_(data);
    return json_(result);
  } catch (err) {
    notifyFailure_(err, e);
    return json_({ ok: false, error: String(err) });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Core
// ─────────────────────────────────────────────────────────────────────────────
function handleBooking_(d) {
  var contactName  = String(d.contact_name  || '').trim();
  var contactEmail = String(d.contact_email || '').trim().toLowerCase();
  var orgName      = String(d.org_name      || '').trim();
  var website      = String(d.website       || '').trim();
  var sector       = String(d.sector        || '').trim();
  var role         = String(d.role          || '').trim();
  var timeframe    = String(d.desired_timeframe || '').trim();

  if (!contactEmail || contactEmail.indexOf('@') < 0) {
    return { ok: false, error: 'A valid contact_email is required.' };
  }
  var domain = contactEmail.split('@')[1] || '';

  // persona (derive from role when not supplied), mirrors the n8n logic
  var persona = String(d.persona || '').trim();
  if (!persona) {
    var r = role.toLowerCase();
    if (r.indexOf('privacy') >= 0 || r.indexOf('ciso') >= 0) persona = 'Risk-First';
    else if (r.indexOf('ops') >= 0 || r.indexOf('transform') >= 0) persona = 'ROI-First';
    else persona = 'Unsure';
  }
  var priority = CONFIG.PRIORITY_SECTORS.indexOf(sector) >= 0 ? 'PRIORITY' : 'STANDARD';

  var cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID) || CalendarApp.getDefaultCalendar();

  // ── NON-PRIORITY ROUTING ──────────────────────────────────────────────
  // Standard sectors are not auto-booked. We propose times and let them choose,
  // mirroring the original pick-a-slot path. No calendar event is created yet.
  if (priority !== 'PRIORITY') {
    var options = findSlots_(cal, CONFIG.SLOT_OPTIONS);
    if (!options.length) {
      sendNoSlot_(contactName, contactEmail, orgName);
    } else {
      sendPickASlot_(contactName, contactEmail, orgName, options);
    }
    if (CONFIG.CLIENT_SHEET_ID) {
      try {
        var cid = 'C-' + domain.replace(/[^a-z0-9]+/g, '-') + '-' +
                  Utilities.formatDate(new Date(), CONFIG.TIMEZONE, 'yyyyMMdd');
        logClient_(cid, d, persona, priority, null, 'PENDING_SLOT');
      } catch (err) { notifyFailure_('Sheet log failed: ' + err, null); }
    }
    notifyInternalPending_(orgName, contactName, contactEmail, sector, options);
    return { ok: true, status: 'pick_a_slot_sent', priority: priority,
             options: options.map(function (s) { return s.start.toISOString(); }) };
  }

  // ── PRIORITY ROUTING (auto-book) ──────────────────────────────────────
  // 1) Idempotency — already a CINTA booking for this domain in the window?
  var existing = findExistingBooking_(cal, domain);
  if (existing) {
    sendConfirmation_(contactName, contactEmail, orgName, existing.getStartTime(),
                      getMeetLink_(existing), true);
    return { ok: true, status: 'already_booked',
             event_start: existing.getStartTime().toISOString() };
  }

  // 2) Find the first free 90-minute slot
  var slot = findSlot_(cal);
  if (!slot) {
    // No slot found — email the contact a "reply to schedule" note, still succeed.
    sendNoSlot_(contactName, contactEmail, orgName);
    return { ok: true, status: 'no_slot_emailed' };
  }

  // 3) Create the event
  var title = orgName ? (orgName + ' — ' + CONFIG.ORG_LABEL + ' Ecosystem Mapping')
                      : (CONFIG.ORG_LABEL + ' Ecosystem Mapping Session');
  var desc =
      TAG + ' domain=' + domain + '\n\n' +
      'Ecosystem Mapping Session (90 min)\n' +
      'Organization: ' + orgName + '\n' +
      'Website: ' + website + '\n' +
      'Sector: ' + sector + '  (' + priority + ')\n' +
      'Contact: ' + contactName + ' <' + contactEmail + '>\n' +
      'Role: ' + role + '\n' +
      'Persona: ' + persona + '\n' +
      'Preferred timing: ' + timeframe + '\n';

  var opts = { description: desc, guests: contactEmail, sendInvites: true };
  var event = cal.createEvent(title, slot.start, slot.end, opts);
  try { event.setColor(priority === 'PRIORITY' ? CalendarApp.EventColor.RED
                                               : CalendarApp.EventColor.BLUE); } catch (_) {}

  // Google Meet link (best-effort; requires the Calendar advanced service if you
  // want a guaranteed Meet link — see BOOKING-SETUP.md).
  var meet = CONFIG.ADD_MEET ? tryAddMeet_(event) : '';

  // 4) Optional: client sheet log
  var clientId = 'C-' + domain.replace(/[^a-z0-9]+/g, '-') + '-' +
                 Utilities.formatDate(new Date(), CONFIG.TIMEZONE, 'yyyyMMdd');
  if (CONFIG.CLIENT_SHEET_ID) {
    try { logClient_(clientId, d, persona, priority, slot.start, event.getId()); }
    catch (err) { notifyFailure_('Sheet log failed: ' + err, null); }
  }

  // 5) Optional: Drive provisioning
  var folderUrl = '';
  if (CONFIG.CLIENTS_ROOT_FOLDER_ID) {
    try { folderUrl = provisionDrive_(orgName || domain); }
    catch (err) { notifyFailure_('Drive provisioning failed: ' + err, null); }
  }

  // 6) Confirmation + internal notice
  sendConfirmation_(contactName, contactEmail, orgName, slot.start, meet, false, folderUrl);
  notifyInternal_(orgName, contactName, contactEmail, sector, priority, slot.start, meet, folderUrl);

  return {
    ok: true, status: 'booked', priority: priority,
    event_id: event.getId(), event_start: slot.start.toISOString(),
    meet: meet, folder: folderUrl
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// Slot finding + idempotency
// ─────────────────────────────────────────────────────────────────────────────
function findSlot_(cal) {
  var now = new Date();
  var startDay = new Date(now.getTime() + 24 * 3600 * 1000); // from tomorrow
  for (var dayOffset = 0; dayOffset < CONFIG.SEARCH_DAYS; dayOffset++) {
    var day = new Date(startDay.getTime() + dayOffset * 24 * 3600 * 1000);
    var dow = day.getDay();
    if (CONFIG.SKIP_WEEKENDS && (dow === 0 || dow === 6)) continue;

    for (var h = CONFIG.DAY_START_HOUR * 60; h <= CONFIG.DAY_END_HOUR * 60;
         h += CONFIG.SLOT_STEP_MINUTES) {
      var start = new Date(day.getFullYear(), day.getMonth(), day.getDate(),
                           Math.floor(h / 60), h % 60, 0);
      if (start <= now) continue;
      var end = new Date(start.getTime() + CONFIG.SESSION_MINUTES * 60 * 1000);
      var busy = cal.getEvents(start, end);
      if (busy.length === 0) return { start: start, end: end };
    }
  }
  return null;
}

// Collect up to n free slots, at most one per day, for the pick-a-slot email.
function findSlots_(cal, n) {
  var out = [];
  var now = new Date();
  var startDay = new Date(now.getTime() + 24 * 3600 * 1000);
  for (var dayOffset = 0; dayOffset < CONFIG.SEARCH_DAYS && out.length < n; dayOffset++) {
    var day = new Date(startDay.getTime() + dayOffset * 24 * 3600 * 1000);
    var dow = day.getDay();
    if (CONFIG.SKIP_WEEKENDS && (dow === 0 || dow === 6)) continue;
    for (var h = CONFIG.DAY_START_HOUR * 60; h <= CONFIG.DAY_END_HOUR * 60;
         h += CONFIG.SLOT_STEP_MINUTES) {
      var start = new Date(day.getFullYear(), day.getMonth(), day.getDate(),
                           Math.floor(h / 60), h % 60, 0);
      if (start <= now) continue;
      var end = new Date(start.getTime() + CONFIG.SESSION_MINUTES * 60 * 1000);
      if (cal.getEvents(start, end).length === 0) {
        out.push({ start: start, end: end });
        break; // one per day, then move on
      }
    }
  }
  return out;
}

function findExistingBooking_(cal, domain) {
  var now = new Date();
  var until = new Date(now.getTime() + CONFIG.SEARCH_DAYS * 24 * 3600 * 1000);
  var events = cal.getEvents(now, until);
  for (var i = 0; i < events.length; i++) {
    var desc = events[i].getDescription() || '';
    if (desc.indexOf(TAG) >= 0 && desc.indexOf('domain=' + domain) >= 0) {
      return events[i];
    }
  }
  return null;
}

// ─────────────────────────────────────────────────────────────────────────────
// Google Meet (best-effort via advanced Calendar service if enabled)
// ─────────────────────────────────────────────────────────────────────────────
function tryAddMeet_(event) {
  try {
    if (typeof Calendar === 'undefined' || !Calendar.Events) return '';
    var id = event.getId().split('@')[0];
    var patched = Calendar.Events.patch(
      { conferenceData: { createRequest: {
          requestId: Utilities.getUuid(),
          conferenceSolutionKey: { type: 'hangoutsMeet' } } } },
      CONFIG.CALENDAR_ID, id, { conferenceDataVersion: 1 });
    return (patched && patched.hangoutLink) ? patched.hangoutLink : '';
  } catch (_) { return ''; }
}
function getMeetLink_(event) {
  try {
    if (typeof Calendar === 'undefined' || !Calendar.Events) return '';
    var ev = Calendar.Events.get(CONFIG.CALENDAR_ID, event.getId().split('@')[0]);
    return (ev && ev.hangoutLink) ? ev.hangoutLink : '';
  } catch (_) { return ''; }
}

// ─────────────────────────────────────────────────────────────────────────────
// Sheet + Drive (optional)
// ─────────────────────────────────────────────────────────────────────────────
function logClient_(clientId, d, persona, priority, start, eventId) {
  var ss = SpreadsheetApp.openById(CONFIG.CLIENT_SHEET_ID);
  var sh = ss.getSheetByName(CONFIG.CLIENT_SHEET_TAB) || ss.insertSheet(CONFIG.CLIENT_SHEET_TAB);
  if (sh.getLastRow() === 0) {
    sh.appendRow(['client_id','created_at','org_name','website','sector','priority',
                  'contact_name','contact_email','role','persona',
                  'desired_timeframe','session_start','event_id']);
  }
  var startStr = start ? Utilities.formatDate(start, CONFIG.TIMEZONE, 'yyyy-MM-dd HH:mm') : '';
  sh.appendRow([clientId, new Date(), d.org_name||'', d.website||'', d.sector||'',
                priority, d.contact_name||'', d.contact_email||'', d.role||'',
                persona, d.desired_timeframe||'', startStr, eventId]);
}

function provisionDrive_(name) {
  var root = DriveApp.getFolderById(CONFIG.CLIENTS_ROOT_FOLDER_ID);
  var folder = root.createFolder(name + ' — ' + CONFIG.ORG_LABEL + ' ' +
                 Utilities.formatDate(new Date(), CONFIG.TIMEZONE, 'yyyy-MM-dd'));
  ['01 Intake','02 Ecosystem Map','03 Deliverables'].forEach(function (n) {
    folder.createFolder(n);
  });
  if (CONFIG.INTAKE_TEMPLATE_ID) {
    DriveApp.getFileById(CONFIG.INTAKE_TEMPLATE_ID)
      .makeCopy('Intake Questions — ' + name, folder);
  }
  if (CONFIG.MAPPING_TEMPLATE_ID) {
    DriveApp.getFileById(CONFIG.MAPPING_TEMPLATE_ID)
      .makeCopy('Ecosystem Map — ' + name, folder);
  }
  return folder.getUrl();
}

// ─────────────────────────────────────────────────────────────────────────────
// Email
// ─────────────────────────────────────────────────────────────────────────────
function fmt_(dt) {
  return Utilities.formatDate(dt, CONFIG.TIMEZONE, "EEEE, MMMM d 'at' h:mm a") + ' (ET)';
}

function sendConfirmation_(name, email, org, start, meet, already, folderUrl) {
  var subj = already
    ? 'Your Ecosystem Mapping Session with CINTA & Co.'
    : 'Confirmed: your Ecosystem Mapping Session with CINTA & Co.';
  var lines = [
    'Hi ' + (name || 'there') + ',',
    '',
    (already ? 'You already have an Ecosystem Mapping Session booked. Here are the details again:'
             : 'Your 90-minute Ecosystem Mapping Session is confirmed.'),
    '',
    'When: ' + fmt_(start),
    (meet ? 'Join: ' + meet : 'A calendar invitation is on its way.'),
    (folderUrl ? 'Your intake folder: ' + folderUrl : ''),
    '',
    'If this time does not work, just reply and we will adjust it.',
    '',
    'CINTA & Co. — Facilitating Success',
    'Toronto, Ontario'
  ].filter(function (x) { return x !== null; });
  GmailApp.sendEmail(email, subj, lines.join('\n'),
    { name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}

function sendPickASlot_(name, email, org, slots) {
  var subj = 'Pick a time for your Ecosystem Mapping Session — CINTA & Co.';
  var opts = slots.map(function (s, i) { return '  ' + (i + 1) + '. ' + fmt_(s.start); });
  var choose = CONFIG.PICK_A_SLOT_URL
    ? ('Choose your time here: ' + CONFIG.PICK_A_SLOT_URL)
    : 'Just reply with the number that works and we will confirm it right away.';
  var body = [
    'Hi ' + (name || 'there') + ',',
    '',
    'Thank you for requesting a 90-minute Ecosystem Mapping Session. Here are a few ' +
    'times that are open:',
    '',
    opts.join('\n'),
    '',
    choose,
    '',
    'If none of these suit you, reply with a day or two that do and we will make it work.',
    '',
    'CINTA & Co. — Facilitating Success',
    'Toronto, Ontario'
  ].join('\n');
  GmailApp.sendEmail(email, subj, body, { name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}

function notifyInternalPending_(org, name, email, sector, slots) {
  if (!CONFIG.NOTIFY_EMAIL) return;
  var when = slots.length
    ? slots.map(function (s) { return '• ' + fmt_(s.start); }).join('\n')
    : '(no open slots found — a reply-to-schedule note was sent)';
  var body = [
    'Non-priority lead sent the pick-a-slot email.', '',
    'Organization: ' + org, 'Contact: ' + name + ' <' + email + '>',
    'Sector: ' + sector + ' (STANDARD)', '', 'Proposed times:', when, '',
    'Once they choose, book it on the calendar as usual.'
  ].join('\n');
  GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL, 'New lead (pick-a-slot): ' + (org || email),
    body, { name: 'CINTA Booking Bot' });
}

function sendNoSlot_(name, email, org) {
  var subj = 'Let us find a time — Ecosystem Mapping Session, CINTA & Co.';
  var body = 'Hi ' + (name || 'there') + ',\n\n' +
    'Thank you for requesting an Ecosystem Mapping Session. Our calendar is tight ' +
    'over the next couple of weeks, so reply with a day or two that suit you and we ' +
    'will lock in your 90-minute session.\n\n' +
    'CINTA & Co. — Facilitating Success';
  GmailApp.sendEmail(email, subj, body, { name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}

function notifyInternal_(org, name, email, sector, priority, start, meet, folderUrl) {
  if (!CONFIG.NOTIFY_EMAIL) return;
  var subj = '[' + priority + '] New booking: ' + (org || email) + ' — ' + fmt_(start);
  var body = [
    'New Ecosystem Mapping Session booked.', '',
    'Organization: ' + org, 'Contact: ' + name + ' <' + email + '>',
    'Sector: ' + sector + ' (' + priority + ')', 'When: ' + fmt_(start),
    (meet ? 'Meet: ' + meet : ''), (folderUrl ? 'Folder: ' + folderUrl : '')
  ].filter(String).join('\n');
  GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL, subj, body, { name: 'CINTA Booking Bot' });
}

function notifyFailure_(err, e) {
  try {
    if (!CONFIG.NOTIFY_EMAIL) return;
    GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL,
      'CINTA booking — error', String(err) +
      '\n\nPayload:\n' + (e && e.postData ? e.postData.contents : '(none)'),
      { name: 'CINTA Booking Bot' });
  } catch (_) {}
}

// ─────────────────────────────────────────────────────────────────────────────
function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/** Run once from the editor to grant permissions and smoke-test both paths. */
function TEST_booking() {
  // STANDARD sector → pick-a-slot email, no event created
  var standard = handleBooking_({
    contact_name: 'Test Standard', contact_email: 'test@standard-example.org',
    org_name: 'Standard Test Org', website: 'https://example.org',
    sector: 'Education', role: 'Director of Operations',
    desired_timeframe: 'This week'
  });
  Logger.log('STANDARD → ' + JSON.stringify(standard, null, 2));

  // PRIORITY sector → auto-booked event
  var priority = handleBooking_({
    contact_name: 'Test Priority', contact_email: 'test@priority-example.org',
    org_name: 'Priority Test Org', website: 'https://example.org',
    sector: 'School Board', role: 'Superintendent',
    desired_timeframe: 'This week'
  });
  Logger.log('PRIORITY → ' + JSON.stringify(priority, null, 2));
}
