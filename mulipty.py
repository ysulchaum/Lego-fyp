import numpy as np
import json


def transformation_rotation(rot, coor):
    # Ensure the matrices have the correct shapes
    if rot.shape != (3, 3) or coor.shape != (3, 1):
        raise ValueError(
            "The shapes of the matrices must be (3, 3) and (3, 1) respectively.")

    # Perform the matrix multiplication
    result = np.dot(rot, coor)
    return result


def transformation_position(pos, coor):
    for x in range(len(coor)):
        coor[x] = coor[x] + pos[x]
    return coor
    

def open_json(num = ''):
    with open(f'brick_model{num}.json', 'w') as json_file:
        json.dump({}, json_file, indent=2)  # Initialize with an empty list
        

def write_json(new_data, num = ''):
    with open(f'brick_model{num}.json', 'r+') as file:
        # Load existing data into a dictionary
        file_data = json.load(file)
        # Update the dictionary with new data
        file_data.update(new_data)
        # Set file's current position at offset
        file.seek(0)
        # Convert back to JSON
        json.dump(file_data, file, indent=2, separators=(', ', ': '))

def read_ldr_file(file_content):
    data = []
    lines = file_content.splitlines()
    for line in lines:
        if line.startswith('1'):
            parts = line.split()
            # Convert the parts to appropriate types and append to data
            data.append([int(parts[0]), int(parts[1])] + [float(x) for x in parts[2:14]] + [parts[14]])
    return np.array(data)
   

def brick_transformation(num):
    with open("voxel_data.json", 'r') as brick_coor:
            brick_data = json.load(brick_coor)

    open_json(num)

    with open("transformation.ldr", 'r') as brick_trans:
        brick_trans_data = brick_trans.read()

    matrix = read_ldr_file(brick_trans_data)

    for x in range(len(matrix)):
        id = matrix[x,14]
        id = id.replace('.dat', '')

        pos = matrix[x, 2:5].astype(float).astype(int)
        rot = matrix[x, 5:14].astype(float).astype(int)

        one_coor = brick_data[id]
        after_trans = []

        for coor in one_coor:
            tp = transformation_position(pos, np.reshape(coor,(3,1)))
            finish_trans = transformation_rotation(np.reshape(rot,(3,3)), tp)
            after_trans.append(np.reshape(finish_trans, (1, 3)))

        after_trans_list = [arr.tolist()[0] for arr in after_trans]


        voxel_data = {id+f"-{x}": after_trans_list}
        write_json(voxel_data, num)

        #print(matrix)

def stud_tube_transformation(num): #to be continus
    with open("stud_data.json", 'r') as brick_coor:
        brick_data = json.load(brick_coor)

    open_json(num)

    with open("transformation.ldr", 'r') as brick_trans:
        brick_trans_data = brick_trans.read()

    matrix = read_ldr_file(brick_trans_data)

    for x in range(len(matrix)):
        id = matrix[x,14]
        id = id.replace('.dat', '')

        pos = matrix[x, 2:5].astype(float).astype(int)
        rot = matrix[x, 5:14].astype(float).astype(int)

        one_coor = brick_data[id]
        after_trans = []

        for coor in one_coor:
            tp = transformation_position(pos, np.reshape(coor,(3,1)))
            finish_trans = transformation_rotation(np.reshape(rot,(3,3)), tp)
            after_trans.append(np.reshape(finish_trans, (1, 3)))

        after_trans_list = [arr.tolist()[0] for arr in after_trans]


        voxel_data = {id+f"-{x}": after_trans_list}
        write_json(voxel_data, num)

        #print(matrix)


brick_transformation(1)
