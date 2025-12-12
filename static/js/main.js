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

    // Delete item from old-todo-list
    $('.old-todo-list').on('click', '.delete-btn', function () {
        const itemId = $(this).data('item-id');
        const li = $(this).closest('.todo-item');

        $.post(`/delete_item/${itemId}`, function () {
            li.remove();
        });
    });
    // Delete todo list from sidebar
    $(document).on('click', '.delete-list-btn-sidebar', function (event) {
        event.preventDefault();
        event.stopPropagation();  // Prevent clicking the link

        const listId = $(this).data('list-id');
        const li = $(this).closest('li');

        $.post(`/delete_list/${listId}`, function () {
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

    document.addEventListener("change", function (event) {
        if (event.target.classList.contains("completed-checkbox")) {
            let item = event.target.closest(".todo-item");
            let text = item.querySelector(".item-text");

            if (event.target.checked) {
                text.classList.add("completed");
            } else {
                text.classList.remove("completed");
            }
        }
    });
    document.addEventListener("DOMContentLoaded", function() {
        const hiddenInput = document.getElementById('taskTempoValue');
        const button = document.getElementById('taskTempoButton');
        const taskUrgency = button.dataset.value;
        const iconMap = {
            "immediate": "/static/icons/red_circle.png",
            "timely": "/static/icons/orange_circle.png",
            "flexible": "/static/icons/green_circle.png"
        };

        const value = hiddenInput.value || taskUrgency || "flexible";

        button.innerHTML =
            `<img src="${iconMap[value]}" width="20" class="me-1">
            ${value.charAt(0).toUpperCase() + value.slice(1)}`;
    });
    document.querySelectorAll('.task-tempo-dropdown .dropdown-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();  // prevent default anchor behaviour

            const value = this.getAttribute('data-value'); // "immediate", "timely", "flexible"
            const text = this.textContent.trim();           // text like "Immediate"

            // Set hidden input value
            document.getElementById('taskTempoValue').value = value;

            // Update button text
            const button = this.closest('.task-tempo-dropdown').querySelector('button.dropdown-toggle');
            button.innerHTML = `<img src="${this.querySelector('img').src}" width="20" class="me-2"> ${text}`;
        });
        document.addEventListener("DOMContentLoaded", function() {
            const hiddenInput = document.getElementById('taskTempoValue');
            const button = document.getElementById('taskTempoButton');
            const taskUrgency = button.dataset.value;
            const iconMap = {
                "immediate": "/static/icons/red_circle.png",
                "timely": "/static/icons/orange_circle.png",
                "flexible": "/static/icons/green_circle.png"
            };

            const value = hiddenInput.value || taskUrgency || "flexible";

            button.innerHTML =
                `<img src="${iconMap[value]}" width="20" class="me-1">
                ${value.charAt(0).toUpperCase() + value.slice(1)}`;
        });

        });
    })(jQuery);
});