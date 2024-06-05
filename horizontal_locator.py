import cv2
import numpy as np
import glob
import os
# Function to calculate distance from point to line
def point_line_distance(point, line_start, line_end):
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end

    # Line vector
    line_vec = np.array([x2 - x1, y2 - y1])
    # Point vector
    point_vec = np.array([px - x1, py - y1])
    
    # Calculate the projection of point_vec onto line_vec
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    point_vec_scaled = point_vec / line_len
    t = np.dot(line_unitvec, point_vec_scaled)
    nearest = line_vec * t
    if point_vec[0] < nearest[0]:
        return "left"
    else:
        return "right"
    
    # Distance is the magnitude of dist_vec
    distance = np.linalg.norm(dist_vec)
    return distance

# Mouse callback function to draw line and calculate distance
drawing = False
line_start = None
line_end = None
point = None

def draw_line(event, x, y, flags, param):
    global drawing, line_start, line_end, point

    if event == cv2.EVENT_LBUTTONDOWN:
        if line_start is None:
            line_start = (x, y)
        elif line_end is None:
            line_end = (x, y)
        else:
            point = (x, y)
            # Calculate distance
            distance = point_line_distance(point, line_start, line_end)
            print(f'Distance from point {point} to line {line_start}-{line_end}: {distance}')
            return line_start, line_end
            

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            line_end = (x, y)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


# Load an image
# get all iamges inside annotated_image2
root=r'C:\Users\247404\ownCloud - juan.felipe.escobar.calderon@tiho-hannover.de@sync.academiccloud.de\Drone footage'
images=glob.glob(os.path.join(root, "**\\drone\\annotated_image2\\*.JPG"))

for image in images:
    image = cv2.imread(image)


    clone = image.copy()

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # Using resizeWindow() 
    cv2.resizeWindow('image', 700, 300) 
    cv2.setMouseCallback('image', draw_line)

    while True:
        temp_image = clone.copy()
        if line_start and line_end:
            cv2.line(temp_image, line_start, line_end, (0, 255, 0), 2)
        if point:
            cv2.circle(temp_image, point, 5, (255, 0, 0), -1)
        
        cv2.imshow('image', temp_image)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):  # Reset the drawing
            line_start = None
            line_end = None
            point = None
            clone = image.copy()
        elif key == 27:  # ESC key to break
            break

    cv2.destroyAllWindows()
