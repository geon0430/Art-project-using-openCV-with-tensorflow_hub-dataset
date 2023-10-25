import os
import cv2
import PIL.Image
import numpy as np
import argparse
import tensorflow as tf
import tensorflow_hub as hub

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Disable GPU
hub_handle_2 = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle_2)

def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

def load_img(path_to_img):
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

def makeArt(content_image_path, style_image_path, output_path):
    try:
        content_image = load_img(content_image_path)
        style_image = load_img(style_image_path)

        stylized_image = hub_module(tf.constant(content_image), tf.constant(style_image))[0]
        print("Saving stylized image...")  # 로그 메시지 추가

        # Ensure the 'results' directory exists
        if not os.path.exists('results'):
            os.makedirs('results')

        # Save the image to the 'results' directory
        tensor_to_image(stylized_image).save(os.path.join('results', output_path))
        print(f"Stylized image saved to results/{output_path}")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    print("Script started...")  # 로그 메시지 추가
    parser = argparse.ArgumentParser(description="Art Making with TensorFlow Hub")
    parser.add_argument("--content", type=str, required=True, help="Path to the content image.")
    parser.add_argument("--style", type=str, required=True, help="Path to the style image.")
    parser.add_argument("--output", type=str, default="output.jpg", help="Path to save the stylized image.")
    args = parser.parse_args()

    makeArt(args.content, args.style, args.output)
