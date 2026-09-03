"""Tests written by Team 4 for our two enhancements.

These cover the test scenarios T1-T5 from the worksheet for each enhancement.
They double as regression tests: any future change that breaks the new
behaviour will fail here.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from helpdesk.models import Queue, Ticket, FollowUp, TicketChange
from helpdesk import settings as helpdesk_settings

User = get_user_model()


class WaitingForCustomerTests(TestCase):
    """Tests for Enhancement 1: Waiting for Customer status."""

    @classmethod
    def setUpTestData(cls):
        cls.queue = Queue.objects.create(title="Test Queue", slug="test")
        cls.agent = User.objects.create_user("agent", password="x", is_staff=True)
        cls.ticket = Ticket.objects.create(
            title="Wi-Fi problem",
            queue=cls.queue,
            submitter_email="cust@example.com",
        )

    def test_waiting_status_is_a_choice(self):
        labels = [label for _id, label in helpdesk_settings.TICKET_STATUS_CHOICES]
        self.assertIn("Waiting for Customer", labels)

    def test_open_ticket_can_move_to_waiting(self):
        allowed = dict(helpdesk_settings.TICKET_STATUS_CHOICES_FLOW)
        self.assertIn(
            helpdesk_settings.WAITING_STATUS,
            allowed[helpdesk_settings.OPEN_STATUS],
        )

    def test_waiting_ticket_can_resume_to_open(self):
        allowed = dict(helpdesk_settings.TICKET_STATUS_CHOICES_FLOW)
        self.assertIn(
            helpdesk_settings.OPEN_STATUS,
            allowed[helpdesk_settings.WAITING_STATUS],
        )

    def test_waiting_is_in_open_statuses(self):
        # A waiting ticket is still active work (not closed/resolved).
        self.assertIn(
            helpdesk_settings.WAITING_STATUS,
            helpdesk_settings.TICKET_OPEN_STATUSES,
        )


class TransferTicketTests(TestCase):
    """Tests for Enhancement 2: Transfer to another queue."""

    @classmethod
    def setUpTestData(cls):
        cls.source = Queue.objects.create(title="Source Queue", slug="src")
        cls.destination = Queue.objects.create(title="Destination Queue", slug="dst")
        cls.agent = User.objects.create_user("agent2", password="x", is_staff=True)
        cls.ticket = Ticket.objects.create(
            title="Move me",
            queue=cls.source,
            submitter_email="cust@example.com",
        )

    def setUp(self):
        self.client.login(username="agent2", password="x")

    def test_transfer_page_loads(self):
        resp = self.client.get(f"/tickets/{self.ticket.id}/transfer/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Transfer")

    def test_transfer_moves_ticket_to_destination(self):
        resp = self.client.post(
            f"/tickets/{self.ticket.id}/transfer/",
            data={"queue": str(self.destination.id), "comment": "wrong team"},
        )
        self.assertEqual(resp.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.queue, self.destination)

    def test_transfer_creates_history_followup(self):
        self.client.post(
            f"/tickets/{self.ticket.id}/transfer/",
            data={"queue": str(self.destination.id), "comment": "wrong team"},
        )
        followups = FollowUp.objects.filter(ticket=self.ticket)
        self.assertTrue(
            followups.filter(title__icontains="transferred").exists()
        )

    def test_transfer_records_queue_change(self):
        self.client.post(
            f"/tickets/{self.ticket.id}/transfer/",
            data={"queue": str(self.destination.id)},
        )
        changes = TicketChange.objects.filter(field="Queue")
        self.assertTrue(changes.exists())
        change = changes.first()
        self.assertEqual(change.old_value, "Source Queue")
        self.assertEqual(change.new_value, "Destination Queue")

    def test_transfer_to_same_queue_is_rejected(self):
        resp = self.client.post(
            f"/tickets/{self.ticket.id}/transfer/",
            data={"queue": str(self.source.id)},
        )
        # Same-queue is not in destination_choices, so the form is shown again
        self.assertEqual(resp.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.queue, self.source)

    def test_transfer_leaves_status_and_priority_unchanged(self):
        self.ticket.priority = 2
        self.ticket.status = helpdesk_settings.OPEN_STATUS
        self.ticket.save()
        self.client.post(
            f"/tickets/{self.ticket.id}/transfer/",
            data={"queue": str(self.destination.id)},
        )
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.priority, 2)
        self.assertEqual(self.ticket.status, helpdesk_settings.OPEN_STATUS)
