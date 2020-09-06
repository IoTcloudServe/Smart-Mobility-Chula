# At camera node
# This program is written by Aung Myo Htut from Chulalongkorn University
import io
import time
import picamera
from PIL import Image
from kafka import SimpleProducer, KafkaClient

# instantiated kafka producer
kafka = KafkaClient('10.0.0.8:9092')
producer = SimpleProducer(kafka)
topic = 'pi1'
frame_number = 0

while(True):

    def outputs():
        # caprutre and send to broker in every 0.2 sec
        with picamera.PiCamera() as camera:
            stream1 = io.BytesIO()
            yield stream1
            img = stream1.getvalue()
            producer.send_messages(topic, img)
            frame_number = frame_number + 1
            print('Producer is sending frame number:', frame_number)
            time.sleep(0.2)
            
    with picamera.PiCamera(resolution = (320, 180), framerate = 24) as camera:
        camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
