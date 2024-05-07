    function submitForm(action) {
	// Determine which form is currently visible
	var desktopForm = document.getElementById('desktop-form');
	var mobileForm = document.getElementById('mobile-form');
	var actionInputDesktop = document.getElementById('desktop-action');
	var actionInputMobile = document.getElementById('mobile-action');
	
	// Check visibility by computing the display style
	var isDesktopVisible = window.getComputedStyle(desktopForm).display !== 'none';
	
	if (isDesktopVisible) {
            // Set action and submit the desktop form if visible
            actionInputDesktop.value = action;
            desktopForm.submit();
	} else {
            // Otherwise, set action and submit the mobile form
            actionInputMobile.value = action;
            mobileForm.submit();
	}
    }
