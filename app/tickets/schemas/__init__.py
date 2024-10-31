import graphene

from app.tickets.graphql.ticket_query import TicketQuery

from .ticket_schema import TicketMutation


class Query(TicketQuery, graphene.ObjectType):
    """
    Root query class that combines all ticket-related queries.
    """

    pass


class Mutation(TicketMutation, graphene.ObjectType):
    """
    Root mutation class that combines all ticket-related mutations.
    """

    pass


# Define the GraphQL schema with query and mutation capabilities
schema = graphene.Schema(query=Query, mutation=Mutation)
