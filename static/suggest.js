$(document).ready(function() {
  $('.suggest-button').on('click', function() {
    var existingName = $(this).closest('tr').find('.existing-name').text();
    var inputField = $(this).closest('tr').find('input[name="new_names[]"]');

    $.ajax({
      type: 'POST',
      url: '/suggest-name',
      data: JSON.stringify({'existing_name': existingName}),
      contentType: 'application/json',
      success: function(response) {
        var suggestedName = response.suggested_name;
        inputField.val(suggestedName);
      },
      error: function() {
        console.error('Failed to suggest name.');
      }
    });
  });
});
