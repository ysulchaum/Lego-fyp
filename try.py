import cv2
import numpy as np
import json

def is_yellow(pixel):
    # Define the range for yellow color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    
    # Convert the pixel to HSV
    hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)
    
    # Check if the pixel is within the yellow range
    return cv2.inRange(hsv_pixel, lower_yellow, upper_yellow) > 0

def create_matrix_from_image(image_path, unit_size):
    # Load the image
    image = cv2.imread(image_path)
    
    # Get the dimensions of the image
    height, width, _ = image.shape
    
    # Calculate the number of units in each dimension
    height_units = height // unit_size
    width_units = width // unit_size
    
    # Initialize the matrix with zeros
    matrix = np.zeros((height_units, width_units), dtype=int)
    
    # Iterate over each unit
    for i in range(height_units):
        for j in range(width_units):
            # Get the region of interest (ROI) for the current unit
            roi = image[i*unit_size:(i+1)*unit_size, j*unit_size:(j+1)*unit_size]
            
            # Check if any pixel in the ROI is yellow
            if any(is_yellow(pixel) for row in roi for pixel in row):
                matrix[i, j] = 1
    
    return matrix

def resized_image(o_image, n_height, n_width):
    # Load the image
    image = cv2.imread(o_image)

    # Resize the image
    resized_image = cv2.resize(image, (n_width, n_height))

    # Save the resized image
    cv2.imwrite(f'resized_{o_image}', resized_image)

    return f'resized_{o_image}'




#######################################################################################

def voxelize_brick(tensor):
    voxel_list = []
    T = tensor.shape
    for d in range(T[0]):
        for h in range(T[1]):
            for w in range(T[2]):
                if tensor[d, h, w]:
                    voxel_list.append([-(T[2]-w)*4//2+2*(w+1), 2+h*4, -(T[0]-d)*4//2+2*(d+1)])
                    #voxel_list.append([w*4-8, 2+h*4, d*4-8])
    return voxel_list


def open_json():
    with open('voxel_data.json', 'w') as json_file:
        json.dump({}, json_file, indent=2)  # Initialize with an empty list

def write_json(new_data, filename='voxel_data.json'):
    with open(filename, 'r+') as file:
        # Load existing data into a dictionary
        file_data = json.load(file)
        # Update the dictionary with new data
        file_data.update(new_data)
        # Set file's current position at offset
        file.seek(0)
        # Convert back to JSON
        json.dump(file_data, file, indent=2, separators=(', ', ': '))


def resized_image(o_image, n_height, n_width):
    # Load the image
    image = cv2.imread(o_image)

    # Resize the image
    resized_image = cv2.resize(image, (n_width, n_height))

    # Save the resized image
    cv2.imwrite(f'resized_{o_image}', resized_image)

    return f'resized_{o_image}'


###################################################################################

def images_to_tensor_to_voxel(brick_code = None): # to be continue 
    with open("bricksize.json", 'r') as brick_size:
        brick_data = json.load(brick_size)

    open_json()

    for ID in brick_data["brick_size"]: 
        brick_ID = ID[0]
        image_path = f'{brick_ID}.png'
        unit_size = 4

        w = ID[1]
        h = ID[3]
        d = ID[2]

        try:
            test = resized_image(image_path, h, w)
        except:
            print(f'{brick_ID}.png does not exist')
            continue

        # Create the matrix from the image
        matrix = create_matrix_from_image(test, unit_size)
        tensor = np.tile(matrix, (int(d/4), 1, 1))

        if brick_code == brick_ID:
            print(tensor)

        # voxel_data = {brick_ID: voxelize_brick(d, w, h, tensor)}
        voxel_data = {brick_ID: voxelize_brick(tensor)}
        write_json(voxel_data)

#######################################################


images_to_tensor_to_voxel('3024')

