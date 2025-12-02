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

    // Remove item
    todoListItem.on('click', '.remove', function() {
      var index = $(this).parent().index();
      hiddenItemsContainer.find("input[name='items']").eq(index).remove();
      $(this).parent().remove();
    });
  });
})(jQuery);
