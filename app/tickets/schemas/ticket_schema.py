from datetime import datetime

import graphene
from graphene import relay
from graphql import GraphQLError

from app import db
from app.tickets.controllers.ticket_controller import TicketController
from app.tickets.graphql.ticket_object import TicketObject
from app.tickets.models.ticket_model import Ticket as TicketModel


class BadRequestException(GraphQLError):
    """
    Custom exception for handling bad requests with appropriate status codes.
    """

    pass


class SellTicketInput(graphene.InputObjectType):
    """
    Input fields for selling a ticket.
    """

    event_id = graphene.Int(required=True)


class SellTicketMutation(graphene.Mutation):
    """
    Mutation to handle the selling of a ticket.
    """

    class Arguments:
        input = SellTicketInput(required=True)

    ticket = graphene.Field(TicketObject)

    def mutate(self, info, input):
        try:
            ticket = TicketController.sell_ticket(event_id=input.event_id)
            return SellTicketMutation(ticket=ticket)
        except Exception as e:
            # Handle errors with appropriate status codes in sell_ticket
            raise BadRequestException(str(e))


class RedeemTicketInput(graphene.InputObjectType):
    """
    Input fields for redeeming a ticket.
    """

    ticket_id = graphene.Int(required=True)


class RedeemTicketMutation(graphene.Mutation):
    """
    Mutation to handle the redemption of a ticket.
    """

    class Arguments:
        input = RedeemTicketInput(required=True)

    ticket = graphene.Field(TicketObject)

    def mutate(self, info, input):
        ticket_id = input.ticket_id

        # Check if the ticket exists
        ticket = TicketModel.query.get(ticket_id)
        if not ticket:
            raise BadRequestException("Ticket not found", 404)

        # Check if the ticket has already been redeemed
        if ticket.redeemed_at is not None:
            raise BadRequestException("The ticket has already been redeemed", 409)

        # Redeem the ticket
        ticket.redeemed_at = datetime.now()
        db.session.commit()

        return RedeemTicketMutation(ticket=ticket)


class TicketQuery(graphene.ObjectType):
    """
    Query for retrieving a list of tickets.
    """

    node = relay.Node.Field()
    tickets = graphene.List(TicketObject)

    def resolve_tickets(self, info):
        """
        Resolver for retrieving all tickets.
        """
        return TicketController.get_all_tickets()


class TicketMutation(graphene.ObjectType):
    """
    Root mutation for ticket-related operations.
    """

    sell_ticket = SellTicketMutation.Field()
    redeem_ticket = RedeemTicketMutation.Field()
