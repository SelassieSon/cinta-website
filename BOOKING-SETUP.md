# Booking → Google Calendar — Setup (no n8n)

The Ecosystem Mapping booking on `www/contact.html` posts to a **Google Apps
Script web app** (`apps-script/Code.gs`). That script runs as you, inside your
Google Workspace, and does everything the old n8n workflow did:

```
www/contact.html ──POST──► Apps Script web app (runs as unika@cintaconsulting.com)
                            ├─ Calendar : find a free 90-min slot, create the event + Meet
                            ├─ Sheets   : log the client            (optional)
                            ├─ Drive    : client folder + templates (optional)
                            └─ Gmail    : confirm to the contact, notify you
```

No servers, no n8n, no third party. Free with your Workspace account.

## Deploy the script (about 5 minutes)

1. Go to **script.google.com** → **New project**. Sign in as
   `unika@cintaconsulting.com`.
2. Delete the stub, paste the entire contents of `apps-script/Code.gs`, and save.
3. At the top of the file, the calendar booking already works as-is. Fill the
   optional IDs in `CONFIG` only when you want the extras:
   - `CLIENT_SHEET_ID` — a Google Sheet to log every booking.
   - `CLIENTS_ROOT_FOLDER_ID` — a Drive folder; each client gets a subfolder.
   - `INTAKE_TEMPLATE_ID`, `MAPPING_TEMPLATE_ID` — Drive files copied into it.
   (Each ID is the long string in that file's URL. Leave `''` to skip.)
4. Run the function **`TEST_booking`** once (Run ▶). Google will ask you to
   authorize Calendar, Drive, Sheets, and Gmail access — approve it. Check the
   log; a test event should land on your calendar.
5. **Deploy → New deployment → Web app**:
   - *Execute as*: **Me**
   - *Who has access*: **Anyone**
   - Deploy, then **copy the Web app URL** (ends in `/exec`).

## Point the website at it

- In `_build/common.py`, set `BOOKING_WEBHOOK` to that `/exec` URL.
- Rebuild and deploy:
  `cd _build && python3 build_www.py && cd .. && cp _shared/*.css www/ && ./deploy.sh www`
- Or edit the `WEBHOOK` value directly in the `<script>` at the bottom of
  `www/contact.html`, then `./deploy.sh www`.

Submit a real booking from the live page: a 90-minute event appears on your
calendar, the contact gets a confirmation, and you get an internal notice.

## Google Meet links (optional)

The script attaches a Meet link if the **advanced Calendar service** is on. In the
Apps Script editor: **Services (+)** → add **Calendar API** → save. Without it,
everything still works; the calendar invite just carries no Meet link.

## Why the form is fire-and-forget

A static site and `script.google.com` are different origins, and Apps Script web
apps don't return CORS headers. The form posts with `mode:"no-cors"` and the
default `text/plain` body, which the script reads as `e.postData.contents`. The
page can't read the reply, so it shows the success state optimistically — the
real receipt is the confirmation email the script sends. This is the standard,
reliable pattern for an Apps Script endpoint behind a static form.

## Routing — matches your original design

- **Priority sectors** (Ministry, School Board, Hospital/Health, Municipality,
  Crown Agency) are **auto-booked** into the first free 90-minute slot: event
  created with Meet, Drive provisioned, Sheet logged, confirmation emailed. The
  event is colour-coded red and flagged `[PRIORITY]` in your internal notice.
- **All other sectors** get the **pick-a-slot email**: the script proposes three
  open times (one per day) and asks the lead to reply with their choice — no event
  is created until they pick. You get an internal notice listing the proposed
  times. Logged to the Sheet as `PENDING_SLOT` if the Sheet is configured.
  - Set `SLOT_OPTIONS` in `CONFIG` to change how many times are proposed.
  - If you later add a self-serve booking page (e.g. a Google Calendar appointment
    page), put its URL in `CONFIG.PICK_A_SLOT_URL` and the email links to it
    instead of asking for a reply.
- **Idempotency kept**: a priority domain won't be double-booked within 14 days.
- **Same outcomes as before**: calendar event, Drive folders, Sheet log, Gmail.

## CINTA AI "Book a Demo" is separate

This is the Ecosystem Mapping intake on the main site. The CINTA AI product demo
still uses its Google Form. Want that one on Apps Script too? Easy to add.
