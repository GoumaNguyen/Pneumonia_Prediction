import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from PIL import Image
from skimage.transform import resize
from skimage import measure
import matplotlib.patches as patches
from io import BytesIO
import base64

def load_image(file):
    img = Image.open(file)
    img = np.array(img)
    return img

def process(img, image_size=256):
    if len(img.shape) == 2:
        img = np.expand_dims(img, axis=-1)
    elif len(img.shape) == 3 and img.shape[2] == 3:
        pass
    else:
        raise ValueError("Unsupported image shape: {}".format(img.shape))

    img = resize(img, (image_size, image_size), mode='reflect', anti_aliasing=True)

    if len(img.shape) == 2:
        img = np.expand_dims(img, axis=-1)

    return img

def predict_and_plot(model, img):
    processed_img = process(img)
    pred = model.predict(np.expand_dims(processed_img, axis=0))[0]

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.imshow(processed_img[:, :, 0], cmap='gray')

    comp = pred[:, :, 0] > 0.5
    comp = measure.label(comp)

    label = -1
    if len(np.unique(comp)) == 1:
        label = 0
    else:
        label = 1
        for region in measure.regionprops(comp):
            y, x, y2, x2 = region.bbox
            height = y2 - y
            width = x2 - x
            ax.add_patch(patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='none'))

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return label, image_base64
