import os
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from base_camera import BaseCamera

model = hub.load('https://tfhub.dev/google/movenet/singlepose/thunder/3')
movenet = model.signatures['serving_default']

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        cap = cv2.VideoCapture(Camera.video_source)
        if not cap.isOpened():
            raise RuntimeError('Could not start camera.')

        success, img = cap.read()

        if not success:
            print('Error reding frame')
            quit()

        y, x, _ = img.shape

        while success:
        # A frame of video or an image, represented as an int32 tensor of shape: 256x256x3. Channels order: RGB with values in [0, 255].
            tf_img = cv2.resize(img, (256,256))
            tf_img = cv2.cvtColor(tf_img, cv2.COLOR_BGR2RGB)
            tf_img = np.asarray(tf_img)
            tf_img = np.expand_dims(tf_img,axis=0)

            # Resize and pad the image to keep the aspect ratio and fit the expected size.
            image = tf.cast(tf_img, dtype=tf.int32)

            # Run model inference.
            outputs = movenet(image)
            # Output is a [1, 1, 17, 3] tensor.
            keypoints = outputs['output_0']

            # iterate through keypoints
            for k in keypoints[0,0,:,:]:
                # Converts to numpy array
                k = k.numpy()

                # Checks confidence for keypoint
                if k[2] > 0.3:
                    # The first two channels of the last dimension represents the yx coordinates (normalized to image frame, i.e. range in [0.0, 1.0]) of the 17 keypoints
                    yc = int(k[0] * y)
                    xc = int(k[1] * x)

                    # Draws a circle on the image for each keypoint
                    img = cv2.circle(img, (xc, yc), 2, (0, 255, 0), 5)
            
            # Shows image
            yield cv2.imencode('.jpg', img)[1].tobytes()

            # Waits for the next frame, checks if q was pressed to quit
            if cv2.waitKey(1) == ord("q"):
                break

            # Reads next frame
            success, img = cap.read()
            
