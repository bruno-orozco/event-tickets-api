from unittest.mock import patch

import pytest

from app.events.controllers.event_controller import EventController
from app.events.services.event_service import EventService


# Fixture para simular un evento creado exitosamente
@pytest.fixture
def mock_event_creation():
    return {
        "event": {
            "id": 1,
            "name": "Concierto de Pop",
            "startDate": "2024-12-01",
            "endDate": "2024-12-02",
            "totalTickets": 100,
            "soldTickets": 0,
            "tickets": [],
        }
    }


@pytest.fixture
def mock_event_creation_min():
    return {
        "event": {
            "id": 1,
            "name": "Concierto de Pop",
            "startDate": "2024-12-01",
            "endDate": "2024-12-02",
            "totalTickets": 1,
            "soldTickets": 0,
            "tickets": [],
        }
    }


# Fixture para simular detalles de un evento
@pytest.fixture
def mock_event_details():
    return {
        "id": 1,
        "name": "Concierto de Rock",
        "startDate": "2024-12-01",
        "endDate": "2024-12-02",
        "totalTickets": 200,
        "soldTickets": 50,
        "tickets": [{"id": 1, "status": "sold"}],
    }


# Pruebas para el método create_event
class TestCreateEvent:
    @patch.object(EventService, "create_event")
    def test_create_event_success(self, mock_create_event, mock_event_creation):
        mock_create_event.return_value = mock_event_creation
        result = EventController.create_event(
            name="Concierto de Pop",
            start_date="2024-12-01",
            end_date="2024-12-02",
            total_tickets=100,
        )
        assert result == mock_event_creation
        assert result["event"]["name"] == "Concierto de Pop"
        assert result["event"]["totalTickets"] == 100

    @patch.object(EventService, "create_event")
    def test_create_event_invalid_dates(self, mock_create_event):
        mock_create_event.side_effect = Exception("End date must be after start date")
        with pytest.raises(Exception, match="End date must be after start date"):
            EventController.create_event(
                name="Concierto de Jazz",
                start_date="2024-12-02",
                end_date="2024-12-01",
                total_tickets=50,
            )

    @patch.object(EventService, "create_event")
    def test_create_event_invalid_tickets(self, mock_create_event):
        mock_create_event.side_effect = Exception(
            "Total tickets must be between 1 and 300"
        )
        with pytest.raises(Exception, match="Total tickets must be between 1 and 300"):
            EventController.create_event(
                name="Concierto de Jazz",
                start_date="2024-12-01",
                end_date="2024-12-02",
                total_tickets=500,
            )

    @patch.object(EventService, "create_event")
    def test_create_event_minimum_tickets(
        self, mock_create_event, mock_event_creation_min
    ):
        mock_create_event.return_value = mock_event_creation_min
        result = EventController.create_event(
            name="Evento Mínimo",
            start_date="2024-12-01",
            end_date="2024-12-02",
            total_tickets=1,
        )
        assert result == mock_event_creation_min
        assert result["event"]["totalTickets"] == 1


# Pruebas para el método update_event
class TestUpdateEvent:
    @patch.object(EventService, "update_event")
    def test_update_event_success(self, mock_update_event, mock_event_details):
        mock_update_event.return_value = mock_event_details
        result = EventController.update_event(
            event_id=1,
            name="Concierto de Rock",
            start_date="2024-12-01",
            end_date="2024-12-02",
            total_tickets=200,
        )
        assert result == mock_event_details
        assert result["name"] == "Concierto de Rock"
        assert result["totalTickets"] == 200

    @patch.object(EventService, "update_event")
    def test_update_event_no_optional_args(self, mock_update_event, mock_event_details):
        # Configurar el mock para devolver los detalles del evento sin actualizar nada
        mock_update_event.return_value = mock_event_details
        result = EventController.update_event(event_id=1)
        assert result == mock_event_details

    @patch.object(EventService, "update_event")
    def test_update_event_reduce_tickets_below_sold(self, mock_update_event):
        mock_update_event.side_effect = Exception(
            "Cannot reduce total tickets below sold tickets"
        )
        with pytest.raises(
            Exception, match="Cannot reduce total tickets below sold tickets"
        ):
            EventController.update_event(event_id=1, total_tickets=30)

    @patch.object(EventService, "update_event")
    def test_update_event_increase_tickets(self, mock_update_event, mock_event_details):
        mock_event_details["totalTickets"] = 250
        mock_update_event.return_value = mock_event_details
        result = EventController.update_event(event_id=1, total_tickets=250)
        assert result["totalTickets"] == 250


# Pruebas para el método delete_event
class TestDeleteEvent:
    @patch.object(EventService, "delete_event")
    def test_delete_event_success(self, mock_delete_event):
        mock_delete_event.return_value = {"ok": True}
        result = EventController.delete_event(event_id=3)
        assert result == {"ok": True}

    @patch.object(EventService, "delete_event")
    def test_delete_event_with_unsatisfied_conditions(self, mock_delete_event):
        mock_delete_event.side_effect = Exception("Event cannot be deleted")
        with pytest.raises(Exception, match="Event cannot be deleted"):
            EventController.delete_event(event_id=3)


# Pruebas para el método get_event_by_id y get_all_events
class TestGetEventDetails:
    @patch.object(EventService, "get_event_by_id")
    def test_get_event_by_id_success(self, mock_get_event_by_id, mock_event_details):
        mock_get_event_by_id.return_value = mock_event_details
        result = EventController.get_event_by_id(event_id=1)
        assert result == mock_event_details
        assert result["name"] == "Concierto de Rock"
        assert result["totalTickets"] == 200
        assert result["soldTickets"] == 50

    @patch.object(EventService, "get_event_by_id")
    def test_get_event_by_id_not_found(self, mock_get_event_by_id):
        mock_get_event_by_id.side_effect = Exception("Event not found")
        with pytest.raises(Exception, match="Event not found"):
            EventController.get_event_by_id(event_id=999)

    @patch.object(EventService, "get_all_events")
    def test_get_all_events_success(self, mock_get_all_events):
        mock_get_all_events.return_value = [
            {
                "id": 1,
                "name": "Concierto de Rock",
                "startDate": "2024-12-01",
                "endDate": "2024-12-02",
                "totalTickets": 200,
                "soldTickets": 50,
            },
            {
                "id": 2,
                "name": "Concierto de Jazz",
                "startDate": "2025-01-10",
                "endDate": "2025-01-12",
                "totalTickets": 150,
                "soldTickets": 20,
            },
        ]
        result = EventController.get_all_events()
        assert len(result) == 2
        assert result[0]["name"] == "Concierto de Rock"
        assert result[1]["name"] == "Concierto de Jazz"
        assert result[0]["soldTickets"] == 50
        assert result[1]["soldTickets"] == 20

    @patch.object(EventService, "get_all_events")
    def test_get_all_events_with_filter(self, mock_get_all_events):
        mock_get_all_events.return_value = [
            {
                "id": 1,
                "name": "Concierto de Rock",
                "startDate": "2024-12-01",
                "endDate": "2024-12-02",
                "totalTickets": 200,
                "soldTickets": 50,
            }
        ]
        result = EventController.get_all_events(name="Concierto de Rock")
        assert len(result) == 1
        assert result[0]["name"] == "Concierto de Rock"

    @patch.object(EventService, "get_all_events")
    def test_get_all_events_with_no_results(self, mock_get_all_events):
        mock_get_all_events.return_value = []
        result = EventController.get_all_events()
        assert result == []
