import graphene

from app.events.graphql.event_query import EventQuery

from .event_schema import EventMutation


class Query(EventQuery, graphene.ObjectType):
    """
    Root query that combines all event-related queries.
    """

    pass


class Mutation(EventMutation, graphene.ObjectType):
    """
    Root mutation that combines all event-related mutations.
    """

    pass


# Define the GraphQL schema with query and mutation capabilities.
schema = graphene.Schema(query=Query, mutation=Mutation)
