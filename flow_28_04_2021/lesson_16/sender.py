import pika

from pika import PlainCredentials


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost', credentials=PlainCredentials("rmquser", "rmqpass")))
channel = connection.channel()

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=b'Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
