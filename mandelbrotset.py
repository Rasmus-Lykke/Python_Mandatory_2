from PIL import Image
import numpy as np
import time
import zoom_levels, mandelbrot_setup

""" SIMD Same instruction Multiple Data
    Numpy written in C, very fast, using multiple processors
    This Python file is made to create an image of the mandelbrot set. 
    You run the program simply by going to the file directory and then writing "python mandelbrotset.py" in the console
"""


zoom_level, file_name = mandelbrot_setup.userInput() # Assign the inputs to the two variables for later use


width, height = 800, 800 # The size of the image created in pixels

# Below is the 'Size' of the coordinate system, decreasing theese will zoom into the coordinatesystem
x_min = zoom_levels.zoom_list[zoom_level]["x_min"]
x_max = zoom_levels.zoom_list[zoom_level]["x_max"]
y_min = zoom_levels.zoom_list[zoom_level]["y_min"]
y_max = zoom_levels.zoom_list[zoom_level]["y_max"]

max_iter = zoom_levels.zoom_list[zoom_level]["max_iter"] # The number of iterations 

def create_mandelbrot():
    cmap = lambda value, v_min, v_max, p_min, p_max: p_min + (p_max - p_min) * ((value - v_min) / (v_max - v_min))

    C = np.zeros((width, height), dtype=np.complex_)
    Z = np.zeros((width, height), dtype=np.complex_)
    M = np.zeros((width, height, 3), dtype=np.uint8)

    """ Looping through each pixel given by the height and width variables """
    for cx in range(width):
        for cy in range(height):
            cr = cmap(cx, 0, width, x_min, x_max)
            ci = cmap(cy, 0, height, y_min, y_max)

            C[cx][cy] = cr + ci * 1j

    for i in range(max_iter):
        N = np.less(abs(Z), 2) # Picking out all the elements which are less than 2
        Z[N] = Z[N] * Z[N] + C[N] # Updateing Z, but still only the elements we need to deal with

        # The color depends on the number of iterations
        hue = int(i % 255)
        saturation = i % 255
        value = 255 if i < max_iter else abs(i % 256 * 1.5)
            
        M[N & (abs(Z) > 2)] = [hue, saturation, value] # Updateing the M matrix if the absolute value is bigger than 2 set the hue
    return M


def rotate_image(image):

    # rotate the image with expand=True, which makes the canvas
    # large enough to contain the entire rotated image.
    x = image.rotate(90, expand=True)

    # crop the rotated image to the size of the original image
    x = x.crop(box=(x.size[0]/2 - image.size[0]/2,
            x.size[1]/2 - image.size[1]/2,
            x.size[0]/2 + image.size[0]/2,
            x.size[1]/2 + image.size[1]/2))
    return x

start_time = time.time()
M = create_mandelbrot()
image = Image.fromarray(M, "RGB") # Creating the image from the "M" array and we use "T" for transpose
print(f"Time used: {(time.time() -start_time)}")
rotated_image = rotate_image(image)
rotated_image.save(file_name + '_numpy.png', 'PNG') # Saves the image to the current director
