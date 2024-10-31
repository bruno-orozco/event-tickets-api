from app import db


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    sold_tickets = db.Column(db.Integer, default=0)
    redeemed_tickets = db.Column(db.Integer, default=0)

    # Relación solo definida en Event, evitando la dependencia circular
    tickets = db.relationship(
        "Ticket", backref="event", cascade="all, delete-orphan", lazy="dynamic"
    )
