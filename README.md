# project

## Features
✅ Reader Microservice (Publisher)
Reads a CSV file line-by-line & Sends each row as a message to RabbitMQ queue

✅ Consumer Microservice
Listens to RabbitMQ queue & Saves each message into PostgreSQL

✅ API Microservice
Endpoint: GET /users?pageno=1&pagesize=10&name=John
Supports:
Search by name
Pagination
Filtering

## Tech Stack
- **FastAPI** – Web framework
- **PostgreSQL** – Database
- **PgAdmin** – Database GUI
- **RabbitMQ** – Message broker
- **Pika** – RabbitMQ client
- **SQLAlchemy** – ORM
- **Docker Compose** – Service orchestration

## CSV Format (data.csv)
id,firstname,lastname,email,phone
1,John,Doe,john@example.com,1234567890

sample taken from https://www.datablist.com/learn/csv/download-sample-csv-files#customers-dataset

🚀 Running the Project
1. Clone the repo
git clone <repo-url>
cd project
