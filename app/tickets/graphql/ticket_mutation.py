from datetime import datetime

import graphene

from app import db
from app.events.models.event_model import Event as EventModel
from app.tickets.graphql.ticket_object import TicketObject
from app.tickets.models.ticket_model import Ticket as TicketModel


class SellTicketMutation(graphene.Mutation):
    """
    Mutation to handle ticket sales for an event.
    """

    class Arguments:
        event_id = graphene.Int(required=True)

    ticket = graphene.Field(TicketObject)

    def mutate(self, info, event_id):
        # Check if the event exists
        event = EventModel.query.get(event_id)
        if not event:
            raise Exception("Event not found", 404)

        # Check ticket availability
        if event.sold_tickets >= event.total_tickets:
            raise Exception("No tickets available", 409)

        # Sell a ticket
        ticket = TicketModel(event_id=event_id, redeemed=False)
        event.sold_tickets += 1
        db.session.add(ticket)
        db.session.commit()

        return SellTicketMutation(ticket=ticket)


class RedeemTicketMutation(graphene.Mutation):
    """
    Mutation to handle ticket redemption for an event.
    """

    class Arguments:
        ticket_id = graphene.Int(required=True)

    ticket = graphene.Field(TicketObject)

    def mutate(self, info, ticket_id):
        # Check if the ticket exists
        ticket = TicketModel.query.get(ticket_id)
        if not ticket:
            raise Exception("Ticket not found", 404)

        # Check if the ticket has already been redeemed
        if ticket.redeemed:
            raise Exception("The ticket has already been redeemed", 409)

        # Verify that the event is within the valid period
        event = EventModel.query.get(ticket.event_id)
        current_date = datetime.now().date()
        if not (event.start_date <= current_date <= event.end_date):
            raise Exception("The event is not within the valid period", 409)

        # Update redeemed ticket count and mark the ticket as redeemed
        event.redeemed_tickets += 1
        ticket.redeemed = True
        db.session.commit()

        return RedeemTicketMutation(ticket=ticket)


class TicketMutation(graphene.ObjectType):
    """
    Root mutation for ticket-related operations.
    """

    sell_ticket = SellTicketMutation.Field()
    redeem_ticket = RedeemTicketMutation.Field()
