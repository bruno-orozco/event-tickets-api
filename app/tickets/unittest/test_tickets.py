from unittest.mock import patch

import pytest

from app.tickets.controllers.ticket_controller import TicketController
from app.tickets.services.ticket_service import TicketService


# Fixture para simular la respuesta de un boleto vendido
@pytest.fixture
def mock_ticket_sale():
    return {"ticket": {"id": 1, "status": "SOLD", "event": {"id": 1, "name": "Concert"}}}


# Fixture para simular la respuesta de un boleto canjeado
@pytest.fixture
def mock_ticket_redeem():
    return {"ticket": {"id": 3, "redeemedAt": "2023-10-31T10:00:00"}}


# Pruebas para el método sell_ticket
class TestSellTicket:
    @patch.object(TicketService, "sell_ticket")
    def test_sell_ticket_success(self, mock_sell_ticket, mock_ticket_sale):
        # Configurar el mock para devolver la venta exitosa del boleto
        mock_sell_ticket.return_value = mock_ticket_sale

        # Ejecutar el método del controlador
        result = TicketController.sell_ticket(event_id=1)

        # Validar que la respuesta es la esperada
        assert result == mock_ticket_sale
        assert result["ticket"]["status"] == "SOLD"
        assert result["ticket"]["event"]["id"] == 1
        assert result["ticket"]["event"]["name"] == "Concert"

    @patch.object(TicketService, "sell_ticket")
    def test_sell_ticket_no_availability(self, mock_sell_ticket):
        # Configurar el mock para simular que no hay disponibilidad de boletos
        mock_sell_ticket.side_effect = Exception("No tickets available")

        # Ejecutar y verificar que se lanza una excepción en caso de no disponibilidad
        with pytest.raises(Exception, match="No tickets available"):
            TicketController.sell_ticket(event_id=1)


# Pruebas para el método redeem_ticket
class TestRedeemTicket:
    @patch.object(TicketService, "redeem_ticket")
    def test_redeem_ticket_success(self, mock_redeem_ticket, mock_ticket_redeem):
        # Configurar el mock para devolver el canje exitoso del boleto
        mock_redeem_ticket.return_value = mock_ticket_redeem

        # Ejecutar el método del controlador
        result = TicketController.redeem_ticket(ticket_id=3)

        # Validar que la respuesta es la esperada
        assert result == mock_ticket_redeem
        assert result["ticket"]["id"] == 3
        assert "redeemedAt" in result["ticket"]

    @patch.object(TicketService, "redeem_ticket")
    def test_redeem_ticket_already_redeemed(self, mock_redeem_ticket):
        # Configurar el mock para simular que el boleto ya ha sido canjeado
        mock_redeem_ticket.side_effect = Exception("Ticket already redeemed")

        # Ejecutar y verificar que se lanza una excepción en caso de boleto ya canjeado
        with pytest.raises(Exception, match="Ticket already redeemed"):
            TicketController.redeem_ticket(ticket_id=3)

    @patch.object(TicketService, "redeem_ticket")
    def test_redeem_ticket_out_of_date(self, mock_redeem_ticket):
        # Configurar el mock para simular que el boleto está fuera del período de validez
        mock_redeem_ticket.side_effect = Exception("Ticket redemption period expired")

        # Ejecutar y verificar que se lanza una excepción en caso de que esté fuera de fecha
        with pytest.raises(Exception, match="Ticket redemption period expired"):
            TicketController.redeem_ticket(ticket_id=3)
