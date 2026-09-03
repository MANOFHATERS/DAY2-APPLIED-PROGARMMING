"""Tests written by Team 4 for Enhancement 1 (Waiting for Customer)."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from helpdesk.models import Queue, Ticket
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

    def test_resolved_ticket_cannot_move_directly_to_waiting(self):
        allowed = dict(helpdesk_settings.TICKET_STATUS_CHOICES_FLOW)
        self.assertNotIn(
            helpdesk_settings.WAITING_STATUS,
            allowed[helpdesk_settings.RESOLVED_STATUS],
        )

    def test_waiting_is_in_open_statuses(self):
        self.assertIn(
            helpdesk_settings.WAITING_STATUS,
            helpdesk_settings.TICKET_OPEN_STATUSES,
        )

    def test_waiting_has_a_css_class(self):
        self.assertIn(
            helpdesk_settings.WAITING_STATUS,
            helpdesk_settings.TICKET_STATUS_CSS_CLASSES,
        )
