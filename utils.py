import cv2
import numpy as np
from tensorflow.keras.models import load_model

#Function to get the model
def predictionModel():
    model = load_model('predictionModel.h5')
    return model
   
#PreProcessing the image
def preProcess(image):
    greyScaleImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    kernelSize = (5,5)
    #kernel size should be odd
    #Larger kernel size results in more blur
    blurredImage = cv2.GaussianBlur(greyScaleImage,kernelSize,1) 
    imageThreshold = cv2.adaptiveThreshold(blurredImage,255,1,1,11,2) #Adaptive Threshold returns a binary image
    return imageThreshold

#Get the biggest contour among all the contours
def getBiggestContour(contours):
    biggestContour = np.array([]) #biggest contour to be found initially set to empty
    max_area = 0 #max_area of contour to be found
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50: #Ignore small contours
            perimeter = cv2.arcLength(contour, True)
            #Simplified polygon curve obtained using Ramer-Douglas-Peucker algorithm
            simplified_curve = cv2.approxPolyDP(contour, 0.02 * perimeter, True) 
            if area > max_area and len(simplified_curve) == 4:
                max_area = area
                biggestContour = simplified_curve
    return biggestContour #The biggest contour is being returned

# Reorder points for Warp Perspective
def reorder(Points):
    Points = Points.reshape((4, 2)) #Reshape to 4x2 array
    re_ordered_points = np.zeros((4, 1, 2), dtype=np.int32) #create an empty array of 4 points each 1x2
    add = Points.sum(1) #sum of x,y co-ordinates (x+y) for each point
    re_ordered_points[0] = Points[np.argmin(add)] #top-left [0,0]
    re_ordered_points[3] = Points[np.argmax(add)] #bottom-right [width,height]
    diff = np.diff(Points, axis=1) #difference of co-ordinates (y-x) for each point
    re_ordered_points[1] = Points[np.argmin(diff)] #top-right [width,0]
    re_ordered_points[2] = Points[np.argmax(diff)] #bottom-left [0,height]
    return re_ordered_points

#Splitting into 81 boxes
def splitIntoBoxes(image):
    boxes = []
    rows = np.vsplit(image, 9)
    for row in rows:
        cols = np.hsplit(row, 9)
        for box in cols:
            boxes.append(box)
    return boxes

#model prediction
def prediction(boxes,model):
    results = []
    for image in boxes:
        image = np.array(image) #list to array
        image = image[4:image.shape[0]-4, 4:image.shape[1]-4] #Crop the image by 4 pixel from all corners where 0 for height, 1 for width
        image = cv2.resize(image,(28,28)) #Resize into 28x28 pixel for ML classification model
        image = image/255 #Normalize the pixel value
        image = image.reshape(1,28,28,1) #creating a batch of images for prediction
        
        #prediction
        predictions = model.predict(image)
        classIndex  = np.argmax(predictions,axis=-1)
        probabilityValue = np.amax(predictions)
        
        #Save the index class indices
        if probabilityValue > 0.8:
            results.append(classIndex[0])
        else:
            results.append(0)
    return results

#Displaying numbers on the image
def displayNumbers(image, numbers, color):
    blockWidth = int(image.shape[1] / 9)
    blockHeight = int(image.shape[0] / 9)
    for x in range(0, 9):
        for y in range(0, 9):
            if numbers[(y * 9) + x] != 0:
                text = str(numbers[(y * 9) + x])
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 2, 2)
                text_x = x * blockWidth + int((blockWidth - text_width) / 2)
                text_y = y * blockHeight + int((blockHeight + text_height) / 2)
                cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, color, 2, cv2.LINE_AA)
    return image







        