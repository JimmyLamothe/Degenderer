document.querySelectorAll(".toggle").forEach(function(btn) {
    btn.addEventListener("click", function(e) {
	e.stopPropagation();
	var sample = this.closest(".sample");
	var content = sample.querySelector(".sample-content");
	if (content.style.display === 'block') {
	    content.style.display = 'none';
	} else {
	    content.style.display = 'block';
	}
	btn.classList.toggle("active");
    });
});

const sampleDescriptions = document.querySelectorAll('.sample-header');
sampleDescriptions.forEach((description) => {
    description.addEventListener('click', (e) => {
	const sample = e.target.closest('.sample');
	const toggleBtn = sample.querySelector('.toggle');
	toggleBtn.click();
    });
});

// Add download links to sample download buttons
const sampleDownloadButtons = document.querySelectorAll('.sample-download');
const sampleNames = ['one', 'two', 'three']; // Change these to match your sample names
sampleDownloadButtons.forEach((button, index) => {
  const sampleName = sampleNames[index];
  button.href = sampleName + '.epub';
  button.download = sampleName + '.epub';
});

