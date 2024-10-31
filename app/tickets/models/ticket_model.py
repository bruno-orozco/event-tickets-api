from app import db


class Ticket(db.Model):
    """
    Ticket model representing a ticket for an event, with attributes
    for creation date, redemption status, and event association.
    """

    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    redeemed_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="sold")
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    def __repr__(self):
        return f"<Ticket {self.id}, Status: {self.status}>"
