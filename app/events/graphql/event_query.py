import graphene

from app.events.graphql.event_object import EventObject
from app.events.models.event_model import Event as EventModel


class EventQuery(graphene.ObjectType):
    """
    GraphQL query to retrieve a list of events, optionally filtered by name.
    """

    events = graphene.List(EventObject, name=graphene.String())

    def resolve_events(self, info, name=None):
        """
        Resolver for events query. Retrieves all events, optionally filtering by name.
        """
        # Use the get_query method to obtain the SQLAlchemy query
        query = EventObject.get_query(info)

        if name:
            query = query.filter(
                EventModel.name.ilike(f"%{name}%")
            )  # Case-insensitive filter

        return query.all()
