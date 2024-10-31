import graphene

from app import db
from app.events.graphql.event_object import EventObject
from app.events.models.event_model import Event as EventModel


class EventInput(graphene.InputObjectType):
    """
    Input fields required to create or modify an event.
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
        input = EventInput(required=True)  # Cambiamos nuevamente a 'input'

    event = graphene.Field(EventObject)

    def mutate(self, input):
        # Validación de las fechas
        if input.start_date > input.end_date:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        # Crear un nuevo evento
        event = EventModel(
            name=input.name,
            start_date=input.start_date,
            end_date=input.end_date,
            total_tickets=input.total_tickets,
        )

        db.session.add(event)
        db.session.commit()

        return CreateEventMutation(event=event)