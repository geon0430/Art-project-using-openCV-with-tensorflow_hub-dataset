import os
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import warnings
import argparse

warnings.filterwarnings("ignore", message="The value of the smallest subnormal for <class 'numpy.float32'> type is zero.")
warnings.filterwarnings("ignore", message="The value of the smallest subnormal for <class 'numpy.float64'> type is zero.")

class ArtMaker:
    def __init__(self, hub_handle='https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'):
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'  
        self.hub_module = hub.load(hub_handle)

    @staticmethod
    def read_image(path_to_img):
        try:
            max_dim = 640
            orig_img = cv2.imread(path_to_img)
            if orig_img is None:
                raise ValueError(f"Image not found at {path_to_img}")
            
            img_resized = cv2.resize(orig_img, (max_dim, max_dim))
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
            return img_rgb
        except Exception as e:
            print(f"Error loading image {path_to_img}: {e}")
            raise

    @staticmethod
    def preprocess(img_rgb):
        img_rgb = img_rgb.astype(np.float32) / 255.0 
        img_rgb = np.expand_dims(img_rgb, axis=0)    
        img_tensor = tf.convert_to_tensor(img_rgb, dtype=tf.float32)
        return img_tensor

    @staticmethod
    def postprocess(tensor):
        tensor = tensor.numpy()
        tensor = tensor * 255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
        img_resized = cv2.resize(tensor, (1920, 1080))
        output_data = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)
        return output_data

    @staticmethod
    def add_logo(output_data):
        logo_path = "/ArtMaker_StyleGan_Tensorflow/src/web/static/image/logo.jpg"
        logo_img = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
        if logo_img is None:
            raise FileNotFoundError("Logo image not found at the specified path.")
        logo_img = cv2.resize(logo_img, (160, 90))

        x_offset = output_data.shape[1] - 160
        y_offset = 0

        if logo_img.shape[2] == 4:
            overlay = logo_img[..., :3]
            mask = logo_img[..., 3:]
            background = output_data[y_offset:y_offset + 90, x_offset:x_offset + 160]
            combined = background * (1 - mask / 255.0) + overlay * (mask / 255.0)
            output_data[y_offset:y_offset + 90, x_offset:x_offset + 160] = combined
        else:
            output_data[y_offset:y_offset + 90, x_offset:x_offset + 160] = logo_img
        return output_data

    @staticmethod
    def get_next_output_path(output_dir, base_name="result", ext=".jpg"):
        index = 1
        while True:
            output_path = os.path.join(output_dir, f"{base_name}_{index}{ext}")
            if not os.path.exists(output_path):
                return output_path
            index += 1

    def make_art(self, content_image_path, style_image_path):
        output_dir = "/ArtMaker_StyleGan_Tensorflow/src/saved_images"
        output_path = self.get_next_output_path(output_dir)

        try:
            content_image = self.read_image(content_image_path)
            content_image = self.preprocess(content_image)
            
            style_image = self.read_image(style_image_path)
            style_image = self.preprocess(style_image)

            stylized_image = self.hub_module(tf.constant(content_image), tf.constant(style_image))[0]
            output_data = self.postprocess(stylized_image)
            output_data = self.add_logo(output_data)  

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            cv2.imwrite(output_path, output_data)
            return output_path
        
        except Exception as e:
            print(f"Error occurred: {e}")
            raise
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ArtMaker - Apply style transfer to images')
    parser.add_argument('--content', required=True, help='Path to the content image')
    parser.add_argument('--style', required=True, help='Path to the style image')
    args = parser.parse_args()

    art_maker = ArtMaker()
    output_path = art_maker.make_art(args.content, args.style)
    print(f"Image saved to {output_path}")