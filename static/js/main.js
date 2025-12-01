(function($) {
  'use strict';
  $(function() {
    var todoListItem = $('.todo-list');
    var todoListInput = $('.todo-list-input');
    var addBtn = $('.todo-list-add-btn');
    var hiddenItemsContainer = $('#hidden-items');

    function addItem() {
      var item = todoListInput.val().trim();
      if (!item) return;

      // Add visible list item
      todoListItem.append(
        "<li><div class='form-check'><label class='form-check-label'>" +
        "<input class='checkbox' type='checkbox'/>" +
        item +
        "<i class='input-helper'></i></label></div>" +
        "<i class='remove mdi mdi-close-circle-outline'></i></li>"
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
