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
