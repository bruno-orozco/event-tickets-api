import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.events.models.event_model import Event as EventModel
from app.tickets.graphql.ticket_object import TicketObject


class EventObject(SQLAlchemyObjectType):
    """
    GraphQL representation of an Event, including related tickets.
    """

    class Meta:
        model = EventModel

    tickets = graphene.List(TicketObject)

    def resolve_tickets(self, info):
        """
        Resolver for the tickets field, retrieving associated tickets for the event.
        """
        return self.tickets.all()
