from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
import datetime
import schemas


# init app
app = FastAPI(title="Audit Log")
security = HTTPBasic()


# authentication credentials
username = 'harrypotter'
password = 'snape123'


# get the db instance
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# NOTE: the credentials above is not a secure solution and only used for the purpose of this project.
# TODO: develop table to store clients that have access to the api,
#  use clients table to verify the authentication credentials


# HELPER METHODS

# method to verify the authentication credentials
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != username or credentials.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# ROUTES

@app.get('/', tags=["Home"])
async def home():
    return {"message": "Hello! Welcome to Ashley's Audit Log Service!"}


# NOTE: any authenticated user can retrieve all events for all users
# enhancements to events retrieval:
#  * implement RBAC and restrict records returned based on user privileges
@app.get('/events', tags=["Events"], response_model=list[schemas.Event])
def retrieve_events(
        db: Session = Depends(get_db),
        user: str = Depends(verify_credentials)):
    """
    ### Retrieve the recorded events.\n
    :param db: database session\n
    :param user: username of the authenticated user\n
    :return: list of event data\n
    """
    # query the db for the list of all events
    events = crud.get_events(db=db)
    return events


# enhancements to searching for specific records:
#  * ability to search during a particular timeframe
#  * ability to search based on an exact match on selected fields
@app.get('/events/query', tags=["Events"], response_model=list[schemas.Event])
def retrieve_events_by_field(
        event_type: str | None = None,
        event_data: str | None = None,
        reason: str | None = None,
        event_id: str | None = None,
        user_id: str | None = None,
        db: Session = Depends(get_db),
        user: str = Depends(verify_credentials)):
    """
    ### Retrieve recorded events based on the specified fields.\n
    :param user_id: username of the client that committed the record\n
    :param event_id: unique id of the event\n
    :param reason: reason that the event occurred\n
    :param event_data: additional data for the required event\n
    :param event_type: type of event\n
    :param db: database session\n
    :param user: username of the authenticated user\n
    :return: list of event data\n
    """
    # ensure at least one field was provided
    if not (event_type or event_data or reason or event_id or user_id):
        raise HTTPException(
            status_code=400,
            detail='At least one query field must be provided.')
    # compile the field values to be queried
    field_values = dict(
        event_type=event_type,
        event_data=event_data,
        reason=reason,
        id=event_id,
        user_id=user_id)
    # query the db for the list of all events
    events = crud.get_filtered_events(db=db, field_values=field_values)
    return events


@app.post('/events/create', tags=["Events"], response_model=schemas.Event)
def submit_event(event: schemas.EventCreate,
                 user: str = Depends(verify_credentials),
                 db: Session = Depends(get_db)):
    """
    ### Create a new event entry.\n
    :param event: event data in json format\n
    :param user: username of the authenticated user\n
    :param db: database session\n
    :return: saved event data\n
    """
    return crud.create_event(db=db, event=event, user=user)
