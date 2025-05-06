# project

## Structure
```
project/
├── api_service/         <- FastAPI API with search/filter/pagination
├── reader_service/      <- Reads CSV and sends to RabbitMQ
├── consumer_service/    <- Consumes from RabbitMQ and saves to PostgreSQL
├── docker-compose.yml   <- Docker file
├── .env                 <- Envirement variables
└── README.md
```

## Features
**Reader Microservice (Publisher)**
- Reads a CSV file line-by-line & Sends each row as a message to RabbitMQ queue

**Consumer Microservice (Consumer)**
- Listens to RabbitMQ queue & Saves each message into PostgreSQL

**API Microservice**
- Endpoint: GET /users?pageno=1&pagesize=10&name=John
- Supports:
    - Search by name
    - Pagination
    -  Filtering

## Tech Stack
- **FastAPI** – Web framework
- **PostgreSQL** – Database
- **PgAdmin** – Database GUI
- **RabbitMQ** – Message broker
- **Pika** – RabbitMQ client
- **SQLAlchemy** – ORM
- **Docker Compose** – Service orchestration

## CSV Format (data.csv)
```
id,firstname,lastname,email,phone
1,John,Doe,john@example.com,1234567890

```
sample taken from https://www.datablist.com/learn/csv/download-sample-csv-files#customers-dataset


## Running the Project
*1. Clone the repo*
```
git clone <repo-url>
cd project

```

*2. install requirements*

```
pip install -r requirements.txt

```

*3. Start services with Docker*
```
docker-compose up --build

```
```
PostgreSQL: localhost:5432

RabbitMQ: localhost:5672

pgAdmin: http://localhost:5050

FastAPI: http://localhost:8000/docs

```

*4. Run Publisher (CSV Reader)*
```
cd reader_service
python main.py

```

*5. Run Consumer*
```
cd consumer_service
python main.py

```

## API Example

## Request:
```
GET /users?pageno=1&pagesize=2&name=Sheryl

eg : http://127.0.0.1:8000/users?pageno=1&pagesize=2&name=Sheryl

```

## Response:

```
{
  "total_count": 10,
  "filtered_count": 10,
  "page_size": 2,
  "page_number": 1,
  "users": [
    {
      "id": 1,
      "firstname": "Sheryl",
      "lastname": "Baxter",
      "email": "zunigavanessa@smith.info",
      "phone": "229.077.5154"
    },
    {
      "id": 9,
      "firstname": "Sheryl",
      "lastname": "Meyers",
      "email": "mariokhan@ryan-pope.org",
      "phone": "854-138-4911x5772"
    }
  ]
}
```