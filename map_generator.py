import cv2
import numpy as np
import json


def generate_vector_map(image_path="map.png", output_json="map_data.json"):
    # Load map image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not find '{image_path}'. Place an image in your project folder.")
        return

    # 1. Week 10: Image Segmentation (Thresholding)
    _, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    # 2. Week 11: Morphological Operations (Closing to fill small gaps)
    kernel = np.ones((3, 3), np.uint8)
    clean_map = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 3. Week 9: Canny Edge Detection
    edges = cv2.Canny(clean_map, 100, 200)

    # 4. Extract pixel coordinates
    y_coords, x_coords = np.where(edges > 0)

    height, width = edges.shape
    coordinates = []

    # Downsample points (every 4th point) to keep rendering fast in Turtle
    for i in range(0, len(x_coords), 1):  # Now it reads every pixel
        # Normalize coordinates so origin (0,0) is in the center
        norm_x = int(x_coords[i] - (width / 2))
        norm_y = int((height / 2) - y_coords[i])  # Flip Y for graphics coordinate system
        coordinates.append((norm_x, norm_y))

    # Save vectors to map_data.json
    with open(output_json, 'w') as f:
        json.dump(coordinates, f)

    print(f"Success! Extracted {len(coordinates)} vector points into '{output_json}'.")


if __name__ == "__main__":
    generate_vector_map()