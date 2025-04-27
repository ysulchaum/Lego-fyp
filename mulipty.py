import numpy as np
import json
import os


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


# Updated open_json to use the output directory
def open_json(num='', output_directory=r"C:\sem1_fyp\jsonDataSet"):
    os.makedirs(output_directory, exist_ok=True)
    file_path = os.path.join(output_directory, f'brick_model{num}.json')
    if not os.path.exists(file_path):  # Only create if it doesn't exist
        with open(file_path, 'w') as json_file:
            json.dump({}, json_file, indent=2)


# Updated write_json (same as before but ensuring consistency)
def write_json(new_data, num='', output_directory=r"C:\sem1_fyp\jsonDataSet"):
    os.makedirs(output_directory, exist_ok=True)
    file_path = os.path.join(output_directory, f'brick_model{num}.json')

    # If file exists, update it; otherwise, create it
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                file_data = json.load(file)
        except json.JSONDecodeError:  # Handle empty or corrupt file
            file_data = {}
    else:
        file_data = {}

    file_data.update(new_data)
    with open(file_path, 'w') as file:
        json.dump(file_data, file, indent=2, separators=(', ', ': '))


def read_ldr_file(file_content):
    data = []
    lines = file_content.splitlines()
    for line in lines:
        if line.startswith('1'):
            parts = line.split()
            # Convert the parts to appropriate types and append to data
            data.append([int(parts[0]), int(parts[1])] + [float(x)
                        for x in parts[2:14]] + [parts[14]])
    return np.array(data)


def special_trans_rot(id, coor):  # some bricks are in wrong rotation, which needs to fix
    rot_matrix = np.array([[0, 0, 1],
                           [0, 1, 0],
                           [-1, 0, 0]])
    special_brick_list = ["54200", "5404", "3573", "92946", "3044a", "3040a"]
    if id in special_brick_list:
        return transformation_rotation(rot_matrix, coor)
    return coor


def special_trans_pos(id, coor):  # some bricks are in wrong position, which needs to fix
    pos_move_up4 = np.array([[0], [-16], [0]])
    pos_move_up18 = np.array([[0], [-72], [0]])
    pos_move_up8 = np.array([[0], [-32], [0]])
    special_brick_list2 = ["54200", "92946", "5404"]
    special_brick_list3 = ["5260", "5259"]
    special_brick_list4 = ["20309"]
    if id in special_brick_list2:
        return transformation_position(pos_move_up4, coor)
    if id in special_brick_list3:
        return transformation_position(pos_move_up18, coor)
    if id in special_brick_list4:
        return transformation_position(pos_move_up8, coor)
    return coor


def brick_transformation(num, model_name, output_directory=r"C:\sem1_fyp\jsonDataSet"):
    with open(r"C:\sem1_fyp\brick cross section\voxel_data.json", 'r') as data:
        brick_data = json.load(data)
    with open(r"C:\sem1_fyp\cp\stud_data.json", 'r') as data2:
        stud_tube_data = json.load(data2)

    open_json(num, output_directory)  # Pass output_directory
    with open(model_name, 'r') as brick_trans:
        brick_trans_data = brick_trans.read()

    matrix = read_ldr_file(brick_trans_data)
    # print(matrix)

    for x in range(len(matrix)):
        id = matrix[x, 14].replace('.dat', '')
        pos = matrix[x, 2:5].astype(float).astype(int)
        rot = matrix[x, 5:14].astype(float).astype(int)

        brick_coor = brick_data[id]
        stud_coor = stud_tube_data[id]["stud_voxels"]
        tube_coor = stud_tube_data[id]["tube_voxels"]

        brick_trans = []
        stud_trans = []
        tube_trans = []

        for coor in brick_coor:
            finish_trans = transformation_rotation(np.reshape(
                rot, (3, 3)), special_trans_rot(id, np.reshape(coor, (3, 1))))
            tp = transformation_position(
                pos, special_trans_pos(id, finish_trans))
            brick_trans.append(np.reshape(tp, (1, 3)))

        for coor in stud_coor:
            finish_trans = transformation_rotation(np.reshape(
                rot, (3, 3)), special_trans_rot(id, np.reshape(coor, (3, 1))))
            tp = transformation_position(
                pos, special_trans_pos(id, finish_trans))
            stud_trans.append(np.reshape(tp, (1, 3)))

        for coor in tube_coor:
            finish_trans = transformation_rotation(np.reshape(
                rot, (3, 3)), special_trans_rot(id, np.reshape(coor, (3, 1))))
            tp = transformation_position(
                pos, special_trans_pos(id, finish_trans))
            tube_trans.append(np.reshape(tp, (1, 3)))

        brick_trans_list = [arr.tolist()[0] for arr in brick_trans]
        stud_trans_list = [arr.tolist()[0] for arr in stud_trans]
        tube_trans_list = [arr.tolist()[0] for arr in tube_trans]

        voxel_data = {f"{x}": {"brick": id,
                               "brick_voxels": brick_trans_list,
                               "stud_voxels": stud_trans_list,
                               "tube_voxels": tube_trans_list}}
        write_json(voxel_data, num, output_directory)  # Pass output_directory


def covert_all(directory_path=r'C:\sem1_fyp\ldrDataSet', output_directory=r"C:\sem1_fyp\jsonDataSet"):
    all_items = os.listdir(directory_path)
    file_names = [file for file in all_items if os.path.isfile(
        os.path.join(directory_path, file))]
    print(f"Number of files: {len(file_names)}")
    print(f"Name of files: {file_names}")
    count = 1

    for ldrFile in file_names:
        try:
            full_ldr_path = os.path.join(directory_path, ldrFile)
            brick_transformation(count, full_ldr_path, output_directory)
            print(f"Processed {ldrFile} successfully.")
        except Exception as e:
            print(f"{ldrFile} has error: {e}")
        count += 1


# brick_transformation(1)
covert_all()
