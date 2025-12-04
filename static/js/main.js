(function($) {
  'use strict';
  $(function() {
    var todoListItem = $('.new-todo-list');
    var todoListInput = $('.todo-list-input');
    var addBtn = $('.todo-list-add-btn');
    var hiddenItemsContainer = $('#hidden-items');

    function addItem() {
      var item = todoListInput.val().trim();
      if (!item) return;

      // Add visible list item
      todoListItem.append(
        "<li class='todo-item'>" +
        "<div class='todo-left'>" +
        "<input class='checkbox' type='checkbox'/>" +
        "<span class='ms-3'>" + item + "</span>" +
        "</div>" +
        "<div class='todo-right'>" +
        "<button type='button' class='btn btn-link btn-sm edit-btn'>" +
            "<img src='" + editIconURL + "' alt='Edit' width='18' height='18'>" +
        "</button>" +
        "<button type='button' class='btn btn-link btn-sm delete-btn'>" +
            "<img src='" + deleteIconURL + "' alt='Delete' width='18' height='18'>" +
        "</button>" +
        "</div>" +
        "</li>"
      );

      // Add hidden input for form submission
      hiddenItemsContainer.append(
        "<input type='hidden' name='items' value='" + item + "'>"
      );

      todoListInput.val("");
    }

    // Add button click
    addBtn.on("click", function(e) {
      e.preventDefault();
      addItem();
    });

    // Enter key adds item
    todoListInput.on("keydown", function(e) {
      if (e.key === "Enter") {
        e.preventDefault();
        addItem();
      }
    });

    // Delete item
    $('.old-todo-list').on('click', '.delete-btn', function () {
        const itemId = $(this).data('item-id');
        const li = $(this).closest('.todo-item');

        $.post(`/delete_item/${itemId}`, function () {
            li.remove();
        });
    });
    // Edit item
    $('.old-todo-list').on('click', '.edit-btn', function () {
        const li = $(this).closest('.todo-item');
        const textSpan = li.find('.item-text');
        const input = li.find('.item-edit-input');

        // Put old text as placeholder
        input.attr('placeholder', textSpan.text());

        // Hide text, show input
        textSpan.addClass('d-none');
        input.removeClass('d-none');

        input.val(''); // clear so placeholder shows
        input.focus();
    });

    // Save edited item on Enter key
    $('.old-todo-list').on('keydown', '.item-edit-input', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();

            const li = $(this).closest('.todo-item');
            const textSpan = li.find('.item-text');
            const input = $(this);

            const newValue = input.val().trim();

            if (newValue) {
                // Update visible text
                textSpan.text(newValue);
            }

            // Restore UI
            input.addClass('d-none');
            textSpan.removeClass('d-none');

            // KEEP hidden input value updated for form submission
            input.val(newValue);
        }
    });


  });
})(jQuery);
