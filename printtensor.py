import numpy as np
import open3d as o3d
import os
import glob
import time

# Ensure the output directory exists
output_dir = "imageBad"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to create a box with a frame (no diagonals)
def create_box_with_frame(x, y, z, color, frame_color=[0, 0, 0]):
    box = o3d.geometry.TriangleMesh.create_box(width=1.0, height=1.0, depth=1.0)
    box.paint_uniform_color(color)
    box.translate((x, y, z))

    # Create a wireframe without diagonals
    points = box.vertices
    lines = [
        [0, 1], [1, 3], [3, 2], [2, 0],  # Bottom face edges
        [4, 5], [5, 7], [7, 6], [6, 4],  # Top face edges
        [0, 4], [1, 5], [2, 6], [3, 7]   # Side edges
    ]
    frame = o3d.geometry.LineSet()
    frame.points = points
    frame.lines = o3d.utility.Vector2iVector(lines)
    frame.paint_uniform_color(frame_color)

    return box, frame

# Color mapping function
def colors(val):
    if val == 42:
        return [0, 1, 0]  # Green
    elif val == 43:
        return [1, 0, 0]  # Red
    else:
        return [0.5, 0.5, 0.5]  # Grey

def view_numpyM(f, output_image):
    # Load the NumPy array
    array = np.load(f, allow_pickle=True)
    print(f"Processing {f} | Array size: {array.shape}")

    # Get the indices of non-zero/non-empty elements
    indices = np.nonzero(array != 0)
    coords = np.array(indices).T  # Shape: (N, 3), where N is the number of voxels

    if len(coords) == 0:
        print(f"No non-zero elements found in {f}.")
        return

    # Extract values at those coordinates
    values = array[indices]
    print(f"Number of non-zero voxels: {len(coords)}")
    print(f"Sample values: {values[:5]}")

    # Create geometries for boxes and frames
    geometries = []
    for i, (x, y, z) in enumerate(coords):
        val = values[i]
        color = colors(val)
        box, frame = create_box_with_frame(x, y, z, color, frame_color=[0, 0, 0])
        geometries.append(box)
        geometries.append(frame)

    print(f"Created {len(geometries)} geometries (boxes + frames)")

    # Create a visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=800, height=600, visible=False)  # Offscreen rendering

    # Add all geometries
    for geom in geometries:
        vis.add_geometry(geom)

    # Adjust camera to focus on the geometries
    # Compute bounding box of all points
    all_points = np.concatenate([np.asarray(geom.vertices) for geom in geometries if isinstance(geom, o3d.geometry.TriangleMesh)])
    if len(all_points) == 0:
        print(f"No valid points for camera adjustment in {f}.")
        vis.destroy_window()
        return

    bounds = o3d.geometry.AxisAlignedBoundingBox.create_from_points(o3d.utility.Vector3dVector(all_points))
    center = bounds.get_center()
    extent = bounds.get_extent()
    max_bound = max(extent)

    ctr = vis.get_view_control()
    ctr.set_lookat(center)
    ctr.set_front([1, 1, 1])  # Diagonal view
    ctr.set_up([1, 0, 1])     # Z-axis up
    ctr.set_zoom(0.7)         # Adjusted for better fit
    vis.update_renderer()
    vis.poll_events()

    # Small delay to ensure rendering
    time.sleep(0.1)

    # Capture and save the image
    vis.capture_screen_image(output_image, do_render=True)
    print(f"Saved image to {output_image}")
    vis.destroy_window()

# Directory containing .npy files
input_dir = "result"
npy_files = glob.glob(os.path.join(input_dir, "*.npy"))

# Process each .npy file
for npy_file in npy_files:
    base_name = os.path.splitext(os.path.basename(npy_file))[0]
    output_image = os.path.join(output_dir, f"{base_name}.png")
    view_numpyM(npy_file, output_image)