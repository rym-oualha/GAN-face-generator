# import the necessary packages
import numpy as np
from tensorflow.keras.models import model_from_json
from PIL import Image
from tensorflow.keras.layers import Input, Dense, Reshape, Conv2D, Conv2DTranspose, LeakyReLU
from tensorflow.keras.models import Model

# Define the generator architecture function

def create_generator():
    LATENT_DIM = 32
    CHANNELS = 3
    gen_input = Input(shape=(LATENT_DIM, ))

    x = Dense(128 * 16 * 16)(gen_input)
    x = LeakyReLU()(x)
    x = Reshape((16, 16, 128))(x)

    x = Conv2D(256, 5, padding='same')(x)
    x = LeakyReLU()(x)

    x = Conv2DTranspose(256, 4, strides=2, padding='same')(x)
    x = LeakyReLU()(x)

    x = Conv2DTranspose(256, 4, strides=2, padding='same')(x)
    x = LeakyReLU()(x)

    x = Conv2DTranspose(256, 4, strides=2, padding='same')(x)
    x = LeakyReLU()(x)

    x = Conv2D(512, 5, padding='same')(x)
    x = LeakyReLU()(x)
    x = Conv2D(512, 5, padding='same')(x)
    x = LeakyReLU()(x)
    x = Conv2D(CHANNELS, 7, activation='tanh', padding='same')(x)

    generator = Model(gen_input, x)
    return generator


# Load the model architecture from JSON
with open('model.json', 'r') as json_file:
    loaded_model_json = json_file.read()
    loaded_generator = model_from_json(loaded_model_json, custom_objects={'LeakyReLU': LeakyReLU})

# Load the saved weights into the generator model
loaded_generator.load_weights('model.h5')

# Generate new faces
num_faces_to_generate = 1  # Change this if you want to generate more faces
latent_dim = 32  # Latent dimension of your GAN

# Generate random noise as input for the generator
noise = np.random.normal(0, 1, (num_faces_to_generate, latent_dim))

# Generate faces using the generator model
generated_faces = loaded_generator.predict(noise)

# Rescale pixel values from [-1, 1] to [0, 255]
generated_faces = (255 * (generated_faces + 1) / 2).astype(np.uint8)

# Save the generated faces
for i in range(num_faces_to_generate):
    im = Image.fromarray(generated_faces[i])
    im.save(f'generated_face_{i}.png')

print(f'{num_faces_to_generate} faces generated and saved.')