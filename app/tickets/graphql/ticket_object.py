from graphene_sqlalchemy import SQLAlchemyObjectType

from app.tickets.models.ticket_model import Ticket as TicketModel


class TicketObject(SQLAlchemyObjectType):
    """
    GraphQL representation of a Ticket, mapped to the TicketModel.
    """

    class Meta:
        model = TicketModel
