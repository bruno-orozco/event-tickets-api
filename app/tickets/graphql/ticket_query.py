import graphene

from app.tickets.graphql.ticket_object import TicketObject
from app.tickets.models.ticket_model import Ticket as TicketModel


class TicketQuery(graphene.ObjectType):
    """
    GraphQL query to retrieve a list of tickets, optionally filtered by event ID.
    """

    tickets = graphene.List(TicketObject, event_id=graphene.Int())

    def resolve_tickets(self, info, event_id=None):
        """
        Resolver for the tickets query.
        """
        # Use get_query method to obtain the SQLAlchemy query
        query = TicketObject.get_query(info)

        if event_id:
            query = query.filter(TicketModel.event_id == event_id)

        return query.all()
