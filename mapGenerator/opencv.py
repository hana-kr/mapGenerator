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


