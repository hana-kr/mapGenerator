from nms import non_max_suppression_fast
import numpy as np
import cv2
import imutils

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and details
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 200)

    return edges

def find_and_draw_matches(image, template):
    # Preprocess the template and search image
    template_processed = preprocess_image(template)
    image_processed = preprocess_image(image)

    # get dimensions of the template
    (tH, tW) = template.shape[:2]

    # perform multi-scale template matching
    print("[INFO] performing multi-scale template matching...")
    matches = []

    for scale in np.linspace(0.5, 1.5, 25)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        resized = imutils.resize(image_processed, width=int(image_processed.shape[1] * scale))
        r = image_processed.shape[1] / float(resized.shape[1])

        # if the resized image is smaller than the template, then break from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        # perform template matching using the preprocessed template and image
        result = cv2.matchTemplate(resized, template_processed, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.8)

        for pt in zip(*loc[::-1]):
            matches.append((int(pt[0] * r), int(pt[1] * r), int((pt[0] + tW * r)), int((pt[1] + tH * r))))

    # apply non-maxima suppression to the rectangles
    pick = non_max_suppression_fast(np.array(matches), 0.3)
    print("[INFO] {} matched locations *after* NMS".format(len(pick)))

    # loop over the final bounding boxes
    for (startX, startY, endX, endY) in pick:
        # draw the bounding box on the original image
        cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 3)

    # show the output image
    cv2.imshow("After Multi-Scale NMS", image)
    cv2.waitKey(0)

    return image

# load the input image and template image from disk
print("[INFO] loading images...")
search_image = cv2.imread('DefaultPics/geometricc.png')
template = cv2.imread('shapes/pre-saved_2D/square.png')

# Find and draw matches for each template at different scales
result_image = search_image.copy()
result_image = find_and_draw_matches(result_image, template)

# Display the result
cv2.imwrite("out.png", result_image)
# cv2.imshow('Matching Result', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()