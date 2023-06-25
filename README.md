# Audit Log Service

This is an Audit Log Service that allows retrieving and creating events. It provides the following routes:

- `GET /events`: Retrieve a list of all events.
- `GET /events/query`: Query events based on specified fields.
- `POST /events/create`: Create a new event.

## Installation and Setup

### Dependencies

You must have the following installed:
- Python 3.10+

### Running the Application

The following command will create a virtual environment, activate it,
install the required dependencies and start the application.

   ```bash
   python3 -m venv env && source env/bin/activate && pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8000
   ```

The SQLite database `audit_log_app.db` is included. There is no need to run migrations as it is already updated with sample data.


### API Documentation

Once the application is running, you can access the Swagger documentation for the application in your browser
through this URL: `http://localhost:8000/docs`


## Testing the Routes

You can use CURL commands to test each route.
Here are examples of how to test each route, including Basic Authentication with a username and password.

*Note: Replace `username` and `password` with the authentication credentials in the main.py file.*


1. **Retrieve a list of all events:**

   ```bash
   curl -u username:password http://localhost:8000/events
   ```

2. **Query events based on specified fields:**

   ```bash
   curl -u username:password "http://localhost:8000/events/query?event_type=account_created"
   ```

3. **Create a new event:**

   ```bash
   curl -u username:password -X POST -H "Content-Type: application/json" -d "{\"event_type\": \"account_created\", \"event_data\": \"account_number:123010;customer_id:DS003;\", \"reason\": \"A new customer account was created for a given identity.\"}" "http://localhost:8000/events/create"
   ```

   *Note: Adjust the event details in the JSON payload based on the event data you want to insert.*
