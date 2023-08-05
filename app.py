import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from utils import preProcess, getBiggestContour, reorder, splitIntoBoxes, prediction, displayNumbers
from sudokuSolverLogic import solve
from tensorflow.keras.models import load_model

model = load_model('predictionModel.h5')

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'  # Set the path to the uploads folder

@app.route('/')
def index():
    return render_template('HomePage.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/solve_sudoku', methods=['POST'])
def solve_sudoku():
    file = request.files['file']
    
    if file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        file.save(image_path)
        
        image = cv2.imread(image_path)
        imageWidth = 450
        imageHeight = 450
        blankImage = np.zeros((imageHeight, imageWidth, 3), np.uint8)
        image = cv2.resize(image, (imageWidth, imageHeight))
        input_image = 'image.jpg'
        input_image_path = os.path.join(app.config['UPLOAD_FOLDER'],input_image)
        cv2.imwrite(input_image_path, image)
        
        processed_image = preProcess(image)
        
        contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        biggestContour = getBiggestContour(contours)
        
        if biggestContour.size != 0:
            biggestContour = reorder(biggestContour)
            
            pts1 = np.float32(biggestContour)
            pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450, 450]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            transformed_image = cv2.warpPerspective(image, matrix, (450, 450))
            transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)
            
            boxes = splitIntoBoxes(transformed_image)
            numbers = prediction(boxes, model)
            
            detectedDigitsImage = blankImage.copy()
            numbers = np.asarray(numbers)
            positionArray = np.where(numbers > 0, 0, 1)
            
            board = np.array_split(numbers,9)
            
            try:
                solve(board)
            except:
                print('Sudoku cannot be solved')
                pass
            print(board)
    
            flattenedList = []
            for sublist in board:
                for item in sublist:
                    flattenedList.append(item)
            
            solved_numbers = flattenedList*positionArray
            solvedDigitsImage = blankImage.copy()
            solvedDigitsImage = displayNumbers(solvedDigitsImage,solved_numbers,color=(0,165,255))
        
            points1 = np.float32([[0, 0],[imageWidth, 0], [0, imageHeight],[imageWidth, imageHeight]])
            points2 = np.float32(biggestContour) 
            matrix = cv2.getPerspectiveTransform(points1, points2) 
            
            solvedImageColored = image.copy()
            solvedImageColored = cv2.warpPerspective(solvedDigitsImage, matrix, (imageWidth, imageHeight))
            solved_image = cv2.addWeighted(solvedImageColored, 1, image, 0.7, 1)
            
            output_image_filename = 'solved_image.jpg'
            output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], output_image_filename)
            
            cv2.imwrite(output_image_path, solved_image)
            
            return jsonify({'status': 'success','input_image_path': url_for('uploaded_file', filename=input_image),'output_image_path': url_for('uploaded_file', filename=output_image_filename)})
        else:
            print('No sudoku detected')
            return jsonify({'status': 'error', 'message': 'No Sudoku detected'})

    else:
        return jsonify({'status': 'error', 'message': 'No image uploaded'}), 400

if __name__ == '__main__':
    app.run()
