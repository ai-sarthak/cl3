import tensorflow as tf
import tensorflow_hub as hub 
import matplotlib.pyplot as plt

def load_image(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, dtype=tf.float32)
    img = img[tf.newaxis,:]
    return img

def show_image(image):
    image = tf.squeeze(image, axis=0)
    plt.imshow(image)
    plt.title("Stylized Image")
    
content_image = load_image("content.jpg")
style_image = load_image("style.jpg")

hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

styled_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

show_image(styled_image)
plt.show()