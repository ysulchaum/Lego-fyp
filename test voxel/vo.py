import numpy as np
import json

with open('3024.json', 'r') as brick:
    brick_data = json.load(brick)

dim = (int(brick_data["Dimension"][0]/4), int(brick_data["Dimension"][2]/4), int(brick_data["Dimension"][1]/4))

def voxelize_brick(dimensions):
    # Define grid size (e.g., 10x10x10 for simplicity)
    grid_size = (10, 10, 10)
    
    # Create an empty voxel grid
    voxel_grid = np.zeros(grid_size, dtype=int)

    # Define brick dimensions and position (x, y, z)
    x, y, z = dimensions  # dimensions should be a tuple (width, depth, height)
    
    # Fill the voxel grid based on brick dimensions
    # Assuming the brick starts at the origin (0,0,0)
    voxel_grid[0:x, 0:y, 0:z] = 1  # Mark as filled
    
    return voxel_grid

# Test
voxel_grid = voxelize_brick(dim)

print(voxel_grid)
