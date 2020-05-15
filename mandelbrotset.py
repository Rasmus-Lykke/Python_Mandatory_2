from PIL import Image
import numpy as np

""" SIMD Same instruction Multiple Data
    Numpy written in C, very fast, using multiple processors
    This Python file is made to create an image of the mandelbrot set. 
    You run the program simply by going to the file directory and then writing "python mandelbrotset.py" in the console
"""

def userInput():
    while True:
        try:
            print('Zoom level (0 - 5) 0 is original 5 i zoomed max in: ')
            user_input = int(input())       
        except ValueError:
            print("Not an integer! Try again.")
            continue
    
        try:
            print('What would you like to call the file? Leave empty for "default" \nIf filename already exists then it will be overwritten: ')
            file_name = input()
            if len(file_name) < 1:
                file_name = "default"    

        except ValueError:
            print("Error with the name, Try again.")
            continue

        else:
            return user_input, file_name
            break 

zoom_level, file_name = userInput() # Assign the inputs to the two variables for later use

original = {
    "x_min": -2.25,
    "x_max": 0.75,
    "y_min": -1.5,
    "y_max": 1.5,
    "max_iter": 500
}
first_level = {
    "x_min": -1.6875,
    "x_max": -0.5625,
    "y_min": -0.5,
    "y_max": 0.5,
    "max_iter": 200
}
second_level = {
    "x_min": -0.22,
    "x_max": -0.21,
    "y_min": -0.70 * 1.12,
    "y_max": -0.69 * 1.12,
    "max_iter": 400
}
third_level = {
    "x_min": -0.22,
    "x_max": -0.21,
    "y_min": -0.70,
    "y_max": -0.69,
    "max_iter": 400
}
fourth_level = {
    "x_min": -0.20,
    "x_max": -0.19,
    "y_min": -0.68,
    "y_max": -0.67,
    "max_iter": 800
}
fifth_level = {
    "x_min": -0.20,
    "x_max": -0.195,
    "y_min": -0.68,
    "y_max": -0.675,
    "max_iter": 1200
}

zoom_list = [original, first_level, second_level, third_level, fourth_level, fifth_level] # Add the dictionaries tho the zoom_list


width, height = 800, 800 # The size of the image created in pixels

# Below is the 'Size' of the coordinate system, decreasing theese will zoom into the coordinatesystem
x_min = zoom_list[zoom_level]["x_min"]
x_max = zoom_list[zoom_level]["x_max"]
y_min = zoom_list[zoom_level]["y_min"]
y_max = zoom_list[zoom_level]["y_max"]

max_iter = zoom_list[zoom_level]["max_iter"] # The number of iterations 

cmap = lambda value, v_min, v_max, p_min, p_max: p_min + (p_max - p_min) * ((value - v_min) / (v_max - v_min))

C = np.zeros((width, height), dtype=np.complex_)
Z = np.zeros((width, height), dtype=np.complex_)
M = np.zeros((width, height))

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
    hue = int(255 * i / max_iter)
    saturation = 255
    value = 255 if i < max_iter else 0
        
    M[N & (abs(Z) > 2)] = hue # Updateing the M matrix if the absolute value is bigger than 2 set the hue

image = Image.fromarray(np.uint8(M.T)) # Creating the image from the "M" array and we use "T" for transpose 
image.save(file_name + '.png', 'PNG') # Saves the image to the current directory







