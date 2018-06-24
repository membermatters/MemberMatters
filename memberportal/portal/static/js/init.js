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
    memberActionsModal = M.Modal.init(modalElem, {'endingBottom': '5%'});

    // Tabs init
    M.Tabs.init(document.querySelectorAll('.tabs'));
});


function initSelects() {
    M.FormSelect.init(document.querySelectorAll('select'), {});
};

function setState(state) {
    var state_url;

    if (state) {
        state_url = active_url;
    } else {
        state_url = deactive_url;
    }

    $.ajax({
        url: state_url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if (state) {
                state_url = active_url;
                document.getElementById("activate-member-button").classList.add("disabled");
                document.getElementById("deactivate-member-button").classList.remove("disabled");
            } else {
                state_url = deactive_url;
                document.getElementById("activate-member-button").classList.remove("disabled");
                document.getElementById("deactivate-member-button").classList.add("disabled");
            }
        },
        error: function (data) {
            alert("There was an error processing the request. :( ")
        }
    });
}

var name;
var url;
var member_id;
var deactive_url;
var active_url;
var member_state;

function openMemberActionsModal(e) {
    name = e.getAttribute("name");
    member_state = e.getAttribute("data-state");
    member_id = e.getAttribute("id");
    url = e.getAttribute("data-url");
    active_url = e.getAttribute("data-active_url");
    deactive_url = e.getAttribute("data-deactive_url");
    document.getElementById('admin-member-modal-name').innerText = name;

    $.ajax({
        url: url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (data) {
            var elem = document.getElementById("admin-edit-member-profile");
            elem.innerHTML = data.html_form;

            setTimeout(function () {
                initSelects();
            }, 0);
        }
    });

    document.getElementById("activate-member-button").innerText = "Enable Access";
    if (member_state == 3) {
        document.getElementById("activate-member-button").classList.remove("disabled");
        document.getElementById("deactivate-member-button").classList.add("disabled");
    } else if (member_state == 2) {
        document.getElementById("activate-member-button").classList.add("disabled");
        document.getElementById("deactivate-member-button").classList.remove("disabled");
    } else if (member_state == 1) {
        document.getElementById("activate-member-button").innerText = "Make Member";
        document.getElementById("activate-member-button").classList.remove("disabled");
        document.getElementById("deactivate-member-button").classList.add("disabled");
    }

    memberActionsModal.open();
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
                alert("Saved :D");
                location.reload();
            }
            else {
                alert("Sorry there was an error with the form data :(");
            }
        }
    });
    return false;
});