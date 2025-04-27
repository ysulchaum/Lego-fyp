import numpy as np
import json
import os
from printtensor import create_box_with_frame, print_model, view_numpyM

def id_mapping(id):
    with open("mapping.json", 'r') as data:
        brick_data = json.load(data)
        
    for ID in brick_data["brick_size"]: 
        brick_ID = ID[0]
        if id == brick_ID:
            return ID[4]

def view_numpy(f="brick_model1.npy"):
    array = np.load(f, allow_pickle=True)
    #print(array)
    #np.set_printoptions(threshold=np.inf)
    print(array[:10]) # Print the first 10 elements
    print("Array size:", array.shape)


def store_matrix(brick, stud, tube, brickid, studid, tubeid):
    # Convert the list of coordinates to a NumPy array
    brick_array = np.array(brick)
    stud_array = np.array(stud)
    tube_array = np.array(tube)

    # Combine all voxel coordinates to find the bounding box
    all_voxels = np.vstack([brick_array, stud_array, tube_array])
    min_coords = all_voxels.min(axis=0)  # [min_x, min_y, min_z]
    max_coords = all_voxels.max(axis=0)  # [max_x, max_y, max_z]

    # Calculate the size of the bounding box in voxel units (divide by 4 due to scaling)
    size = (max_coords - min_coords) // 4 + 1  # Add 1 to include the max coordinate
    size_x, size_y, size_z = size

    # Check if the model fits within the fixed shape (64, 32, 64) -> (64, 64, 32)
    if size_x > 64 or size_y > 64 or size_z > 64:
        raise ValueError(f"Model dimensions {size_x}x{size_y}x{size_z} exceed fixed tensor shape 64x32x64")

    # Create a 3D matrix with the fixed shape
    T = np.zeros((64, 64, 64), dtype=object)

    # Normalize coordinates by subtracting the minimum and scaling
    for (x, y, z), id in zip(brick_array, brickid): 
        idx_x = (x - min_coords[0]) // 4
        idx_y = (y - min_coords[1]) // 4
        idx_z = (z - min_coords[2]) // 4
        T[idx_x, idx_y, idx_z] = id_mapping(id)
    
    for (x, y, z), id in zip(stud_array, studid):  # Studs marked with 42
        idx_x = (x - min_coords[0]) // 4
        idx_y = (y - min_coords[1]) // 4
        idx_z = (z - min_coords[2]) // 4
        T[idx_x, idx_y, idx_z] = 42
        
    for (x, y, z), id in zip(tube_array, tubeid):  # Tubes marked with 43
        idx_x = (x - min_coords[0]) // 4
        idx_y = (y - min_coords[1]) // 4
        idx_z = (z - min_coords[2]) // 4
        T[idx_x, idx_y, idx_z] = 43
        
    return T
    
def tensor(model=r"C:\sem1_fyp\jsonDataSet\brick_model1.json"): # "C:\sem1_fyp\transf\brick_model1.json"
    with open(model, 'r') as data:
        brick_data = json.load(data)

    brick_list = []
    stud_list = []
    tube_list = []
    
    brick_id = []
    stud_id = []
    tube_id = []
    for num in range(len(brick_data)):
        brick_coor = brick_data[f"{num}"]["brick_voxels"]
        brick_list += brick_coor
        id = brick_data[f"{num}"]["brick"]
        brick_id += len(brick_coor) * [id]
        
        brick_coor = brick_data[f"{num}"]["stud_voxels"]
        stud_list += brick_coor
        id = brick_data[f"{num}"]["brick"]
        stud_id += len(brick_coor) * [id]
        
        brick_coor = brick_data[f"{num}"]["tube_voxels"]
        tube_list += brick_coor
        id = brick_data[f"{num}"]["brick"]
        tube_id += len(brick_coor) * [id]

    return store_matrix(brick_list, stud_list, tube_list, brick_id, stud_id, tube_id)


def covert_all(directory_path=r"C:\sem1_fyp\jsonDataSet", output_directory=r"C:\sem1_fyp\numpyDataSet"):
    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    all_items = os.listdir(directory_path)
    file_names = [file for file in all_items if os.path.isfile(
        os.path.join(directory_path, file))]
    print(f"Number of files: {len(file_names)}")
    print(f"Name of files: {file_names}")

    for jsonFile in file_names:
        try:
            full_json_path = os.path.join(directory_path, jsonFile)
            full_output_path = os.path.join(output_directory, changeName(jsonFile))
            np.save(full_output_path, tensor(full_json_path))
            print(f"Processed {jsonFile} successfully.")
        except Exception as e:
            print(f"{jsonFile} has error: {e}")

        
def changeName(filename):
    # Split the filename at the '.' and take the first part (base name)
    return filename.split('.')[0]


#covert_all()

#print_model(tensor())

#view_numpy(r"C:\sem1_fyp\numpyDataSet\brick_model1.npy")

#view_numpyM(r"C:\sem1_fyp\numpyDataSet\brick_model1.npy")

#view_numpyM("Result/occupancy_map_5.npy")

view_numpy()