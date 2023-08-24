function getCurrentSuggestions() {
    var currentSuggestions = []
    var rows = document.querySelectorAll('tbody tr');
    for (var i = 1; i < rows.length - 1; i++) {
        var row = rows[i];
	var inputField = row.querySelector('input[name="new_names[]"]');
	if (inputField.value != '') {
	    currentSuggestions.push(inputField.value);
	}
    }
    return currentSuggestions
}

function uniqueValue(arr, value) {
    console.log(arr);
    console.log(value);
    let count = 0;
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === value) {
            count++;
            if (count > 1) {
                return false; // Value not found more than once
            }
        }
    }
    return true; // Value found more than once
}

function suggestMale(row) {
    return new Promise((resolve) => {
	$.ajax({
            type: 'POST',
            url: '/suggest-male',
            contentType: 'application/json',
            success: function(response) {
		var suggestedName = response.suggested_name;
		var inputField = row.querySelector('input[name="new_names[]"]');
		inputField.value = suggestedName;
		resolve(suggestedName);
            }
	});
    });
}

function suggestFemale(row) {
    return new Promise((resolve) => {
	$.ajax({
            type: 'POST',
            url: '/suggest-female',
            contentType: 'application/json',
            success: function(response) {
		var suggestedName = response.suggested_name;
		var inputField = row.querySelector('input[name="new_names[]"]');
		inputField.value = suggestedName;
		resolve(suggestedName);
            }
	});
    });
}

function suggestNb(row) {
    return new Promise((resolve) => {
	$.ajax({
            type: 'POST',
            url: '/suggest-nb',
            contentType: 'application/json',
            success: function(response) {
		var suggestedName = response.suggested_name;
		var inputField = row.querySelector('input[name="new_names[]"]');
		inputField.value = suggestedName;
		resolve(suggestedName);
            }
	});
    });
}
		     	      

async function suggestRow(suggestFunction, row) {
    return new Promise((resolve) => {
	(async () => {
	    success = false
	    for(var i = 1; i < 20; i++) {
		console.log(i);
		i += 1;
		const response = await suggestFunction(row);
		console.log(response);
		if (uniqueValue(getCurrentSuggestions(), response)) {
		    success = true;
		    resolve(response)
		    break;
		}
	    }
	    if (!success) {
		console.log('Failed to find unique name')
		resolve('Failed to find unique name')
	    }
	})()
    });
}
		      
async function suggestAll(type) {
    var rows = document.querySelectorAll('tbody tr');
    for (var i = 1; i < rows.length - 1; i++) {
        var row = rows[i];
	console.log('Working on row ' + i)
        switch (type) {
            case 'nb':
                await suggestRow(suggestNb, row);
                break;
            case 'female':
                await suggestRow(suggestFemale, row);
                break;
            case 'male':
                await suggestRow(suggestMale, row);
                break;
            default:
                break;
        }
    }
}

function clearRow(row){
    var inputField = row.querySelector('input[name="new_names[]"]');
    inputField.value = '';
}

function clearAll() {
    var rows = document.querySelectorAll('tbody tr');
    for (var i = 1; i < rows.length - 1; i++) {
        var row = rows[i];
        clearRow(row);
    }
}
