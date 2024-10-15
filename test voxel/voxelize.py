import json

def voxelize_brick(n, m, r):
    voxel_list = []
    for x in range(-n//2 + 2, n//2 + 1, 4):
        for y in range(2, r + 1, 4):
            for z in range(-m//2 + 2, m//2 + 1, 4):
                voxel_list.append([x, y, z])
    return {"3024": voxel_list}

# Test
n, m, r = 20, 20, 8
voxel_data = voxelize_brick(n, m, r)

# Save JSON data to a file
with open('voxel_data.json', 'w') as json_file:
    json.dump(voxel_data, json_file, indent=2, separators=(', ', ': '))

print("JSON file 'voxel_data.json' has been created.")
