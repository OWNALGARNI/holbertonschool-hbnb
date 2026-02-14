import uuid
from datetime import datetime

from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def to_dict(self):
        data = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            # Convert datetime to ISO format string
            if isinstance(value, datetime):
                value = value.isoformat()
            data[c.name] = value
        return data
