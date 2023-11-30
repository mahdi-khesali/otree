// gallery.js
var currentImageIndex = 0;
var images = [
  "../../global/mugIdentity_1.jpg",
  "../../global/mugIdentity_2.jpg",
  "../../global/mugIdentity_3.jpg",
  "../../global/mugIdentity_4.jpg",
  "../../global/mugIdentity_5.jpg",
  // Add more image paths as needed
];

function previousImage() {
  if (currentImageIndex > 0) {
    currentImageIndex--;
    updateImage();
  }
}

function nextImage() {
  if (currentImageIndex < images.length - 1) {
    currentImageIndex++;
    updateImage();
  }
}

function updateImage() {
  var img = document.getElementById('main-img');
  img.src = images[currentImageIndex];
}

function setColor(color) {
  console.log("User selected the color: " + color);

  // Update the border of the selected color to show selection
  var colorChoices = document.getElementsByClassName('color-choice');
  for (var i = 0; i < colorChoices.length; i++) {
    colorChoices[i].classList.remove('selected');
  }
  document.getElementById(color).classList.add('selected');
  
  // Perform further actions based on the color selected
}
