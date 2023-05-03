/*
// Get all the buttons with class "toggle"
let toggleButtons = document.querySelectorAll('.toggle');

// Loop through the buttons and add the click event listener
toggleButtons.forEach(button => {
    button.addEventListener('click', () => {
	// Toggle the active class of the button and content
	button.classList.toggle('active');
	let content = button.nextElementSibling;
	if (content.style.display === 'block') {
	    content.style.display = 'none';
	} else {
	    content.style.display = 'block';
	}
    });
});
*/

document.querySelectorAll(".toggle").forEach(function(btn) {
    btn.addEventListener("click", function(e) {
	e.stopPropagation();
	var example = this.closest(".example");
	var content = example.querySelector(".example-content");
	if (content.style.display === 'block') {
	    content.style.display = 'none';
	} else {
	    content.style.display = 'block';
	}
	btn.classList.toggle("active");
    });
});

const exampleDescriptions = document.querySelectorAll('.example-header');
exampleDescriptions.forEach((description) => {
    description.addEventListener('click', (e) => {
	const example = e.target.closest('.example');
	const toggleBtn = example.querySelector('.toggle');
	toggleBtn.click();
    });
});

// Add download links to example download buttons
const exampleDownloadButtons = document.querySelectorAll('.example-download');
const exampleNames = ['one', 'two', 'three']; // Change these to match your example names
exampleDownloadButtons.forEach((button, index) => {
  const exampleName = exampleNames[index];
  button.href = exampleName + '.epub';
  button.download = exampleName + '.epub';
});

