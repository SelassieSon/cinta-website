/**
 * CINTA & Co. — Ecosystem Mapping booking endpoint (Google Workspace only)
 *
 * Website form  ─POST→  doPost → handleBooking_
 *   • Priority sectors  → auto-booked into the first free 90-min slot
 *   • Other sectors     → emailed clickable time buttons; clicking one books it
 *
 * Clicking a time  ─GET→  doGet(action=confirm) → createBooking_
 *   The script creates the Calendar event, (optional) Drive + Sheet, emails
 *   confirmation, and shows a branded "you're booked" page. Fully automatic.
 *
 * DEPLOY / UPDATE: after pasting changes, Deploy → Manage deployments → edit
 * (pencil) → Version: New version → Deploy. The /exec URL stays the same.
 */

var CONFIG = {
  CALENDAR_ID:        'unika@cintaconsulting.com', // or 'primary'
  TIMEZONE:           'America/Toronto',
  SESSION_MINUTES:    90,
  SEARCH_DAYS:        14,
  DAY_START_HOUR:     9,
  DAY_END_HOUR:       16,
  SLOT_STEP_MINUTES:  30,
  SKIP_WEEKENDS:      true,
  ADD_MEET:           true,
  ORG_LABEL:          'CoCr8 x CINTA',
  PRIORITY_SECTORS:   ['Ministry','School Board','Hospital/Health','Municipality','Crown Agency'],
  SLOT_OPTIONS:       3,

  NOTIFY_EMAIL:       'info@cintaconsulting.com',
  REPLY_TO:           'info@cintaconsulting.com',

  // Signs the click-to-book links so they can't be forged. Change once to any
  // random string; changing it invalidates links already emailed.
  BOOKING_SECRET:     'cinta-2026-change-me-to-anything-random',

  // Optional — paste IDs to enable, leave '' to skip
  CLIENT_SHEET_ID:        '',
  CLIENT_SHEET_TAB:       'Clients',
  CLIENTS_ROOT_FOLDER_ID: '',
  INTAKE_TEMPLATE_ID:     '',
  MAPPING_TEMPLATE_ID:    ''
};

var TAG = '[CINTA-BOOKING]';
var RED = '#D04747';

// ─────────────────────────────────────────────────────────── HTTP entry points
function doGet(e) {
  if (e && e.parameter && e.parameter.action === 'confirm') {
    return handleConfirm_(e);
  }
  return json_({ ok: true, service: 'CINTA Ecosystem Mapping booking' });
}

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); } catch (_) { data = (e.parameter || {}); }
    } else { data = (e && e.parameter) || {}; }
    return json_(handleBooking_(data));
  } catch (err) {
    notifyFailure_(err, e);
    return json_({ ok: false, error: String(err) });
  }
}

// ─────────────────────────────────────────────────────────── Submit handler
function handleBooking_(d) {
  var contactEmail = String(d.contact_email || '').trim().toLowerCase();
  if (!contactEmail || contactEmail.indexOf('@') < 0) {
    return { ok: false, error: 'A valid contact_email is required.' };
  }
  d.contact_email = contactEmail;
  d.contact_name  = String(d.contact_name || '').trim();
  d.org_name      = String(d.org_name || '').trim();
  d.website       = String(d.website || '').trim();
  d.sector        = String(d.sector || '').trim();
  d.role          = String(d.role || '').trim();
  d.desired_timeframe = String(d.desired_timeframe || '').trim();
  d.service_interest  = String(d.service_interest || '').trim();

  var persona = derivePersona_(d);
  var priority = CONFIG.PRIORITY_SECTORS.indexOf(d.sector) >= 0 ? 'PRIORITY' : 'STANDARD';
  var cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID) || CalendarApp.getDefaultCalendar();

  if (priority === 'PRIORITY') {
    var slot = findSlot_(cal);
    if (!slot) { sendNoSlot_(d); return { ok: true, status: 'no_slot_emailed' }; }
    return createBooking_(cal, d, persona, priority, slot.start);
  }

  // Non-priority → clickable time options
  var options = findSlots_(cal, CONFIG.SLOT_OPTIONS);
  if (!options.length) { sendNoSlot_(d); return { ok: true, status: 'no_slot_emailed' }; }
  sendPickLinks_(d, options);
  if (CONFIG.CLIENT_SHEET_ID) {
    try {
      logClient_('C-' + domainOf_(contactEmail) + '-' + today_(), d, persona, priority, null, 'PENDING_PICK');
    } catch (err) { notifyFailure_('Sheet log failed: ' + err, null); }
  }
  return { ok: true, status: 'pick_links_sent',
           options: options.map(function (s) { return s.start.toISOString(); }) };
}

// ─────────────────────────────────────────────────────────── Click-to-book (GET)
function handleConfirm_(e) {
  try {
    var p = e.parameter;
    var email = String(p.e || '').trim().toLowerCase();
    var startIso = String(p.t || '');
    if (!email || !startIso) return htmlPage_('Something went wrong', 'That booking link is incomplete. Please use the buttons in your email.');
    if (sign_(email + '|' + startIso) !== String(p.sig || '')) {
      return htmlPage_('Link expired', 'That booking link is no longer valid. Reply to your email and we will help you book.');
    }
    var d = { contact_email: email, contact_name: p.n || '', org_name: p.o || '',
              website: p.w || '', sector: p.s || '', role: p.r || '', desired_timeframe: '',
              service_interest: p.si || '' };
    var persona = derivePersona_(d);
    var priority = CONFIG.PRIORITY_SECTORS.indexOf(d.sector) >= 0 ? 'PRIORITY' : 'STANDARD';
    var cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID) || CalendarApp.getDefaultCalendar();
    var start = new Date(startIso);
    var res = createBooking_(cal, d, persona, priority, start);
    var when = res.event_start ? fmt_(new Date(res.event_start)) : '';
    if (res.status === 'already_booked') {
      return htmlPage_('You are already booked', 'You already have an Ecosystem Mapping Session scheduled for <b>' + when + '</b>. We look forward to it. A calendar invite is in your inbox.');
    }
    return htmlPage_('You are booked', 'Your 90-minute Ecosystem Mapping Session is confirmed for <b>' + when + '</b>. A calendar invite and confirmation email are on their way. See you then.');
  } catch (err) {
    notifyFailure_(err, e);
    return htmlPage_('Something went wrong', 'We could not complete that booking. Please reply to your email and we will sort it out.');
  }
}

// ─────────────────────────────────────────────────────────── Shared booking
function createBooking_(cal, d, persona, priority, start) {
  var domain = domainOf_(d.contact_email);

  var existing = findExistingBooking_(cal, domain);
  if (existing) {
    sendConfirmation_(d, existing.getStartTime(), getMeetLink_(existing), true, '');
    return { ok: true, status: 'already_booked', event_start: existing.getStartTime().toISOString() };
  }

  var end = new Date(start.getTime() + CONFIG.SESSION_MINUTES * 60000);
  if (cal.getEvents(start, end).length > 0) {        // slot taken since the email
    var slot = findSlot_(cal);
    if (!slot) { sendNoSlot_(d); return { ok: true, status: 'no_slot_emailed' }; }
    start = slot.start; end = slot.end;
  }

  var title = d.org_name ? (d.org_name + ' — ' + CONFIG.ORG_LABEL + ' Ecosystem Mapping')
                         : (CONFIG.ORG_LABEL + ' Ecosystem Mapping Session');
  var desc = TAG + ' domain=' + domain + '\n\n' +
      'Ecosystem Mapping Session (90 min)\n' +
      'Organization: ' + d.org_name + '\nWebsite: ' + d.website + '\n' +
      'Sector: ' + d.sector + '  (' + priority + ')\n' +
      (d.service_interest ? 'Service of interest: ' + d.service_interest + '\n' : '') +
      'Contact: ' + d.contact_name + ' <' + d.contact_email + '>\n' +
      'Role: ' + d.role + '\nPersona: ' + persona + '\n';

  var event = cal.createEvent(title, start, end,
      { description: desc, guests: d.contact_email, sendInvites: true });
  try { event.setColor(priority === 'PRIORITY' ? CalendarApp.EventColor.RED : CalendarApp.EventColor.BLUE); } catch (_) {}
  var meet = CONFIG.ADD_MEET ? tryAddMeet_(event) : '';

  if (CONFIG.CLIENT_SHEET_ID) {
    try { logClient_('C-' + domain + '-' + today_(), d, persona, priority, start, event.getId()); }
    catch (err) { notifyFailure_('Sheet log failed: ' + err, null); }
  }
  var folderUrl = '';
  if (CONFIG.CLIENTS_ROOT_FOLDER_ID) {
    try { folderUrl = provisionDrive_(d.org_name || domain); }
    catch (err) { notifyFailure_('Drive provisioning failed: ' + err, null); }
  }

  sendConfirmation_(d, start, meet, false, folderUrl);
  notifyInternal_(d, priority, start, meet, folderUrl);
  return { ok: true, status: 'booked', priority: priority,
           event_id: event.getId(), event_start: start.toISOString(), meet: meet, folder: folderUrl };
}

// ─────────────────────────────────────────────────────────── Helpers
function derivePersona_(d) {
  var persona = String(d.persona || '').trim();
  if (persona) return persona;
  var r = String(d.role || '').toLowerCase();
  if (r.indexOf('privacy') >= 0 || r.indexOf('ciso') >= 0) return 'Risk-First';
  if (r.indexOf('ops') >= 0 || r.indexOf('transform') >= 0) return 'ROI-First';
  return 'Unsure';
}
function domainOf_(email) { return (email.split('@')[1] || '').replace(/[^a-z0-9]+/g, '-'); }
function today_() { return Utilities.formatDate(new Date(), CONFIG.TIMEZONE, 'yyyyMMdd'); }

function findSlot_(cal) {
  var now = new Date(), startDay = new Date(now.getTime() + 864e5);
  for (var o = 0; o < CONFIG.SEARCH_DAYS; o++) {
    var day = new Date(startDay.getTime() + o * 864e5), dow = day.getDay();
    if (CONFIG.SKIP_WEEKENDS && (dow === 0 || dow === 6)) continue;
    for (var h = CONFIG.DAY_START_HOUR * 60; h <= CONFIG.DAY_END_HOUR * 60; h += CONFIG.SLOT_STEP_MINUTES) {
      var start = new Date(day.getFullYear(), day.getMonth(), day.getDate(), Math.floor(h / 60), h % 60, 0);
      if (start <= now) continue;
      var end = new Date(start.getTime() + CONFIG.SESSION_MINUTES * 60000);
      if (cal.getEvents(start, end).length === 0) return { start: start, end: end };
    }
  }
  return null;
}
function findSlots_(cal, n) {
  var out = [], now = new Date(), startDay = new Date(now.getTime() + 864e5);
  for (var o = 0; o < CONFIG.SEARCH_DAYS && out.length < n; o++) {
    var day = new Date(startDay.getTime() + o * 864e5), dow = day.getDay();
    if (CONFIG.SKIP_WEEKENDS && (dow === 0 || dow === 6)) continue;
    for (var h = CONFIG.DAY_START_HOUR * 60; h <= CONFIG.DAY_END_HOUR * 60; h += CONFIG.SLOT_STEP_MINUTES) {
      var start = new Date(day.getFullYear(), day.getMonth(), day.getDate(), Math.floor(h / 60), h % 60, 0);
      if (start <= now) continue;
      var end = new Date(start.getTime() + CONFIG.SESSION_MINUTES * 60000);
      if (cal.getEvents(start, end).length === 0) { out.push({ start: start, end: end }); break; }
    }
  }
  return out;
}
function findExistingBooking_(cal, domain) {
  var now = new Date(), until = new Date(now.getTime() + CONFIG.SEARCH_DAYS * 864e5);
  var ev = cal.getEvents(now, until);
  for (var i = 0; i < ev.length; i++) {
    var desc = ev[i].getDescription() || '';
    if (desc.indexOf(TAG) >= 0 && desc.indexOf('domain=' + domain) >= 0) return ev[i];
  }
  return null;
}

function sign_(s) {
  var raw = Utilities.computeHmacSha256Signature(s, CONFIG.BOOKING_SECRET);
  return raw.map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('');
}
function confirmUrl_(d, startIso) {
  var base = ScriptApp.getService().getUrl();
  var q = { action: 'confirm', e: d.contact_email, n: d.contact_name, o: d.org_name,
            w: d.website, s: d.sector, r: d.role, si: d.service_interest || '', t: startIso,
            sig: sign_(d.contact_email + '|' + startIso) };
  return base + '?' + Object.keys(q).map(function (k) {
    return encodeURIComponent(k) + '=' + encodeURIComponent(q[k]); }).join('&');
}

function tryAddMeet_(event) {
  try {
    if (typeof Calendar === 'undefined' || !Calendar.Events) return '';
    var id = event.getId().split('@')[0];
    var patched = Calendar.Events.patch(
      { conferenceData: { createRequest: { requestId: Utilities.getUuid(),
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

function logClient_(clientId, d, persona, priority, start, eventId) {
  var ss = SpreadsheetApp.openById(CONFIG.CLIENT_SHEET_ID);
  var sh = ss.getSheetByName(CONFIG.CLIENT_SHEET_TAB) || ss.insertSheet(CONFIG.CLIENT_SHEET_TAB);
  if (sh.getLastRow() === 0) {
    sh.appendRow(['client_id','created_at','org_name','website','sector','priority',
                  'contact_name','contact_email','role','persona','desired_timeframe',
                  'session_start','event_id']);
  }
  var s = start ? Utilities.formatDate(start, CONFIG.TIMEZONE, 'yyyy-MM-dd HH:mm') : '';
  sh.appendRow([clientId, new Date(), d.org_name||'', d.website||'', d.sector||'', priority,
                d.contact_name||'', d.contact_email||'', d.role||'', persona,
                d.desired_timeframe||'', s, eventId]);
}
function provisionDrive_(name) {
  var root = DriveApp.getFolderById(CONFIG.CLIENTS_ROOT_FOLDER_ID);
  var folder = root.createFolder(name + ' — ' + CONFIG.ORG_LABEL + ' ' +
                 Utilities.formatDate(new Date(), CONFIG.TIMEZONE, 'yyyy-MM-dd'));
  ['01 Intake','02 Ecosystem Map','03 Deliverables'].forEach(function (n) { folder.createFolder(n); });
  if (CONFIG.INTAKE_TEMPLATE_ID)  DriveApp.getFileById(CONFIG.INTAKE_TEMPLATE_ID).makeCopy('Intake Questions — ' + name, folder);
  if (CONFIG.MAPPING_TEMPLATE_ID) DriveApp.getFileById(CONFIG.MAPPING_TEMPLATE_ID).makeCopy('Ecosystem Map — ' + name, folder);
  return folder.getUrl();
}

// ─────────────────────────────────────────────────────────── Email
function fmt_(dt) { return Utilities.formatDate(dt, CONFIG.TIMEZONE, "EEEE, MMMM d 'at' h:mm a") + ' (ET)'; }

function sendPickLinks_(d, slots) {
  var btns = slots.map(function (s) {
    var url = confirmUrl_(d, s.start.toISOString());
    return '<tr><td style="padding:6px 0"><a href="' + url + '" ' +
      'style="display:inline-block;background:' + RED + ';color:#fff;text-decoration:none;' +
      'font-family:Arial,sans-serif;font-size:15px;font-weight:600;padding:13px 22px;border-radius:4px">' +
      fmt_(s.start) + '</a></td></tr>';
  }).join('');
  var html =
    '<div style="font-family:Arial,sans-serif;font-size:15px;color:#222;line-height:1.6;max-width:520px">' +
    '<p>Hi ' + esc_(d.contact_name || 'there') + ',</p>' +
    '<p>Thank you for requesting a 90-minute Ecosystem Mapping Session. Pick a time that works and you are booked, just click it:</p>' +
    '<table role="presentation" cellpadding="0" cellspacing="0">' + btns + '</table>' +
    '<p style="color:#666;font-size:13px">None of these work? Just reply to this email and we will find one that does.</p>' +
    '<p style="margin-top:22px">CINTA &amp; Co. — Facilitating Success<br>Toronto, Ontario</p></div>';
  var plain = 'Hi ' + (d.contact_name || 'there') + ',\n\nPick a time for your Ecosystem Mapping Session by opening this email in a browser that shows the buttons, or reply with your preferred time:\n\n' +
    slots.map(function (s) { return '• ' + fmt_(s.start); }).join('\n') + '\n\nCINTA & Co.';
  GmailApp.sendEmail(d.contact_email, 'Pick a time for your Ecosystem Mapping Session — CINTA & Co.',
    plain, { htmlBody: html, name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}

function sendConfirmation_(d, start, meet, already, folderUrl) {
  var subj = (already ? 'Your Ecosystem Mapping Session with CINTA & Co.'
                      : 'Confirmed: your Ecosystem Mapping Session with CINTA & Co.');
  var lines = [
    'Hi ' + (d.contact_name || 'there') + ',', '',
    (already ? 'You already have an Ecosystem Mapping Session booked. Details again:'
             : 'Your 90-minute Ecosystem Mapping Session is confirmed.'), '',
    'When: ' + fmt_(start),
    (meet ? 'Join: ' + meet : 'A calendar invitation is on its way.'),
    (folderUrl ? 'Your intake folder: ' + folderUrl : ''), '',
    'If this time does not work, just reply and we will adjust it.', '',
    'CINTA & Co. — Facilitating Success', 'Toronto, Ontario'
  ].filter(function (x) { return x !== ''; });
  GmailApp.sendEmail(d.contact_email, subj, lines.join('\n'),
    { name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}

function sendNoSlot_(d) {
  GmailApp.sendEmail(d.contact_email, 'Let us find a time — Ecosystem Mapping Session, CINTA & Co.',
    'Hi ' + (d.contact_name || 'there') + ',\n\nThank you for requesting an Ecosystem Mapping Session. ' +
    'Our calendar is tight over the next couple of weeks, so reply with a day or two that suit you and ' +
    'we will lock in your 90-minute session.\n\nCINTA & Co. — Facilitating Success',
    { name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}

function notifyInternal_(d, priority, start, meet, folderUrl) {
  if (!CONFIG.NOTIFY_EMAIL) return;
  GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL,
    '[' + priority + '] Booked: ' + (d.org_name || d.contact_email) + ' — ' + fmt_(start),
    ['New Ecosystem Mapping Session booked.', '',
     'Organization: ' + d.org_name, 'Contact: ' + d.contact_name + ' <' + d.contact_email + '>',
     'Sector: ' + d.sector + ' (' + priority + ')',
     (d.service_interest ? 'Service of interest: ' + d.service_interest : ''),
     'When: ' + fmt_(start),
     (meet ? 'Meet: ' + meet : ''), (folderUrl ? 'Folder: ' + folderUrl : '')
    ].filter(String).join('\n'), { name: 'CINTA Booking Bot' });
}
function notifyFailure_(err, e) {
  try {
    if (!CONFIG.NOTIFY_EMAIL) return;
    GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL, 'CINTA booking — error',
      String(err) + '\n\nPayload:\n' + (e && e.postData ? e.postData.contents : '(none)'),
      { name: 'CINTA Booking Bot' });
  } catch (_) {}
}

// ─────────────────────────────────────────────────────────── Output
function esc_(s) { return String(s).replace(/[<>&"]/g, function (c) {
  return { '<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;' }[c]; }); }
function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
function htmlPage_(title, msg) {
  var html =
    '<!doctype html><html><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<title>' + esc_(title) + ' — CINTA & Co.</title></head>' +
    '<body style="margin:0;font-family:Arial,Helvetica,sans-serif;background:#F4F4F2;color:#111">' +
    '<div style="max-width:560px;margin:60px auto;background:#fff;border:1px solid #E6E6E6;border-radius:8px;overflow:hidden">' +
    '<div style="height:6px;background:' + RED + '"></div>' +
    '<div style="padding:40px">' +
    '<div style="font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#944026;margin-bottom:10px">CINTA &amp; Co.</div>' +
    '<h1 style="font-size:26px;margin:0 0 14px">' + esc_(title) + '</h1>' +
    '<p style="font-size:16px;line-height:1.6;color:#333;margin:0">' + msg + '</p>' +
    '<p style="font-size:13px;color:#888;margin-top:28px">Facilitating Success · Toronto, Ontario</p>' +
    '</div></div></body></html>';
  return HtmlService.createHtmlOutput(html).setTitle(title + ' — CINTA & Co.');
}

/** Run once from the editor to authorize + smoke-test both paths. */
function TEST_booking() {
  var standard = handleBooking_({ contact_name: 'Test Standard', contact_email: 'test@standard-example.org',
    org_name: 'Standard Test Org', website: 'https://example.org', sector: 'Education',
    role: 'Director of Operations', desired_timeframe: 'This week' });
  Logger.log('STANDARD → ' + JSON.stringify(standard, null, 2));
  var priority = handleBooking_({ contact_name: 'Test Priority', contact_email: 'test@priority-example.org',
    org_name: 'Priority Test Org', website: 'https://example.org', sector: 'School Board',
    role: 'Superintendent', desired_timeframe: 'This week' });
  Logger.log('PRIORITY → ' + JSON.stringify(priority, null, 2));
}
