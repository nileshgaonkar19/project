import os
import ast
import pika
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Validate environment variables
required_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB", "RABBITMQ_HOST", "RABBITMQ_QUEUE"]
for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

# --- SQLAlchemy Setup ---
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- User Model ---
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    phone = Column(String)

    __tablename__ = 'users'

# Create table if not exists
Base.metadata.create_all(bind=engine)

# --- RabbitMQ Callback ---
def callback(ch, method, properties, body):
    session = SessionLocal()
    try:
        data = ast.literal_eval(body.decode())

        # Basic validation
        if not all(k in data for k in ('firstname', 'lastname', 'email', 'phone')):
            raise ValueError("Missing required fields in message")

        print("Received:", data)

        user = User(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            phone=data['phone']
        )
        session.add(user)
        session.commit()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error processing message:", e)
        session.rollback()
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    finally:
        session.close()

# --- RabbitMQ Setup ---
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST")))
    channel = connection.channel()
    channel.queue_declare(queue=os.getenv("RABBITMQ_QUEUE"), durable=True)
    channel.basic_consume(queue=os.getenv("RABBITMQ_QUEUE"), on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
except pika.exceptions.AMQPConnectionError as e:
    print("Failed to connect to RabbitMQ:", e)
