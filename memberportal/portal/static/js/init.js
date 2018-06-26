let memberActionsModal;

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
    let modalElem = document.getElementById('member-actions-modal');
    memberActionsModal = M.Modal.init(modalElem, {'endingBottom': '5%'});

    // Tabs init
    M.Tabs.init(document.querySelectorAll('.tabs'));
});


function initSelects() {
    M.FormSelect.init(document.querySelectorAll('select'), {});
};

function setState(state) {
    let state_url;

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
                M.toast({html: "Successfully enabled access."});
            } else {
                state_url = deactive_url;
                document.getElementById("activate-member-button").classList.remove("disabled");
                document.getElementById("deactivate-member-button").classList.add("disabled");
                M.toast({html: "Successfully disabled access."});
            }
        },
        error: function (data) {
              M.toast({html: "There was an error processing the request. :("});
        }
    });
}

let name;
let profile_url;
let access_url;
let member_id;
let deactive_url;
let active_url;
let member_state;

function openMemberActionsModal(e) {
    name = e.getAttribute("name");
    member_state = e.getAttribute("data-state");
    member_id = e.getAttribute("id");
    profile_url = e.getAttribute("data-url");
    access_url = e.getAttribute("data-access_url");
    active_url = e.getAttribute("data-active_url");
    deactive_url = e.getAttribute("data-deactive_url");
    document.getElementById('admin-member-modal-name').innerText = name;

    // get the edit profile form
    $.ajax({
        url: profile_url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (data) {
            let elem = document.getElementById("admin-edit-member-profile");
            elem.innerHTML = data.html_form;

            setTimeout(function () {
                initSelects();
            }, 0);
        }
    });

    // get the access form
    $.ajax({
        url: access_url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (data) {
            let elem = document.getElementById("admin-edit-member-access");
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
    let form = $(this);

    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                M.toast({html: "Saved successfully :D"});
            }
            else {
                M.toast({html: "There was an error saving the data. :("});            }
        }
    });
    return false;
});

function deleteCause(btn) {
    $.get(btn.getAttribute("data-url"), function(data){
        alert(data);
        location.reload();
    });
}
