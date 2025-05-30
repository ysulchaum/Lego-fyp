import cv2
import numpy as np
import json


def is_black(pixel):
    # Define the range for black color in BGR
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([50, 50, 50])

    # Check if the pixel is within the black range
    return np.all(pixel >= lower_black) and np.all(pixel <= upper_black)


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
            roi = image[i*unit_size:(i+1)*unit_size,
                        j*unit_size:(j+1)*unit_size]

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


def create_matrix_from_image_stud(image_path, unit_size):
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
            roi = image[i*unit_size:(i+1)*unit_size,
                        j*unit_size:(j+1)*unit_size]

            # Check if any pixel in the ROI is yellow
            if any(is_black(pixel) for row in roi for pixel in row):
                matrix[i, j] = 1

    return matrix


def indicate_stud(png):
    image = cv2.imread(png)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                               param1=50, param2=30, minRadius=30, maxRadius=80)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            # print(r)
            cv2.rectangle(image, (x - r+3, y - r+3),
                          (x + r-3, y + r-3), (0, 0, 0), -1)

    # cv2.imshow("output", image)
    # cv2.waitKey(0)
    cv2.imwrite(f'indicated_{png}', image)
    return f'indicated_{png}'


# compare the stud_matrix and tensor and match the coor.
def stud_positions(tensor, matrix):
    positions = []
    T = tensor.shape
    # matrix_shape = matrix.shape
    # print([T[x] for x in range(3)])
    for D in range(T[0]):
        for H in range(T[1]):
            for W in range(T[2]):
                if tensor[D, H, W] == matrix[D, W] == 1:
                    if H == 0 or tensor[D, H-1, W] != 1:
                        positions.append([-(T[2]-W)*4//2+2*(W+1), 2+H*4, -(T[0]-D)*4//2+2*(D+1)])
    return positions


def tude_positions(tensor):
    positions = []
    T = tensor.shape
    for D in range(1, T[0]-1):
        for H in range(T[1]):
            for W in range(1, T[2]-1):
                if (D % 5 in {1, 2, 3}) and (W % 5 in {1, 2, 3}):
                    if tensor[D, H, W] == 1:
                        if H == T[1] - 1 or tensor[D, H + 1, W] != 1:
                            positions.append([-(T[2]-W)*4//2+2*(W+1), 2+H*4, -(T[0]-D)*4//2+2*(D+1)])
    return positions


def tude_test(tensor):
    T = tensor.shape
    positions = np.zeros((T[0], T[2]), dtype=int)
    for D in range(1, T[0]-1):
        for H in range(T[1]):
            for W in range(1, T[2]-1):
                if (D % 5 in {1, 2, 3}) and (W % 5 in {1, 2, 3}):
                    if tensor[D, H, W] == 1:
                        if H == T[1] - 1 or tensor[D, H + 1, W] != 1:
                            positions[D, W] = 1
    return positions


def open_json():
    with open('stud_data.json', 'w') as json_file:
        json.dump({}, json_file, indent=2)  # Initialize with an empty list


def write_json(new_data, filename='stud_data.json'):
    with open(filename, 'r+') as file:
        # Load existing data into a dictionary
        file_data = json.load(file)
        # Update the dictionary with new data
        file_data.update(new_data)
        # Set file's current position at offset
        file.seek(0)
        # Convert back to JSON
        json.dump(file_data, file, indent=2, separators=(', ', ': '))


def images_to_tensor_to_stud_voxel(brick_code=None): 
    with open("bricksize.json", 'r') as brick_size:
        brick_data = json.load(brick_size)

    open_json()

    for ID in brick_data["brick_size"]:
        brick_ID = ID[0]
        unit_size = 4

        w = ID[1]
        h = ID[3]
        d = ID[2]

        try:
            img = indicate_stud(f'{brick_ID}.png')
            resized_image(img, d, w)
            stud_matrix = create_matrix_from_image_stud(
                f'resized_indicated_{brick_ID}.png', 4)
            #print(stud_matrix)
        except:
            # print(f'{brick_ID}.png does not exist')
            continue

        # Create the matrix from the image

        matrix = create_matrix_from_image(
            r"C:\sem1_fyp\brick cross section\resized_"+brick_ID+".png", unit_size)
        tensor = np.tile(matrix, (int(d/4), 1, 1))

        if brick_code == brick_ID:
            print("The whole tensor: ")
            print(tensor)

        # voxel_data = {brick_ID: voxelize_brick(d, w, h, tensor)}
        try:
            voxel_data = {brick_ID: {"stud_voxels": stud_positions(tensor, stud_matrix),
                                     "tube_voxels": tude_positions(tensor),
                                     "stud_voxel_augmented": stud_positions(tensor, stud_matrix),
                                     "tube_voxel_augmented": tude_positions(tensor)}}
            if brick_code == brick_ID:
                print("Top: ")
                print(stud_matrix)
                print("Bottom: ")
                print(tude_test(tensor))
            write_json(voxel_data)
        except:
            continue
##############


images_to_tensor_to_stud_voxel("3040a")


# print(create_matrix_from_image(f'resized_indicated_{id}.png', 4))
