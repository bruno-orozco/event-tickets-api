from app.events.services.event_service import EventService


class EventController:
    """
    Controller for handling event-related operations via the EventService.
    """

    @staticmethod
    def create_event(name, start_date, end_date, total_tickets):
        """
        Creates a new event with the provided details.
        """
        return EventService.create_event(name, start_date, end_date, total_tickets)

    @staticmethod
    def get_all_events(name=None):
        """
        Retrieves all events, optionally filtering by name.
        """
        return EventService.get_all_events(name)

    @staticmethod
    def get_event_by_id(event_id):
        """
        Retrieves a single event by its unique ID.
        """
        return EventService.get_event_by_id(event_id)

    @staticmethod
    def update_event(
        event_id,
        name=None,
        start_date=None,
        end_date=None,
        total_tickets=None,
    ):
        """
        Updates an existing event with provided details.
        """
        return EventService.update_event(
            event_id,
            name,
            start_date,
            end_date,
            total_tickets,
        )

    @staticmethod
    def delete_event(event_id):
        """
        Deletes an event by its unique ID.
        """
        return EventService.delete_event(event_id)
