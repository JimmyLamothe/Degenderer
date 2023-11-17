function getCurrentSuggestions() {
    var currentSuggestions = []
    var rows = document.querySelectorAll('tbody tr');
    for (var i = 1; i < rows.length - 1; i++) {
        var row = rows[i];
	var inputField = row.querySelector('input[name="new_names[]"]');
	if (inputField && inputField.value != '') {
	    currentSuggestions.push(inputField.value);
	}
    }
    return currentSuggestions
}

function suggestMale(row, index) {
    return new Promise((resolve) => {
	$.ajax({
            type: 'POST',
            url: '/suggest-male',
            contentType: 'application/json',
	    data: JSON.stringify({
		row : index,
		pageSuggestions: getCurrentSuggestions()
	    }),
            success: function(response) {
		var suggestedName = response.suggested_name;
	    var inputField = row.querySelector('input[name="new_names[]"]');
		inputField.value = suggestedName;
		resolve(suggestedName);
            }
	});
    });
}

function suggestFemale(row, index) {
    return new Promise((resolve) => {
	$.ajax({
            type: 'POST',
            url: '/suggest-female',
	    data: JSON.stringify({
		row : index,
		pageSuggestions: getCurrentSuggestions()
	    }),
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

function suggestNb(row, index) {
    return new Promise((resolve) => {
	$.ajax({
            type: 'POST',
            url: '/suggest-nb',
	    data: JSON.stringify({
		row : index,
		pageSuggestions: getCurrentSuggestions()
	    }),
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
		     	      

async function suggestRow(suggestFunction, row, index) {
    return new Promise((resolve) => {
       (async () => {
           const response = await suggestFunction(row);
	   resolve(response);
       })()
    });
}
		      		      
async function suggestAll(type, index) {
    var rows = document.querySelectorAll('tbody tr');
    for (var i = 1; i < rows.length - 1; i++) {
        var row = rows[i];
	console.log('Working on row ' + i)
        switch (type) {
            case 'nb':
                await suggestRow(suggestNb, row, i);
                break;
            case 'female':
                await suggestRow(suggestFemale, row, i);
                break;
            case 'male':
                await suggestRow(suggestMale, row, i);
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
