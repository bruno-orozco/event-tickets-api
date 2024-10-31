from datetime import datetime

from app import db
from app.events.models.event_model import Event as EventModel


class EventService:
    """
    Service to handle business logic related to events.
    """

    @staticmethod
    def create_event(name, start_date, end_date, total_tickets):
        """
        Creates a new event after validating dates and total tickets.
        """
        EventService._validate_dates_create(start_date, end_date)
        EventService._validate_total_tickets_create(total_tickets)

        event = EventModel(
            name=name,
            start_date=start_date,
            end_date=end_date,
            total_tickets=total_tickets,
            sold_tickets=0,
        )
        db.session.add(event)
        db.session.commit()
        return event

    @staticmethod
    def get_all_events(name=None):
        """
        Retrieves all events, optionally filtered by name.
        """
        query = EventModel.query
        if name:
            query = query.filter(EventModel.name == name)
        return query.all()

    @staticmethod
    def get_event_by_id(event_id):
        """
        Retrieves an event by its ID.
        """
        return EventModel.query.get(event_id)

    @staticmethod
    def update_event(
        event_id, name=None, start_date=None, end_date=None, total_tickets=None
    ):
        """
        Updates an existing event after validating dates and total tickets.
        """
        event = EventService.get_event_by_id(event_id)
        if not event:
            raise Exception("Event not found")

        EventService._validate_dates_update(start_date, end_date, event)
        EventService._validate_total_tickets_update(total_tickets, event.sold_tickets)

        if name:
            event.name = name
        if start_date:
            event.start_date = start_date
        if end_date:
            event.end_date = end_date
        if total_tickets is not None:
            event.total_tickets = total_tickets

        db.session.commit()
        return event

    @staticmethod
    def delete_event(event_id):
        """
        Deletes an event if the end date has passed or if no tickets have been sold.
        """
        event = EventService.get_event_by_id(event_id)

        if not event:
            raise Exception("Event not found")

        EventService._validate_delete_event(event)

        db.session.delete(event)
        db.session.commit()
        return True

    @staticmethod
    def _validate_dates_create(start_date, end_date):
        """
        Validates dates when creating an event.
        """
        today = datetime.now().date()
        if start_date < today:
            raise ValueError("Start date must be today or a future date.")
        if end_date < start_date:
            raise ValueError("End date cannot be earlier than the start date.")

    @staticmethod
    def _validate_total_tickets_create(total_tickets):
        """
        Validates the total number of tickets when creating an event.
        """
        if not (1 <= total_tickets <= 300):
            raise ValueError("Total tickets must be between 1 and 300.")

    @staticmethod
    def _validate_dates_update(start_date, end_date, event):
        """
        Validates dates when updating an event.
        """
        today = datetime.now().date()

        if start_date and start_date < today:
            raise ValueError("Start date cannot be earlier than today.")

        if end_date:
            effective_start_date = start_date if start_date else event.start_date
            if end_date < effective_start_date:
                raise ValueError("End date cannot be earlier than the start date.")

    @staticmethod
    def _validate_total_tickets_update(total_tickets, sold_tickets):
        """
        Validates the total number of tickets when updating an event.
        """
        if total_tickets is not None:
            if total_tickets < sold_tickets:
                raise ValueError(
                    f"Cannot set total tickets to {total_tickets} as {sold_tickets} tickets are already sold."
                )
            if total_tickets < 1:
                raise ValueError("Total tickets must be at least 1.")

    @staticmethod
    def _validate_delete_event(event):
        """
        Validates if an event can be deleted.
        """
        if event.sold_tickets > 0:
            raise Exception("Cannot delete the event because tickets have been sold.")

        today = datetime.now().date()
        if event.end_date > today:
            raise Exception("Cannot delete the event because it has not yet ended.")
