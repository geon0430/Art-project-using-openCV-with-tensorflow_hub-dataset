import os
import cv2
import PIL.Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import argparse

class ArtMaker:
    def __init__(self, hub_handle='https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'):
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use GPU if available
        self.hub_module = hub.load(hub_handle)

    @staticmethod
    def tensor_to_image(tensor):
        tensor = tensor * 255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
        return PIL.Image.fromarray(tensor)

    @staticmethod
    def load_img(path_to_img):
        try:
            max_dim = 640
            img = tf.io.read_file(path_to_img)
            img = tf.image.decode_image(img, channels=3)
            img = tf.image.convert_image_dtype(img, tf.float32)

            shape = tf.cast(tf.shape(img)[:-1], tf.float32)
            long_dim = max(shape)
            scale = max_dim / long_dim

            new_shape = tf.cast(shape * scale, tf.int32)

            img = tf.image.resize(img, new_shape)
            img = img[tf.newaxis, :]
            return img
        except Exception as e:
            print(f"Error loading image {path_to_img}: {e}")
            raise

    def make_art(self, content_image_path, style_image_path):
        output_path = "./result/result.jpg"
        try:
            content_image = self.load_img(content_image_path)
            style_image = self.load_img(style_image_path)

            stylized_image = self.hub_module(tf.constant(content_image), tf.constant(style_image))[0]
            print("Saving stylized image...")

            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            self.tensor_to_image(stylized_image).save(output_path)
            print(f"Stylized image saved to {output_path}")
        except Exception as e:
            print(f"Error occurred: {e}")
