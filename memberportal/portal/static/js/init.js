var memberActionsModal;

(function ($) {
    $(function () {

    }); // end of document ready
})(jQuery); // end of jQuery name space

// when the page finishes loading
document.addEventListener('DOMContentLoaded', function () {
    // Side bar init
    M.Sidenav.init(document.querySelectorAll('.sidenav'), {});

    // Select init
    M.FormSelect.init(document.querySelectorAll('select'), {});

    // Dropdown init
    M.Dropdown.init(document.querySelectorAll('.dropdown-trigger'), {"coverTrigger": false, "hover": false});
    M.Dropdown.init(document.querySelectorAll('.dropdown-trigger-hover'), {"coverTrigger": false, "hover": true});

    // Modal init
    var modalElem = document.getElementById('member-actions-modal');
    memberActionsModal = M.Modal.init(modalElem);

    // Tabs init
    M.Tabs.init(document.querySelectorAll('.tabs'));
});


function initSelects() {
   M.FormSelect.init(document.querySelectorAll('select'), {});
};


function openMemberActionsModal(e) {
    memberActionsModal.open();
    var name = e.getAttribute("name");
    var url = e.getAttribute("data-url");
    document.getElementById('admin-member-modal-name').innerText = name;

    $.ajax({
    url: url,  // <-- AND HERE
    type: 'get',
    dataType: 'json',
    success: function (data) {
      var elem = document.getElementById("admin-edit-member-profile");
      elem.innerHTML = data.html_form;

      setTimeout(function(){ initSelects(); }, 0);
    }
  });
}

$("#member-actions-modal").on("submit", ".member-edit-form", function () {
    var form = $(this);
    console.log(form);

    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          alert("yay");
        }
        else {
          alert("nay");
        }
      }
    });
    return false;
  });