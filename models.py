from sqlalchemy import Column, String, DateTime

from database import Base


class Events(Base):
    __tablename__ = "events"

    id = Column(String(50), primary_key=True, index=True)  # unique event id
    user_id = Column(String(50), index=True)  # if there was a users table, this would be a foreign key relation
    event_type = Column(String(50), index=True)  # type of event
    reason = Column(String(100))  # the reason or description for the event
    event_data = Column(String(256))  # event specific data. e.g. account number
    created_at = Column(DateTime)  # timestamp
