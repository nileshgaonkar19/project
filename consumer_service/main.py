import os, ast, pika
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
 
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    phone = Column(String)

    __tablename__ = 'users'

def callback(ch, method, properties, body):
    session = SessionLocal()
    try:
        data = ast.literal_eval(body.decode())
        print("Inserted data -->",data)
        user = User(firstname=data['firstname'],lastname=data['lastname'],email=data['email'],phone=data['phone'])
        session.add(user)
        session.commit()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error:", e)
        session.rollback()
    finally:
        session.close()


Base.metadata.create_all(bind=engine) # Create table if not exists

connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST")))
channel = connection.channel()
channel.queue_declare(queue=os.getenv("RABBITMQ_QUEUE"), durable=True)
channel.basic_consume(queue=os.getenv("RABBITMQ_QUEUE"), on_message_callback=callback)

print("Waiting....")
channel.start_consuming()
