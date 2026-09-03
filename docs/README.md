# Team 4 - Day 9 Feature Enhancement Activity

This repository contains our work for the Day 9 Hypothesise and Enhance
activity on the django-helpdesk codebase.

## Team
- Team 4
- Members: Manoj. C, Meghana. S, Aseem

## Selected enhancements (Appendix A)
- **Enhancement 1 - A.2 Waiting for Customer**: a new ticket status so agents
  can mark tickets that are blocked waiting for information from the customer.
- **Enhancement 2 - A.1 Transfer a ticket to another queue**: a dedicated
  Transfer action on the ticket detail page so moving a ticket between queues
  is no longer buried inside the general Edit form.

## Git tags
- `enhancement-1-complete` - the commit in which Enhancement 1 is fully
  implemented and validated.
- `enhancement-2-complete` - the commit in which Enhancement 2 is also fully
  implemented and validated. This tag contains both enhancements.

## How to run the demo
The project can be run from the `student_demo/` directory:

```bash
cd student_demo
python3 -m venv venv
source venv/bin/activate
pip install -e ..
python manage.py migrate
python manage.py load_demo
python manage.py runserver
```

Classroom accounts (loaded by `load_demo`):
- Customer: `maya` / `demo123`
- Customer: `rahul` / `demo123`
- Support agent: `anita` / `demo123`
- Support agent: `vikram` / `demo123`
- Support manager: `manager` / `demo123`

## How to run the tests
```bash
python -m django test tests.test_team4_enhancements --settings=tests.test_settings -v 2
```
This runs both the Enhancement 1 tests and the Enhancement 2 tests.

To run the project's full existing test suite (to confirm we did not break
anything):
```bash
python -m django test tests.test_ticket_actions tests.test_update_ticket_view \
    tests.test_staff_ticket_view tests.test_staff_ticket_list_view \
    tests.test_navigation tests.test_dashboard_sorting tests.test_status_css_classes \
    --settings=tests.test_settings
```

## Files we changed
- `src/helpdesk/settings.py` - added `WAITING_STATUS = 6`, the new entry in
  `DEFAULT_TICKET_STATUS_CHOICES`, `DEFAULT_TICKET_OPEN_STATUSES`,
  `DEFAULT_TICKET_STATUS_CHOICES_FLOW`, and `DEFAULT_TICKET_STATUS_CSS_CLASSES`.
- `src/helpdesk/urls.py` - added the `transfer` URL pattern.
- `src/helpdesk/views/staff.py` - added the `transfer_ticket` view.
- `src/helpdesk/templates/helpdesk/ticket_desc_table.html` - added the
  `Transfer` entry to the Actions dropdown.
- `src/helpdesk/templates/helpdesk/ticket_transfer.html` - new template for
  the transfer form.
- `tests/test_team4_enhancements.py` - new tests for both enhancements.

## Demo recording
- `docs/demo/Team4_Demo.mp4` - 1920x1080 Full HD, ~2 min, 30 fps, H.264
- Shows BEFORE (original UI without our enhancements) for the first 6 frames,
  then AFTER (with both enhancements working) for the next 8 frames.
- Subtle Ken Burns zoom on each frame so it looks like a real screen recording,
  not stacked screenshots.

## Worksheet and presentation notes
- `docs/Team4_Feature_Enhancement_Worksheet.pdf` - 12-page full writeup in
  the same format as the worked example distributed in class.
- `docs/Team4_Presentation_Notes.docx` - simple 2-page presentation notes
  in Word format. Bullet-pointed, simple English, covers everything in the
  worksheet so we can present it without missing anything.
