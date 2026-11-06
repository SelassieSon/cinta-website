/**
 * CINTA & Co. — unified booking + lead endpoint (Google Workspace only)
 *
 * One web app serves every property, routed by an `intent` field in the POST:
 *   • intent "ecosystem" (default) — 90-min Ecosystem Mapping (cintaconsulting.com)
 *       Priority sectors auto-book; others get click-to-book time buttons.
 *   • intent "demo"               — 30-min CINTA AI demo (cintaai.cintaconsulting.com)
 *       Everyone gets click-to-book time buttons.
 *   • intent "lead"               — Responsible AI scope request (responsibleai + landers)
 *       No calendar event; acknowledges the contact and emails info@ to follow up.
 *
 * Clicking a time  ─GET→ doGet(action=confirm) → createBooking_ (books + confirms).
 *
 * UPDATE: after pasting changes, Deploy → Manage deployments → edit (pencil) →
 * Version: New version → Deploy. The /exec URL never changes.
 */

var CONFIG = {
  CALENDAR_ID:        'unika@cintaconsulting.com',
  TIMEZONE:           'America/Toronto',
  SESSION_MINUTES:    90,          // ecosystem default
  DEMO_MINUTES:       30,
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
  BOOKING_SECRET:     'cinta-2026-change-me-to-anything-random',

  // Auto company briefing on inbound leads (uses Claude API + web search).
  // The API key is NOT stored here — set Script property ANTHROPIC_API_KEY
  // under Project Settings → Script properties. If no key is set, leads still
  // send normally, just without the briefing.
  COMPANY_BRIEFING:   true,
  BRIEFING_MODEL:     'claude-sonnet-5-5',   // any current API model string
  BRIEFING_TOOL:      'web_search_20250305', // web search server-tool version
  BRIEFING_MAX_USES:  4,
  BRIEFING_CACHE_HRS: 6,                      // reuse a briefing per domain/org

  CLIENT_SHEET_ID:        '',
  CLIENT_SHEET_TAB:       'Clients',
  CLIENTS_ROOT_FOLDER_ID: '',
  INTAKE_TEMPLATE_ID:     '',
  MAPPING_TEMPLATE_ID:    ''
};

var TAG = '[CINTA-BOOKING]';
var RED = '#D04747';

function typeOf_(d) {
  var t = String((d && d.intent) || '').trim().toLowerCase();
  if (t === 'demo') return { key: 'demo', minutes: CONFIG.DEMO_MINUTES, label: 'CINTA AI Demo', priorityRouting: false };
  return { key: 'ecosystem', minutes: CONFIG.SESSION_MINUTES, label: 'Ecosystem Mapping Session', priorityRouting: true };
}
function typeFromKey_(k) { return typeOf_({ intent: (k === 'demo' ? 'demo' : '') }); }

// ─────────────────────────────────────────────────────────── HTTP
function doGet(e) {
  if (e && e.parameter && e.parameter.action === 'confirm')    return handleConfirm_(e);
  if (e && e.parameter && e.parameter.action === 'reschedule') return handleReschedule_(e);
  return json_({ ok: true, service: 'CINTA booking + lead endpoint' });
}
function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); } catch (_) { data = (e.parameter || {}); }
    } else { data = (e && e.parameter) || {}; }
    return json_(handleBooking_(data));
  } catch (err) { notifyFailure_(err, e); return json_({ ok: false, error: String(err) }); }
}

// ─────────────────────────────────────────────────────────── Submit
function handleBooking_(d) {
  var email = String(d.contact_email || '').trim().toLowerCase();
  if (!email || email.indexOf('@') < 0) return { ok: false, error: 'A valid contact_email is required.' };
  d.contact_email = email;
  d.contact_name  = String(d.contact_name || '').trim();
  d.org_name      = String(d.org_name || '').trim();
  d.website       = String(d.website || '').trim();
  d.sector        = String(d.sector || '').trim();
  d.role          = String(d.role || '').trim();
  d.desired_timeframe = String(d.desired_timeframe || '').trim();
  d.service_interest  = String(d.service_interest || '').trim();
  d.segment       = String(d.segment || '').trim();
  d.message       = String(d.message || '').trim();
  d.brand_notes   = String(d.brand_notes || '').trim();
  d.action_plan   = String(d.action_plan || '').trim();
  d.assessment_result = String(d.assessment_result || '').trim();
  d.assessment_score  = String(d.assessment_score || '').trim();
  d.cta_url       = String(d.cta_url || '').trim();
  d.cta_label     = String(d.cta_label || '').trim();
  d.intent        = String(d.intent || '').trim().toLowerCase();

  if (d.intent === 'lead') return handleLead_(d);

  var type = typeOf_(d);
  var persona = derivePersona_(d);
  var priority = (type.priorityRouting && CONFIG.PRIORITY_SECTORS.indexOf(d.sector) >= 0) ? 'PRIORITY' : 'STANDARD';
  var cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID) || CalendarApp.getDefaultCalendar();

  if (priority === 'PRIORITY') {
    var slot = findSlot_(cal, type.minutes);
    if (!slot) { sendNoSlot_(d, type); return { ok: true, status: 'no_slot_emailed' }; }
    return createBooking_(cal, d, persona, priority, slot.start, type);
  }
  var options = findSlots_(cal, CONFIG.SLOT_OPTIONS, type.minutes);
  if (!options.length) { sendNoSlot_(d, type); return { ok: true, status: 'no_slot_emailed' }; }
  sendPickLinks_(d, options, type);
  if (CONFIG.CLIENT_SHEET_ID) {
    try { logClient_('C-' + domainOf_(email) + '-' + today_(), d, persona, priority, null, 'PENDING_PICK'); }
    catch (err) { notifyFailure_('Sheet log failed: ' + err, null); }
  }
  return { ok: true, status: 'pick_links_sent', type: type.key,
           options: options.map(function (s) { return s.start.toISOString(); }) };
}

// ─────────────────────────────────────────────────────────── Lead (no calendar)
function handleLead_(d) {
  if (CONFIG.CLIENT_SHEET_ID) {
    try { logClient_('L-' + domainOf_(d.contact_email) + '-' + today_(), d, derivePersona_(d), 'LEAD', null, 'LEAD'); }
    catch (err) { notifyFailure_('Sheet log failed: ' + err, null); }
  }
  var isAssessment = !!d.action_plan || /assessment/i.test(d.service_interest);
  if (isAssessment) { sendActionPlan_(d); }
  else {
    var about = d.service_interest ? ('your interest in ' + d.service_interest) : 'your Responsible AI enquiry';
    GmailApp.sendEmail(d.contact_email, 'We received your request — CoCr8 x CINTA Responsible AI',
      'Hi ' + (d.contact_name || 'there') + ',\n\n' +
      'Thank you for reaching out about ' + about + '. A member of the CoCr8 x CINTA Responsible AI team ' +
      'will be in touch within one business day to scope next steps.\n\n' +
      'CoCr8 Labs x CINTA & Co.\nResponsible AI',
      { name: 'CoCr8 x CINTA — Responsible AI', replyTo: CONFIG.REPLY_TO });
  }
  if (CONFIG.NOTIFY_EMAIL) {
    var tag = isAssessment ? '[ASSESSMENT LEAD]' : '[RAI LEAD]';
    var brief = enrichCompany_(d);
    var briefBlock = '';
    if (brief) {
      briefBlock = '\n────────────  COMPANY BRIEFING (auto-researched)  ────────────\n' + brief;
    } else if (CONFIG.COMPANY_BRIEFING) {
      briefBlock = '\n────────────  COMPANY BRIEFING  ────────────\n' +
        '(Not available: no business domain on the email, or research was skipped. ' +
        'See setup if this is unexpected.)';
    }
    GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL,
      tag + ' ' + (d.org_name || d.contact_email) + (d.service_interest ? ' — ' + d.service_interest : ''),
      ['New lead from ' + (d.service_interest || 'Responsible AI'), '',
       '──────────────  PROSPECT SNAPSHOT  ──────────────',
       'Organization: ' + (d.org_name || '(not given)'),
       'Contact: ' + (d.contact_name || '(not given)') + ' <' + d.contact_email + '>',
       (companyDomain_(d.contact_email) ? 'Company domain: ' + companyDomain_(d.contact_email) : ''),
       'Website: ' + (d.website || '(not given)'),
       'Sector: ' + (d.sector || '(not given)'), 'Role: ' + (d.role || '(not given)'),
       (d.segment ? 'Segment: ' + d.segment : ''), '',
       '──────────────  ASSESSMENT  ──────────────',
       'Service: ' + (d.service_interest || '(general)'),
       (d.assessment_result ? 'Result: ' + d.assessment_result + (d.assessment_score ? ' (score ' + d.assessment_score + ')' : '') : ''),
       '',
       (d.action_plan ? 'Action plan sent to prospect:\n' + d.action_plan : 'Message:\n' + (d.message || '(none)')),
       (d.brand_notes ? '\nBrand guidelines: ' + d.brand_notes : ''),
       briefBlock]
       .filter(function (x) { return x !== ''; }).join('\n'),
      { name: 'CINTA Booking Bot' });
  }
  return { ok: true, status: isAssessment ? 'action_plan_sent' : 'lead_received' };
}

function sendActionPlan_(d) {
  var svc = d.service_interest || 'AI Readiness Assessment';
  var result = d.assessment_result || '';
  var score = d.assessment_score || '';
  var plan = d.action_plan || '';
  var ctaLabel = (d.cta_label || '').replace(/^Or\s+/i, '').trim();
  if (ctaLabel) ctaLabel = ctaLabel.charAt(0).toUpperCase() + ctaLabel.slice(1);
  // Plain text
  var plain = ['Hi ' + (d.contact_name || 'there') + ',', '',
    'Here is your ' + svc + ' result and action plan.', '',
    'Your result: ' + result + (score ? ' (score ' + score + ')' : ''), '',
    plan, '',
    (d.cta_url ? (ctaLabel || 'Take the next step') + ': ' + d.cta_url : ''),
    'A member of our team will also follow up within one business day.', '',
    'CINTA & Co. — Facilitating Success', 'Toronto, Ontario'
  ].filter(function (x) { return x !== ''; }).join('\n');
  // HTML: turn the plan's "- " lines into a list, other lines into paragraphs
  var lines = plan.split('\n'), html = '', inList = false;
  for (var i = 0; i < lines.length; i++) {
    var l = lines[i].trim();
    if (!l) continue;
    if (l.indexOf('- ') === 0) {
      if (!inList) { html += '<ul style="padding-left:18px;margin:10px 0">'; inList = true; }
      html += '<li style="margin:6px 0">' + esc_(l.slice(2)) + '</li>';
    } else {
      if (inList) { html += '</ul>'; inList = false; }
      html += '<p style="margin:10px 0">' + esc_(l) + '</p>';
    }
  }
  if (inList) html += '</ul>';
  var body = '<div style="font-family:Arial,sans-serif;font-size:15px;color:#222;line-height:1.6;max-width:560px">' +
    '<p>Hi ' + esc_(d.contact_name || 'there') + ',</p>' +
    '<p>Here is your <strong>' + esc_(svc) + '</strong> result and action plan.</p>' +
    '<div style="background:#F4F4F2;border-left:4px solid ' + RED + ';padding:14px 18px;border-radius:4px;margin:16px 0">' +
    '<div style="font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#944026">Your result</div>' +
    '<div style="font-size:18px;font-weight:700;margin-top:4px">' + esc_(result) + (score ? ' <span style="font-weight:400;color:#666;font-size:14px">(score ' + esc_(score) + ')</span>' : '') + '</div></div>' +
    '<div style="font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#944026;margin-top:18px">Your action plan</div>' +
    html +
    (d.cta_url ? '<p style="margin:22px 0 6px"><a href="' + d.cta_url + '" style="display:inline-block;background:' + RED +
       ';color:#fff;text-decoration:none;font-weight:600;padding:12px 22px;border-radius:4px">' + esc_(ctaLabel || 'Take the next step') + '</a></p>' : '') +
    '<p style="color:#666;font-size:13px">A member of our team will also follow up within one business day.</p>' +
    '<p style="margin-top:22px">CINTA &amp; Co. — Facilitating Success<br>Toronto, Ontario</p></div>';
  GmailApp.sendEmail(d.contact_email, 'Your ' + svc + ' results and action plan — CINTA & Co.',
    plain, { htmlBody: body, name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}

// ─────────────────────────────────────────────── Company briefing (web research)

// Return the business domain of an email, or '' for free webmail / missing.
function companyDomain_(email) {
  var dom = (String(email || '').split('@')[1] || '').toLowerCase().trim();
  if (!dom) return '';
  var free = ['gmail.com','googlemail.com','outlook.com','hotmail.com','live.com',
    'yahoo.com','yahoo.ca','ymail.com','icloud.com','me.com','mac.com','aol.com',
    'proton.me','protonmail.com','gmx.com','msn.com','pm.me','mail.com','hey.com'];
  return free.indexOf(dom) === -1 ? dom : '';
}

// Ask Claude (with web search) for a short internal briefing on the lead's company.
// Returns plain text, or '' if disabled, no key, nothing to research, or on error.
function enrichCompany_(d) {
  if (!CONFIG.COMPANY_BRIEFING) return '';
  var key = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
  if (!key) return '';
  var org = String(d.org_name || '').trim();
  var domain = companyDomain_(d.contact_email);
  if (!org && !domain) return '';   // nothing identifiable (e.g. gmail with no org)

  var cache = CacheService.getScriptCache();
  var ck = 'brief:' + (domain || org).toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 200);
  var hit = cache.get(ck);
  if (hit) return hit;

  var who = org && domain ? ('"' + org + '" (email domain ' + domain + ')')
          : org ? ('"' + org + '"') : ('the organization at the domain ' + domain);
  var prompt =
    'You are briefing a boutique consulting firm on an inbound lead. Research ' + who +
    ' using web search and write a concise internal briefing, under 180 words, plain text, no markdown headings or bullets characters. ' +
    'Cover only what you can actually verify: what the organization is and does; its sector; approximate size (employees) and HQ/location; ' +
    'anything notable or recent (leadership, funding, initiatives) that is relevant to a conversation; and one closing line on where an AI, ' +
    'strategy, and transformation consultancy could plausibly help them. ' +
    'If you cannot confidently identify the organization, say that in one line instead of guessing. Never invent facts, names, or numbers.';

  var payload = {
    model: CONFIG.BRIEFING_MODEL,
    max_tokens: 800,
    tools: [{ type: CONFIG.BRIEFING_TOOL, name: 'web_search', max_uses: CONFIG.BRIEFING_MAX_USES }],
    messages: [{ role: 'user', content: prompt }]
  };

  try {
    var res = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
      method: 'post',
      contentType: 'application/json',
      headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01' },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
    var code = res.getResponseCode();
    if (code !== 200) {
      notifyFailure_('Company briefing API ' + code + ': ' + res.getContentText().slice(0, 400), null);
      return '';
    }
    var data = JSON.parse(res.getContentText());
    var text = (data.content || [])
      .filter(function (b) { return b.type === 'text'; })
      .map(function (b) { return b.text; }).join('\n').trim();
    if (text) cache.put(ck, text, Math.round(CONFIG.BRIEFING_CACHE_HRS * 3600));
    return text;
  } catch (err) {
    notifyFailure_('Company briefing fetch failed: ' + err, null);
    return '';
  }
}

// ─────────────────────────────────────────────────────────── Click-to-book
function handleConfirm_(e) {
  try {
    var p = e.parameter;
    var email = String(p.e || '').trim().toLowerCase();
    var startIso = String(p.t || ''), ty = String(p.ty || '');
    if (!email || !startIso) return htmlPage_('Something went wrong', 'That booking link is incomplete. Please use the buttons in your email.');
    if (sign_(email + '|' + startIso + '|' + ty) !== String(p.sig || '')) {
      return htmlPage_('Link expired', 'That booking link is no longer valid. Reply to your email and we will help you book.');
    }
    var d = { contact_email: email, contact_name: p.n || '', org_name: p.o || '', website: p.w || '',
              sector: p.s || '', role: p.r || '', service_interest: p.si || '', segment: p.sg || '', desired_timeframe: '' };
    var type = typeFromKey_(ty);
    var persona = derivePersona_(d);
    var priority = (type.priorityRouting && CONFIG.PRIORITY_SECTORS.indexOf(d.sector) >= 0) ? 'PRIORITY' : 'STANDARD';
    var cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID) || CalendarApp.getDefaultCalendar();
    var res = createBooking_(cal, d, persona, priority, new Date(startIso), type);
    var when = res.event_start ? fmt_(new Date(res.event_start)) : '';
    if (res.status === 'already_booked') {
      return htmlPage_('You are already booked', 'You already have a ' + type.label + ' scheduled for <b>' + when + '</b>. A calendar invite is in your inbox.');
    }
    return htmlPage_('You are booked', 'Your ' + type.minutes + '-minute ' + type.label + ' is confirmed for <b>' + when + '</b>. A calendar invite and confirmation email are on their way.');
  } catch (err) {
    notifyFailure_(err, e);
    return htmlPage_('Something went wrong', 'We could not complete that booking. Please reply to your email and we will sort it out.');
  }
}

// ─────────────────────────────────────────────────────────── Reschedule
function handleReschedule_(e) {
  try {
    var p = e.parameter;
    var email = String(p.e || '').trim().toLowerCase();
    var ty = String(p.ty || '');
    if (!email) return htmlPage_('Something went wrong', 'That link is incomplete. Please reply to your email and we will help you find a new time.');
    if (sign_(email + '|reschedule|' + ty) !== String(p.sig || '')) {
      return htmlPage_('Link expired', 'That reschedule link is no longer valid. Reply to your email and we will find a new time with you.');
    }
    var type = typeFromKey_(ty);
    var cal = CalendarApp.getCalendarById(CONFIG.CALENDAR_ID) || CalendarApp.getDefaultCalendar();
    // Release the existing booking so the slot frees up and nothing is left stuck.
    var existing = findExistingBooking_(cal, domainOf_(email), type.key);
    if (existing) { try { existing.deleteEvent(); } catch (_) {} }
    var d = { contact_email: email, contact_name: p.n || '', org_name: p.o || '', website: p.w || '',
              sector: p.s || '', role: p.r || '', service_interest: p.si || '', segment: p.sg || '' };
    var options = findSlots_(cal, CONFIG.SLOT_OPTIONS, type.minutes);
    if (!options.length) {
      sendNoSlot_(d, type);
      return htmlPage_('We will be in touch', 'Your original time has been released. Our calendar is tight over the next couple of weeks, so we have emailed you to lock in a new time.');
    }
    var btns = options.map(function (s) {
      var url = confirmUrl_(d, s.start.toISOString(), type);
      return '<a href="' + url + '" style="display:inline-block;width:100%;box-sizing:border-box;text-align:center;' +
why_btn_() + '">' + fmt_(s.start) + '</a>';
    }).join('');
    return htmlPage_('Pick a new time',
      'Your original time has been released. Choose one that works and you are booked, just click it:<br><br>' +
      btns + '<br><span style="font-size:13px;color:#888">None of these work? Reply to your email and we will find one that does.</span>');
  } catch (err) {
    notifyFailure_(err, e);
    return htmlPage_('Something went wrong', 'We could not reschedule that. Please reply to your email and we will sort it out.');
  }
}
function why_btn_() {
  return 'background:' + RED + ';color:#fff;text-decoration:none;font-weight:600;padding:14px 20px;border-radius:4px;margin:6px 0;font-size:16px';
}

// ─────────────────────────────────────────────────────────── Booking
function createBooking_(cal, d, persona, priority, start, type) {
  var domain = domainOf_(d.contact_email);
  var existing = findExistingBooking_(cal, domain, type.key);
  if (existing) {
    sendConfirmation_(d, existing.getStartTime(), getMeetLink_(existing), true, '', type);
    return { ok: true, status: 'already_booked', event_start: existing.getStartTime().toISOString() };
  }
  var end = new Date(start.getTime() + type.minutes * 60000);
  if (cal.getEvents(start, end).length > 0) {
    var slot = findSlot_(cal, type.minutes);
    if (!slot) { sendNoSlot_(d, type); return { ok: true, status: 'no_slot_emailed' }; }
    start = slot.start; end = slot.end;
  }
  var extra = d.service_interest || d.segment || '';
  var title = (d.org_name ? d.org_name + ' — ' : '') + CONFIG.ORG_LABEL + ' ' + type.label;
  var desc = TAG + ' domain=' + domain + ' type=' + type.key + '\n\n' +
      type.label + ' (' + type.minutes + ' min)\n' +
      'Organization: ' + d.org_name + '\nWebsite: ' + d.website + '\n' +
      (d.sector ? 'Sector: ' + d.sector + '  (' + priority + ')\n' : '') +
      (extra ? 'Focus: ' + extra + '\n' : '') +
      'Contact: ' + d.contact_name + ' <' + d.contact_email + '>\n' +
      'Role: ' + d.role + '\nPersona: ' + persona + '\n';
  var event = cal.createEvent(title, start, end, { description: desc, guests: d.contact_email, sendInvites: true });
  try { event.setColor(priority === 'PRIORITY' ? CalendarApp.EventColor.RED : CalendarApp.EventColor.BLUE); } catch (_) {}
  var meet = CONFIG.ADD_MEET ? tryAddMeet_(event) : '';

  if (CONFIG.CLIENT_SHEET_ID) {
    try { logClient_('C-' + domain + '-' + today_(), d, persona, priority, start, event.getId()); }
    catch (err) { notifyFailure_('Sheet log failed: ' + err, null); }
  }
  var folderUrl = '';
  if (CONFIG.CLIENTS_ROOT_FOLDER_ID && type.key === 'ecosystem') {
    try { folderUrl = provisionDrive_(d.org_name || domain); }
    catch (err) { notifyFailure_('Drive provisioning failed: ' + err, null); }
  }
  sendConfirmation_(d, start, meet, false, folderUrl, type);
  notifyInternal_(d, priority, start, meet, folderUrl, type);
  return { ok: true, status: 'booked', type: type.key, priority: priority,
           event_id: event.getId(), event_start: start.toISOString(), meet: meet, folder: folderUrl };
}

// ─────────────────────────────────────────────────────────── Slots
function findSlot_(cal, minutes) {
  minutes = minutes || CONFIG.SESSION_MINUTES;
  var now = new Date(), startDay = new Date(now.getTime() + 864e5);
  for (var o = 0; o < CONFIG.SEARCH_DAYS; o++) {
    var day = new Date(startDay.getTime() + o * 864e5), dow = day.getDay();
    if (CONFIG.SKIP_WEEKENDS && (dow === 0 || dow === 6)) continue;
    for (var h = CONFIG.DAY_START_HOUR * 60; h <= CONFIG.DAY_END_HOUR * 60; h += CONFIG.SLOT_STEP_MINUTES) {
      var start = new Date(day.getFullYear(), day.getMonth(), day.getDate(), Math.floor(h / 60), h % 60, 0);
      if (start <= now) continue;
      var end = new Date(start.getTime() + minutes * 60000);
      if (cal.getEvents(start, end).length === 0) return { start: start, end: end };
    }
  }
  return null;
}
function findSlots_(cal, n, minutes) {
  minutes = minutes || CONFIG.SESSION_MINUTES;
  var out = [], now = new Date(), startDay = new Date(now.getTime() + 864e5);
  for (var o = 0; o < CONFIG.SEARCH_DAYS && out.length < n; o++) {
    var day = new Date(startDay.getTime() + o * 864e5), dow = day.getDay();
    if (CONFIG.SKIP_WEEKENDS && (dow === 0 || dow === 6)) continue;
    for (var h = CONFIG.DAY_START_HOUR * 60; h <= CONFIG.DAY_END_HOUR * 60; h += CONFIG.SLOT_STEP_MINUTES) {
      var start = new Date(day.getFullYear(), day.getMonth(), day.getDate(), Math.floor(h / 60), h % 60, 0);
      if (start <= now) continue;
      var end = new Date(start.getTime() + minutes * 60000);
      if (cal.getEvents(start, end).length === 0) { out.push({ start: start, end: end }); break; }
    }
  }
  return out;
}
function findExistingBooking_(cal, domain, typeKey) {
  var now = new Date(), until = new Date(now.getTime() + CONFIG.SEARCH_DAYS * 864e5);
  var ev = cal.getEvents(now, until);
  for (var i = 0; i < ev.length; i++) {
    var desc = ev[i].getDescription() || '';
    if (desc.indexOf(TAG) >= 0 && desc.indexOf('domain=' + domain) >= 0 &&
        (!typeKey || desc.indexOf('type=' + typeKey) >= 0)) return ev[i];
  }
  return null;
}

// ─────────────────────────────────────────────────────────── Helpers
function derivePersona_(d) {
  var persona = String(d.persona || '').trim(); if (persona) return persona;
  var r = String(d.role || '').toLowerCase();
  if (r.indexOf('privacy') >= 0 || r.indexOf('ciso') >= 0) return 'Risk-First';
  if (r.indexOf('ops') >= 0 || r.indexOf('transform') >= 0) return 'ROI-First';
  return 'Unsure';
}
function domainOf_(email) { return (email.split('@')[1] || '').replace(/[^a-z0-9]+/g, '-'); }
function today_() { return Utilities.formatDate(new Date(), CONFIG.TIMEZONE, 'yyyyMMdd'); }
function sign_(s) {
  return Utilities.computeHmacSha256Signature(s, CONFIG.BOOKING_SECRET)
    .map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('');
}
function confirmUrl_(d, startIso, type) {
  var base = ScriptApp.getService().getUrl();
  var q = { action: 'confirm', e: d.contact_email, n: d.contact_name, o: d.org_name, w: d.website,
            s: d.sector, r: d.role, si: d.service_interest || '', sg: d.segment || '',
            ty: type.key, t: startIso, sig: sign_(d.contact_email + '|' + startIso + '|' + type.key) };
  return base + '?' + Object.keys(q).map(function (k) {
    return encodeURIComponent(k) + '=' + encodeURIComponent(q[k]); }).join('&');
}
function rescheduleUrl_(d, type) {
  var base = ScriptApp.getService().getUrl();
  var q = { action: 'reschedule', e: d.contact_email, n: d.contact_name, o: d.org_name, w: d.website,
            s: d.sector, r: d.role, si: d.service_interest || '', sg: d.segment || '',
            ty: type.key, sig: sign_(d.contact_email + '|reschedule|' + type.key) };
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
    sh.appendRow(['client_id','created_at','intent','org_name','website','sector','priority',
                  'contact_name','contact_email','role','persona','service_interest','segment',
                  'desired_timeframe','message','session_start','event_id']);
  }
  var s = start ? Utilities.formatDate(start, CONFIG.TIMEZONE, 'yyyy-MM-dd HH:mm') : '';
  sh.appendRow([clientId, new Date(), d.intent||'', d.org_name||'', d.website||'', d.sector||'', priority,
                d.contact_name||'', d.contact_email||'', d.role||'', persona, d.service_interest||'',
                d.segment||'', d.desired_timeframe||'', d.message||'', s, eventId]);
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
function sendPickLinks_(d, slots, type) {
  var btns = slots.map(function (s) {
    var url = confirmUrl_(d, s.start.toISOString(), type);
    return '<tr><td style="padding:6px 0"><a href="' + url + '" style="display:inline-block;background:' + RED +
      ';color:#fff;text-decoration:none;font-family:Arial,sans-serif;font-size:15px;font-weight:600;padding:13px 22px;border-radius:4px">' +
      fmt_(s.start) + '</a></td></tr>';
  }).join('');
  var html = '<div style="font-family:Arial,sans-serif;font-size:15px;color:#222;line-height:1.6;max-width:520px">' +
    '<p>Hi ' + esc_(d.contact_name || 'there') + ',</p>' +
    '<p>Thank you for requesting a ' + type.minutes + '-minute ' + type.label + '. Pick a time that works and you are booked, just click it:</p>' +
    '<table role="presentation" cellpadding="0" cellspacing="0">' + btns + '</table>' +
    '<p style="color:#666;font-size:13px">None of these work? Just reply to this email and we will find one that does.</p>' +
    '<p style="margin-top:22px">CINTA &amp; Co. — Facilitating Success<br>Toronto, Ontario</p></div>';
  var plain = 'Hi ' + (d.contact_name || 'there') + ',\n\nPick a time for your ' + type.label +
    ' by opening this email where the buttons show, or reply with your preferred time:\n\n' +
    slots.map(function (s) { return '• ' + fmt_(s.start); }).join('\n') + '\n\nCINTA & Co.';
  GmailApp.sendEmail(d.contact_email, 'Pick a time for your ' + type.label + ' — CINTA & Co.',
    plain, { htmlBody: html, name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}
function sendConfirmation_(d, start, meet, already, folderUrl, type) {
  var subj = (already ? 'Your ' + type.label + ' with CINTA & Co.' : 'Confirmed: your ' + type.label + ' with CINTA & Co.');
  var rurl = rescheduleUrl_(d, type);
  var plain = ['Hi ' + (d.contact_name || 'there') + ',', '',
     (already ? 'You already have a ' + type.label + ' booked. Details again:'
              : 'Your ' + type.minutes + '-minute ' + type.label + ' is confirmed.'), '',
     'When: ' + fmt_(start),
     (meet ? 'Join: ' + meet : 'A calendar invitation is on its way.'),
     (folderUrl ? 'Your intake folder: ' + folderUrl : ''), '',
     'If this time does not work, pick a different one here (it releases this slot): ' + rurl, '',
     'CINTA & Co. — Facilitating Success', 'Toronto, Ontario'
    ].filter(function (x) { return x !== ''; }).join('\n');
  var html = '<div style="font-family:Arial,sans-serif;font-size:15px;color:#222;line-height:1.6;max-width:520px">' +
     '<p>Hi ' + esc_(d.contact_name || 'there') + ',</p>' +
     '<p>' + (already ? 'You already have a ' + esc_(type.label) + ' booked. Details again:'
                      : 'Your ' + type.minutes + '-minute ' + esc_(type.label) + ' is confirmed.') + '</p>' +
     '<p><strong>When:</strong> ' + fmt_(start) + '<br>' +
       (meet ? '<strong>Join:</strong> <a href="' + meet + '">' + meet + '</a>' : 'A calendar invitation is on its way.') + '</p>' +
     (folderUrl ? '<p>Your intake folder: <a href="' + folderUrl + '">' + folderUrl + '</a></p>' : '') +
     '<p style="margin:22px 0 8px">Need a different time?</p>' +
     '<p style="margin:0"><a href="' + rurl + '" style="display:inline-block;background:' + RED +
       ';color:#fff;text-decoration:none;font-weight:600;padding:12px 22px;border-radius:4px">Pick a different time</a></p>' +
     '<p style="color:#666;font-size:13px;margin-top:8px">That releases this slot and lets you choose a new one, no reply needed.</p>' +
     '<p style="margin-top:22px">CINTA &amp; Co. — Facilitating Success<br>Toronto, Ontario</p></div>';
  GmailApp.sendEmail(d.contact_email, subj, plain,
    { htmlBody: html, name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}
function sendNoSlot_(d, type) {
  GmailApp.sendEmail(d.contact_email, 'Let us find a time — ' + type.label + ', CINTA & Co.',
    'Hi ' + (d.contact_name || 'there') + ',\n\nThank you for requesting a ' + type.label + '. ' +
    'Our calendar is tight over the next couple of weeks, so reply with a day or two that suit you and ' +
    'we will lock in your session.\n\nCINTA & Co. — Facilitating Success',
    { name: 'CINTA & Co.', replyTo: CONFIG.REPLY_TO });
}
function notifyInternal_(d, priority, start, meet, folderUrl, type) {
  if (!CONFIG.NOTIFY_EMAIL) return;
  var extra = d.service_interest || d.segment || '';
  GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL,
    '[' + type.label + '] ' + (d.org_name || d.contact_email) + ' — ' + fmt_(start),
    ['New ' + type.label + ' booked.', '',
     'Organization: ' + d.org_name, 'Contact: ' + d.contact_name + ' <' + d.contact_email + '>',
     (d.sector ? 'Sector: ' + d.sector + ' (' + priority + ')' : ''),
     (extra ? 'Focus: ' + extra : ''), 'When: ' + fmt_(start),
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
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function htmlPage_(title, msg) {
  var html = '<!doctype html><html><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<title>' + esc_(title) + ' — CINTA & Co.</title></head>' +
    '<body style="margin:0;font-family:Arial,Helvetica,sans-serif;background:#F4F4F2;color:#111">' +
    '<div style="max-width:560px;margin:60px auto;background:#fff;border:1px solid #E6E6E6;border-radius:8px;overflow:hidden">' +
    '<div style="height:6px;background:' + RED + '"></div><div style="padding:40px">' +
    '<div style="font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#944026;margin-bottom:10px">CINTA &amp; Co.</div>' +
    '<h1 style="font-size:26px;margin:0 0 14px">' + esc_(title) + '</h1>' +
    '<p style="font-size:16px;line-height:1.6;color:#333;margin:0">' + msg + '</p>' +
    '<p style="font-size:13px;color:#888;margin-top:28px">Facilitating Success · Toronto, Ontario</p>' +
    '</div></div></body></html>';
  return HtmlService.createHtmlOutput(html).setTitle(title + ' — CINTA & Co.');
}

/** Run once from the editor to authorize + smoke-test all three intents. */
function TEST_booking() {
  Logger.log('ECOSYSTEM/STANDARD → ' + JSON.stringify(handleBooking_({ contact_name:'Test Std', contact_email:'test@std-example.org',
    org_name:'Std Org', sector:'Education', role:'Director of Operations' }), null, 2));
  Logger.log('ECOSYSTEM/PRIORITY → ' + JSON.stringify(handleBooking_({ contact_name:'Test Pri', contact_email:'test@pri-example.org',
    org_name:'Pri Org', sector:'School Board', role:'Superintendent' }), null, 2));
  Logger.log('DEMO → ' + JSON.stringify(handleBooking_({ intent:'demo', contact_name:'Test Demo', contact_email:'test@demo-example.org',
    org_name:'Demo Org', segment:'B2B SaaS' }), null, 2));
  Logger.log('LEAD → ' + JSON.stringify(handleBooking_({ intent:'lead', contact_name:'Test Lead', contact_email:'test@lead-example.org',
    org_name:'Lead Org', service_interest:'Algorithm Impact Assessment', message:'We need an AIA for a hiring tool.' }), null, 2));
}
