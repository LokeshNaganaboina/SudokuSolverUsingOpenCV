document.getElementById("image-form").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the default form submission
  
  var imageInput = document.getElementById("image-input");
  var file = imageInput.files[0];

  // Check if a file has been selected
  if (!file) {
    alert("Please select an image before submitting.");
    return; // Stop further processing
  }

  var formData = new FormData();
  formData.append('file', file);
  
  // Send the uploaded image to the Flask app for processing
  fetch('/solve_sudoku', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      var InputImageDisplay = document.getElementById('input-image-display');
      var outputImageDisplay = document.getElementById("output-image-display");
      InputImageDisplay.src = data.input_image_path + '?' + new Date().getTime(); //Browser refresh
      outputImageDisplay.src = data.output_image_path + '?' + new Date().getTime();
      
      console.log(InputImageDisplay.src);
      console.log(outputImageDisplay.src);
  })
  .catch(error => {console.error('Error:', error)
      alert("Error occured, please try again!");
    }
  );
});
  