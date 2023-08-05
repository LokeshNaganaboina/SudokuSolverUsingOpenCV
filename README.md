# Sudoku Solver using OpenCV

This repository contains a web-based Sudoku Solver implemented using the OpenCV library for image processing and the Flask framework for web development in Python. The application utilizes AJAX (Asynchronous JavaScript and XML) to handle user interactions and dynamic updates, allowing for a seamless and interactive experience. The goal of this project is to provide a user-friendly tool for solving Sudoku puzzles automatically using computer vision techniques.

## Installation

Clone the repository:

```bash
git clone https://github.com/LokeshYadav-01/SudokuSolverUsingOpenCV.git
```
Set up a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate #For Linux or macOS users
venv\Scripts\activate #For Windows users
```

Install the necessary packages to run this project from requirements.txt

```bash
pip install requirement.txt
```
To run the app, run the following command
```bash
python app.py
```

## Usage
Run the Sudoku Solver application:
```python
python app.py
```
Select an image: You can select to input an image file containing an unsolved sudoku puzzle. Ensure that the image is of good quality and images should be recognized.

Press the 'Solve' button to initiate the solving process. The application will display the solved puzzle on the screen.

## How it Works

The Sudoku Solver uses OpenCV for image processing and computer vision tasks. Here's a high-level overview of the solving process:

Input Processing: The input image is preprocessed using various techniques like thresholding, contour detection, and perspective transformation to extract the Sudoku grid.

Digit Recognition: Each cell of the grid is isolated, and digit recognition is performed using a custom OCR trained model.

Backtracking Algorithm: The recognized puzzle is then solved using a backtracking algorithm, a common approach for solving Sudoku puzzles.

Flask Web Server: Flask acts as a web server. It listens for incoming requests from the user's web browser and responds accordingly. When the user accesses the web application, Flask serves the HTML, CSS, and JavaScript files to create the front-end interface.

AJAX Handling: AJAX requests handle interactions between the front-end and back-end, enabling real-time updates without full page reloads.

Here is a sample image of the application on how it looks

##

Enjoy solving Sudoku puzzles with the power of OpenCV and Flask! If you have any questions or need assistance, feel free to contact me.
