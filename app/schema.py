import graphene

from app.events.graphql.event_query import EventQuery
from app.events.schemas.event_schema import EventMutation
from app.tickets.graphql.ticket_query import TicketQuery
from app.tickets.schemas.ticket_schema import TicketMutation


class Query(EventQuery, TicketQuery, graphene.ObjectType):
    """
    Root query that combines event and ticket queries.
    """

    pass


class Mutation(EventMutation, TicketMutation, graphene.ObjectType):
    """
    Root mutation that combines event and ticket mutations.
    """

    pass


# Single schema combining queries and mutations
schema = graphene.Schema(query=Query, mutation=Mutation)
