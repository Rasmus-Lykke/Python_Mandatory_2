from PIL import Image, ImageDraw
import time
import zoom_levels, mandelbrot_setup

t0 = time.time()

MAX_ITER = 100

zoom_level, file_name = mandelbrot_setup.userInput()

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z * z + c
        n += 1
    return n


# Image size (pixels) // Pixel size of the picture
WIDTH = 800
HEIGHT = 800

n = 1

# Plot window // Adjust this for panning and zooming // Imaginary and Real parts
# Below is the 'Size' of the coordinate system, decreasing theese will zoom into the coordinatesystem
x_min = zoom_levels.zoom_list[zoom_level]["x_min"]
x_max = zoom_levels.zoom_list[zoom_level]["x_max"]
y_min = zoom_levels.zoom_list[zoom_level]["y_min"]
y_max = zoom_levels.zoom_list[zoom_level]["y_max"]

image = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(image)

""" Iterating through each pixel in the image"""
for x in range(WIDTH):
    for y in range(HEIGHT):
        # Convert pixel coordinate to complex number
        coordinate = complex(x_min + (x / WIDTH) * (x_max - x_min),
                             y_min + (y / HEIGHT) * (y_max - y_min))

        # Compute the number of iterations
        m = mandelbrot(coordinate)

        # The color depends on the number of iterations
        hue = int(255 * m / MAX_ITER)
        saturation = 255
        value = 255 if m < MAX_ITER else 0

        # Plot the point
        draw.point([x, y], (hue, saturation, value))

image.convert('RGB').save(file_name + '_iterative.png', 'PNG')

t1 = time.time()
print("Time: " + str(t1 - t0)[:4])


