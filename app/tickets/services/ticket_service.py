from datetime import datetime

from app import db
from app.events.models.event_model import Event as EventModel
from app.tickets.models.ticket_model import Ticket as TicketModel


class TicketService:
    """
    Service class for managing tickets, including selling, redeeming, and retrieving tickets.
    """

    @staticmethod
    def sell_ticket(event_id):
        """
        Sells a ticket for the specified event if tickets are available.
        """
        event = EventModel.query.get(event_id)
        if not event:
            raise ValueError("Event not found", 404)

        if event.sold_tickets >= event.total_tickets:
            raise ValueError("No tickets available", 409)

        # Create a ticket without the redeemed flag initially set
        ticket = TicketModel(event_id=event_id)
        ticket.redeemed = False  # Set 'redeemed' after creation

        event.sold_tickets += 1
        db.session.add(ticket)
        db.session.commit()
        return ticket

    @staticmethod
    def redeem_ticket(ticket_id):
        """
        Redeems a ticket if it has not already been redeemed and the event is within its valid date range.
        """
        ticket = TicketModel.query.get(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found", 404)

        event = EventModel.query.get(ticket.event_id)
        if not event:
            raise ValueError("Associated event not found", 404)

        # Check if the ticket has already been redeemed
        if ticket.redeemed:
            raise ValueError("The ticket has already been redeemed", 409)

        # Check if the event is within the valid date range
        current_date = datetime.now().date()
        if not (event.start_date <= current_date <= event.end_date):
            raise ValueError("The event is not within the valid period", 409)

        # Redeem the ticket
        ticket.redeemed = True
        db.session.commit()
        return ticket

    @staticmethod
    def get_all_tickets():
        """
        Returns all registered tickets.
        """
        return TicketModel.query.all()

    @staticmethod
    def get_ticket_by_id(ticket_id):
        """
        Returns a specific ticket by its ID.
        """
        return TicketModel.query.get(ticket_id)

    @staticmethod
    def delete_ticket(ticket_id):
        """
        Deletes a specific ticket by its ID.
        """
        ticket = TicketModel.query.get(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found", 404)
        db.session.delete(ticket)
        db.session.commit()
        return True
