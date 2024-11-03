import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json


all = "brick_voxel.json"
some = "voxel_data.json"

with open(some, 'r') as brick_size:
        brick_data = json.load(brick_size)

ID = "3455"
# Coordinates of the voxels
voxels = [item for item in brick_data[ID]]

# Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract x, y, z coordinates from the voxels list
x = [v[0] for v in voxels]
y = [v[1] for v in voxels]
z = [v[2] for v in voxels]

# Plot the voxels
ax.scatter(x, y, z)

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()
