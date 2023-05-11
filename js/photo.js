const gallery = document.querySelector('.gallery');

// Define the folder containing the images
const folder = './images/photos/full size';

// Define the file extension of the images to display
const fileExt = '.jpg';

// Create a new XMLHttpRequest object
const xhr = new XMLHttpRequest();

// Define the HTTP method and URL
xhr.open('GET', folder);

// Define the responseType as document
xhr.responseType = 'document';

// When the request has loaded
xhr.onload = function() {
	// Get the response HTML document
	const response = xhr.response;

	// Get all the anchor elements in the response
	const anchors = response.querySelectorAll('a');

	// Filter the anchor elements to only include those that link to images with the specified file extension
	const images = Array.from(anchors).filter(anchor => anchor.href.endsWith(fileExt));

	// Loop through the images and add them to the gallery
	images.forEach(image => {
		// Create a new image element
		const img = document.createElement('img');

		// Set the src attribute to the image URL
		img.src = image.href;

		// Add the image to the gallery
		gallery.appendChild(img);
	});
};

// Send the request
xhr.send();
