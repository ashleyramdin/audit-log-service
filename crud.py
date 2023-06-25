from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
import uuid
import models
import schemas


# method to fetch all events
def get_events(db: Session):
    return db.query(models.Events).all()


# method to retrieve event based on filtered fields
def get_filtered_events(db: Session, field_values: dict):
    # exact field matching
    # filter_conditions = [getattr(models.Events, f) == v for f, v in field_values.items() if v is not None]

    # create the search conditions. I chose to use LIKE pattern matching for the purposes of this app.
    # However, the line of code above will perform exact matching on the fields queried.
    filter_conditions = [getattr(models.Events, f).like(f"%{v}%") for f, v in field_values.items() if v is not None]
    records = db.query(models.Events).filter(and_(*filter_conditions)).all()
    return records


# method to create an event
def create_event(db: Session, event: schemas.EventCreate, user):
    event_id = str(uuid.uuid4())  # generate a unique id for the event
    dt = datetime.utcnow()  # create the event timestamp
    # add the event to the db and return the recorded event data
    db_record = models.Events(**event.dict(), id=event_id, user_id=user, created_at=dt)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
