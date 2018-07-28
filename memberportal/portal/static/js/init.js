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
    M.Dropdown.init(document.querySelectorAll('.dropdown-trigger'), {
        "closeOnClick": false,
        "coverTrigger": false,
        "hover": false
    });
    M.Dropdown.init(document.querySelectorAll('.dropdown-trigger-hover'), {"coverTrigger": false, "hover": true});
    M.Dropdown.init(document.querySelectorAll('body > div.container > div > form > div > div > p:nth-child(11) > div > input'), {"coverTrigger": false, "closeOnClick": true,});

    // Modal init
    let modalElem = document.getElementById('member-actions-modal');
    memberActionsModal = M.Modal.init(modalElem, {'endingBottom': '5%'});

    // Tabs init
    M.Tabs.init(document.querySelectorAll('.tabs'));

    // Collapsible init
    M.Collapsible.init(document.querySelectorAll('.collapsible'), {});
});


function initSelects() {
    M.FormSelect.init(document.querySelectorAll('select'), {});
}

function resendWelcome() {
    $.ajax({
        url: resend_welcome_url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (data) {
                M.toast({html: "Successfully resent welcome email."});
        },
        error: function (data) {
            M.toast({html: "There was an error processing the request. :("});
        }
    });
}

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
                if (document.getElementById("activate-member-button").innerText == "MAKE MEMBER") {
                    M.toast({html: "Successfully activated member and sent welcome email."});
                } else {
                    M.toast({html: "Successfully enabled access."});
                }
            } else {
                state_url = deactive_url;
                document.getElementById("activate-member-button").classList.remove("disabled");
                document.getElementById("deactivate-member-button").classList.add("disabled");
                M.toast({html: "Successfully disabled access."});
            }
            // not very DRY... ideally should be modularised a bit more...
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
                },
                error: function () {
                    M.toast({html: "Unkown error 2 :( "});
                }
            });
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
let resend_welcome_url;
let get_logs_url;

function openMemberActionsModal(e) {
    name = e.getAttribute("data-name");
    member_state = e.getAttribute("data-state");
    member_id = e.getAttribute("id");
    profile_url = e.getAttribute("data-url");
    access_url = e.getAttribute("data-access_url");
    active_url = e.getAttribute("data-active_url");
    deactive_url = e.getAttribute("data-deactive_url");
    resend_welcome_url = e.getAttribute("data-resend_welcome_url");
    get_logs_url = e.getAttribute("data-get_logs_url");
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
        },
        error: function () {
            M.toast({html: "Unkown error while getting profile form :( "});
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
        },
        error: function () {
            M.toast({html: "Unkown error while getting access form :( "});
        }
    });

    // get the member logs
    $.ajax({
        url: get_logs_url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (data) {
            let elem = document.getElementById("admin-edit-member-logs");
            elem.innerHTML = data.html_form;

            // init the table
            let table = $('#logTable').DataTable({
                "initComplete": function () {
                    M.FormSelect.init(document.querySelectorAll('select'), {});
                }
            });

            table.order([0, 'desc']).draw();
        },
        error: function () {
            M.toast({html: "Unkown error while getting logs :( "});
        }
    });

    document.getElementById("activate-member-button").innerText = "Enable Access";
    if (member_state == "inactive") {
        document.getElementById("activate-member-button").classList.remove("disabled");
        document.getElementById("deactivate-member-button").classList.add("disabled");
    } else if (member_state == "active") {
        document.getElementById("activate-member-button").classList.add("disabled");
        document.getElementById("deactivate-member-button").classList.remove("disabled");
    } else if (member_state == "noob") {
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
                let elem = document.getElementById("admin-edit-member-profile");
                elem.innerHTML = data.html_form;
                setTimeout(function () {
                    initSelects();
                }, 0);
            }
            else {
                M.toast({html: "There was an error saving the data. :("});
                let elem = document.getElementById("admin-edit-member-profile");
                elem.innerHTML = data.html_form;
                setTimeout(function () {
                    initSelects();
                }, 0);
            }
        },
        error: function () {
            M.toast({html: "Unkown error 3 :( "});
        }
    });
    return false;
});

function deleteCause(btn) {
    $.get(btn.getAttribute("data-url"), function (data) {
        location.reload();
    });
}

function grantAccess(url, id) {
    $.ajax({
        url: url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                document.getElementById(id + "-grant-button").classList.add("disabled");
                document.getElementById(id + "-revoke-button").classList.remove("disabled");
                M.toast({html: "Access Granted :D"});
            }
            else {
                M.toast({html: "Error :( " + response.reason});
            }
        },
        error: function () {
            M.toast({html: "Unkown error 4 :( "});
        }
    });
}

function revokeAccess(url, id) {
    $.ajax({
        url: url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                document.getElementById(id + "-grant-button").classList.remove("disabled");
                document.getElementById(id + "-revoke-button").classList.add("disabled");
                M.toast({html: "Access Revoked :O"});
            }
            else {
                M.toast({html: "Error :( " + response.reason});
            }
        },
        error: function () {
            M.toast({html: "Unkown error 5 :( "});
        }
    });
}

function requestAccess(url) {
    $.ajax({
        url: url,  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Access request submitted."});
            }
            else {
                M.toast({html: "Error :( " + response.reason});
            }
        },
        error: function () {
            M.toast({html: "Unkown error 6 :( "});
        }
    });
}

function unlockDoor(thing) {
    $.ajax({
        url: thing.getAttribute("data-url"),  // <-- AND HERE
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Door unlock success."});
            }
            else {
                M.toast({html: "Error while trying to unlock door :("});
            }
        },
        error: function () {
            M.toast({html: "Unkown error while trying to unlock door :( "});
        }
    });
}