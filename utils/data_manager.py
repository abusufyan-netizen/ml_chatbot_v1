import os, time
from PIL import Image, ImageOps
import numpy as np

BASE = os.path.dirname(os.path.dirname(__file__))
FEEDBACK_DIR = os.path.join(BASE, 'logs', 'feedback')
os.makedirs(FEEDBACK_DIR, exist_ok=True)

def preprocess_pil(pil_img):
    img = pil_img.convert('L')
    img = ImageOps.invert(img)
    img.thumbnail((20,20), Image.LANCZOS)
    new_img = Image.new('L', (28,28), color=0)
    new_img.paste(img, ((28-img.width)//2, (28-img.height)//2))
    arr = np.array(new_img).astype('float32')/255.0
    arr = arr.reshape(1,28,28,1)
    return arr, new_img

def save_feedback_image(pil_img, label):
    ts = int(time.time()*1000)
    fname = f'feedback_{label}_{ts}.png'
    path = os.path.join(FEEDBACK_DIR, fname)
    pil_img.save(path)
    return path

def load_model_safe(path):
    try:
        import tensorflow as tf
        if os.path.exists(path):
            return tf.keras.models.load_model(path)
        return None
    except Exception:
        return None
