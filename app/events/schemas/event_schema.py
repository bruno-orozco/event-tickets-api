import graphene
from graphene import relay
from graphql import GraphQLError

from app.events.controllers.event_controller import EventController
from app.events.graphql.event_object import EventObject


class BadRequestException(GraphQLError):
    """
    Exception to handle bad requests, returns a 400 error.
    """

    pass


class EventInput(graphene.InputObjectType):
    """
    Defines input fields for creating an event.
    """

    name = graphene.String(required=True)
    start_date = graphene.Date(required=True)
    end_date = graphene.Date(required=True)
    total_tickets = graphene.Int(required=True)


class CreateEventMutation(graphene.Mutation):
    """
    Mutation to create a new event.
    """

    class Arguments:
        input = EventInput(required=True)

    event = graphene.Field(EventObject)

    def mutate(self, info, input):
        try:
            event = EventController.create_event(
                name=input.name,
                start_date=input.start_date,
                end_date=input.end_date,
                total_tickets=input.total_tickets,
            )
            return CreateEventMutation(event=event)
        except ValueError as e:
            raise BadRequestException(str(e))


class UpdateEventInput(graphene.InputObjectType):
    """
    Defines input fields for updating an event.
    """

    id = graphene.Int(required=True)
    name = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    total_tickets = graphene.Int()


class UpdateEventMutation(graphene.Mutation):
    """
    Mutation to update an existing event.
    """

    class Arguments:
        input = UpdateEventInput(required=True)

    event = graphene.Field(EventObject)

    def mutate(self, info, input):
        try:
            event = EventController.update_event(
                event_id=input.id,
                name=input.name,
                start_date=input.start_date,
                end_date=input.end_date,
                total_tickets=input.total_tickets,
            )
            return UpdateEventMutation(event=event)
        except ValueError as e:
            raise BadRequestException(str(e))
        except Exception:
            raise BadRequestException("Event not found")


class DeleteEventMutation(graphene.Mutation):
    """
    Mutation to delete an event.
    """

    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        try:
            success = EventController.delete_event(id)
            return DeleteEventMutation(ok=success)
        except Exception as e:
            raise BadRequestException(str(e))


class EventQuery(graphene.ObjectType):
    """
    Query to retrieve events.
    """

    node = relay.Node.Field()
    events = graphene.List(EventObject, name=graphene.String())

    def resolve_events(self, name=None):
        return EventController.get_all_events(name)


class EventMutation(graphene.ObjectType):
    """
    Mutation operations for event creation, update, and deletion.
    """

    create_event = CreateEventMutation.Field()
    update_event = UpdateEventMutation.Field()
    delete_event = DeleteEventMutation.Field()
