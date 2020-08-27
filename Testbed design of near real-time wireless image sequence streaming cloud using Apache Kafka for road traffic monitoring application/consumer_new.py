# At consumer node
# This program is written by Aung Myo Htut from Chulalongkorn University
from kafka import KafkaConsumer
from PIL import Image
import io
import cv2
import numpy 

# instantiated kafka consumer
consumer = KafkaConsumer('pi1', group_id='gateway', bootstrap_servers=['10.0.0.8:9092'])

def image_viewer():

    for msg in consumer:
        key= cv2.waitKey(1) & 0xFF
        image = Image.open(io.BytesIO(msg[6])).convert('RGB')
        img = numpy.array(image)
        cv2.imshow('Pi1', img)
        
        if key == ord("q"):
            break

if __name__ == '__main__':
    image_viewer()

