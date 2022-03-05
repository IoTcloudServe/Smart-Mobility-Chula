import io
import time
import picamera
from kafka import KafkaProducer
import pickle
import threading
import pickle
from datetime import datetime

producer = [KafkaProducer(bootstrap_servers=['10.0.0.9:9092'], acks = 1, linger_ms = 0, retries = 0, max_in_flight_requests_per_connection = 11)]

#producer.append(KafkaProducer(bootstrap_servers=['10.0.0.9:9092'], acks = 1, linger_ms = 0, retries = 0, max_in_flight_requests_per_connection = 11))

print('all producers instantiated already here')

topic1 = 'PhayaThai-6'

producer_id = 0
batches = 1
frame = 1
image = 1
max_batches = 3
max_image_in_batch = 50
producer_timeout = 5

while True:
    def outputs():
        global producer_id
        global batches
        global max_batches
        global frame
        global image
        global max_image_in_batch
        global producer_timeout

        while True:
            stream1 = io.BytesIO()
            yield stream1
            now = float(round(time.time() * 1000))
            current_time = datetime.now().strftime("%Y-%m-%d_" + "%H:%M:%S")
            img_raw1 = str(frame) + ' chula ' + str(now) +  ' chula ' + stream1.getvalue() + ' chula ' + current_time
#            img_raw1 = str(frame) + ' chula ' + str(now) +  ' chula ' + stream1.getvalue()
            failure = producer[producer_id].send(topic1, img_raw1)
            print('Producer is sending: '+ str(frame) + ' to GW '+ str(producer_id+2))
            frame = frame+1
            time.sleep(10)

    with picamera.PiCamera(resolution = (320, 180), framerate = 24) as camera:
#    with picamera.PiCamera(resolution = (1080, 920), framerate = 24) as camera:

        camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)


