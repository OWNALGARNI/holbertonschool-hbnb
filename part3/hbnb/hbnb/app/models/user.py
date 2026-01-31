from sqlalchemy.orm import relationship

places = relationship(
    "Place",
    backref="owner",
    cascade="all, delete-orphan"
)

reviews = relationship(
    "Review",
    backref="author",
    cascade="all, delete-orphan"
)
