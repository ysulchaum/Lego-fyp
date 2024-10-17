import json

def voxelize_brick(n, m, r):
    voxel_list = []
    for x in range(-n//2 + 2, n//2 + 1, 4):
        for y in range(2, r + 1, 4):
            for z in range(-m//2 + 2, m//2 + 1, 4):
                voxel_list.append([x, y, z])
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

open_json()
voxel_data = {"3024": voxelize_brick(20, 20, 8)}
write_json(voxel_data)





# Test
#n, m, r = 20, 20, 8
#voxel_data = voxelize_brick(n, m, r)

# Save JSON data to a file
#with open('voxel_data.json', 'w') as json_file:
#    json.dump(voxel_data, json_file, indent=2, separators=(', ', ': '))

print("JSON file 'voxel_data.json' has been created.")
