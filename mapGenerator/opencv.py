import cv2
import numpy as np

def find_all_shapes(source_image_path, template_paths, output_path):
    # Read the source image
    source_image = cv2.imread(source_image_path)

    # Convert the source image to grayscale
    source_gray = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

    for template_path in template_paths:
        # Read the template image
        template_image = cv2.imread(template_path)

        # Convert the template image to grayscale
        template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

        # Match the template in the source image
        result = cv2.matchTemplate(source_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust threshold as needed
        locations = np.where(result >= threshold)

        # Draw rectangles around all occurrences
        for loc in zip(*locations[::-1]):
            top_left = loc
            bottom_right = (top_left[0] + template_gray.shape[1], top_left[1] + template_gray.shape[0])
            cv2.rectangle(source_image, top_left, bottom_right, (0, 255, 0), 1)  # Adjust thickness here

    # Save the result image
    cv2.imwrite(output_path, source_image)

# def main():
#     # Replace this path with the path to your source image
#     source_image_path = "DefaultPics/shapes.png"

#     # Replace this path with the desired output path for the result image
#     output_path = "DefaultPics/res.png"

#     use_pre_saved_templates = False  # Set to False if you want to provide your own templates

#     if use_pre_saved_templates:
#         # Use pre-saved templates
#         template_paths = [
#             "path/to/template/unknown_shape_1.jpg",
#             "path/to/template/unknown_shape_2.jpg",
#             # Add more template paths as needed
#         ]
#     else:
#         # Provide your own template paths
#         template_paths = [
#             "DefaultPics/shape.png",
#             "DefaultPics/shape2.png",
#             "DefaultPics/shape3.png",
#             # Add more template paths as needed
#         ]

#     find_all_shapes(source_image_path, template_paths, output_path)

# if __name__ == "__main__":
#     main()
