var suggestedNames = []; // Initialize an empty array to store suggested names

function suggest_male(row) {
    var existingName = row.querySelector('.existing-name').textContent;
    var recursionCalls = 0
    // Define the recursive function for suggesting a name
    function suggestName() {
	recursionCalls += 1
        $.ajax({
            type: 'POST',
            url: '/suggest-male',
            data: JSON.stringify({'existing_name': existingName}),
            contentType: 'application/json',
            success: function(response) {
                var suggestedName = response.suggested_name;
                if (suggestedNames.includes(suggestedName)) {
                    // Call the suggestName function again if the name is already in the list
                    if (recursionCalls < 6) {
			suggestName();
		    }
		    else {
			var inputField = row.querySelector('input[name="new_names[]"]');
			inputField.value = suggestedName;
		    }
                } else {
		    suggestedNames.push(suggestedName); // Add the suggested name to the list
                    var inputField = row.querySelector('input[name="new_names[]"]');
                    inputField.value = suggestedName;
                }
            },
            error: function() {
                console.error('Failed to suggest name.');
            }
        });
    }

    // Start the recursive suggestion process
    suggestName();
}

function suggest_male_backup(row) {
    // Old version that doesn't check for duplicates
    var existingName = row.querySelector('.existing-name').textContent;

    $.ajax({
        type: 'POST',
        url: '/suggest-male',
        data: JSON.stringify({'existing_name': existingName}),
        contentType: 'application/json',
        success: function(response) {
            var suggestedName = response.suggested_name;
            var inputField = row.querySelector('input[name="new_names[]"]');
            inputField.value = suggestedName;
        },
        error: function() {
            console.error('Failed to suggest name.');
        }
    });
}

function suggest_female(row) {
    var existingName = row.querySelector('.existing-name').textContent;
    var recursionCalls = 0
    // Define the recursive function for suggesting a name
    function suggestName() {
	recursionCalls += 1
        $.ajax({
            type: 'POST',
            url: '/suggest-female',
            data: JSON.stringify({'existing_name': existingName}),
            contentType: 'application/json',
            success: function(response) {
                var suggestedName = response.suggested_name;
                if (suggestedNames.includes(suggestedName)) {
                    // Call the suggestName function again if the name is already in the list
                    if (recursionCalls < 6) {
			suggestName();
		    }
		    else {
			var inputField = row.querySelector('input[name="new_names[]"]');
			inputField.value = suggestedName;
		    }
                } else {
		    suggestedNames.push(suggestedName); // Add the suggested name to the list
                    var inputField = row.querySelector('input[name="new_names[]"]');
                    inputField.value = suggestedName;
                }
            },
            error: function() {
                console.error('Failed to suggest name.');
            }
        });
    }

    // Start the recursive suggestion process
    suggestName();
}

function suggest_female_backup(row) {
    // Old version that doesn't check for duplicates
    var existingName = row.querySelector('.existing-name').textContent;
    $.ajax({
        type: 'POST',
        url: '/suggest-female',
        data: JSON.stringify({'existing_name': existingName}),
        contentType: 'application/json',
        success: function(response) {
            var suggestedName = response.suggested_name;
            var inputField = row.querySelector('input[name="new_names[]"]');
            inputField.value = suggestedName;
        },
        error: function() {
            console.error('Failed to suggest name.');
        }
    });
}

function suggest_nb(row) {
    var existingName = row.querySelector('.existing-name').textContent;
    var recursionCalls = 0
    // Define the recursive function for suggesting a name
    function suggestName() {
	recursionCalls += 1
        $.ajax({
            type: 'POST',
            url: '/suggest-nb',
            data: JSON.stringify({'existing_name': existingName}),
            contentType: 'application/json',
            success: function(response) {
                var suggestedName = response.suggested_name;
                if (suggestedNames.includes(suggestedName)) {
                    // Call the suggestName function again if the name is already in the list
                    if (recursionCalls < 6) {
			suggestName();
		    }
		    else {
			var inputField = row.querySelector('input[name="new_names[]"]');
			inputField.value = suggestedName;
		    }
                } else {
		    suggestedNames.push(suggestedName); // Add the suggested name to the list
                    var inputField = row.querySelector('input[name="new_names[]"]');
                    inputField.value = suggestedName;
                }
            },
            error: function() {
                console.error('Failed to suggest name.');
            }
        });
    }

    // Start the recursive suggestion process
    suggestName();
}

function suggest_nb_backup(row) {
    // Old version that doesn't check for duplicates
    var existingName = row.querySelector('.existing-name').textContent;

    $.ajax({
        type: 'POST',
        url: '/suggest-nb',
        data: JSON.stringify({'existing_name': existingName}),
        contentType: 'application/json',
        success: function(response) {
            var suggestedName = response.suggested_name;
            var inputField = row.querySelector('input[name="new_names[]"]');
            inputField.value = suggestedName;
        },
        error: function() {
            console.error('Failed to suggest name.');
        }
    });
}
    
function suggestAll(type) {
    var rows = document.querySelectorAll('tbody tr');
    for (var i = 1; i < rows.length - 1; i++) {
        var row = rows[i];
        switch (type) {
          case 'nb':
              suggest_nb(row);
              break;
          case 'female':
              suggest_female(row);
              break;
          case 'male':
              suggest_male(row);
              break;
          default:
              break;
        }
    }
}
