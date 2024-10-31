from app.tickets.services.ticket_service import TicketService


class TicketController:
    @staticmethod
    def sell_ticket(event_id):
        """
        Vende un boleto para el evento especificado si hay disponibilidad.
        """
        return TicketService.sell_ticket(event_id)

    @staticmethod
    def redeem_ticket(ticket_id):
        """
        Canjea un boleto si está en el período de validez y aún no ha sido canjeado.
        """
        return TicketService.redeem_ticket(ticket_id)

    @staticmethod
    def get_all_tickets():
        """
        Obtiene todos los boletos.
        """
        return TicketService.get_all_tickets()

    @staticmethod
    def get_ticket_by_id(ticket_id):
        """
        Obtiene un boleto específico por su ID.
        """
        return TicketService.get_ticket_by_id(ticket_id)

    @staticmethod
    def delete_ticket(ticket_id):
        """
        Elimina un boleto específico por su ID.
        """
        return TicketService.delete_ticket(ticket_id)
