let memberActionsModal;

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
    M.Dropdown.init(document.querySelectorAll('body > div.container > div > form > div > div > p:nth-child(12) > div > input'), {
        "coverTrigger": false,
        "closeOnClick": true,
    });

    // Modal init
    let modalElem = document.getElementById('member-actions-modal');
    memberActionsModal = M.Modal.init(modalElem, {'endingBottom': '5%'});

    // Tabs init
    M.Tabs.init(document.querySelectorAll('.tabs'));

    // Collapsible init
    M.Collapsible.init(document.querySelectorAll('.collapsible'), {});

    // Add spacebucks buttons
    let spacebucksButtons = document.getElementsByClassName("add-spacebucks");
    for (var i = 0; i < spacebucksButtons.length; i++) {
        spacebucksButtons[i].addEventListener('click', chargeCardForSpacebucks);
    }
});


function initSelects() {
    M.FormSelect.init(document.querySelectorAll('select'), {});
}

function resendWelcome() {
    $.ajax({
        url: resend_welcome_url,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            M.toast({html: data.message});
        },
        error: function (data) {
            M.toast({html: data.message});
        }
    });
}

function addToXero() {
    $.ajax({
        url: add_to_xero_url,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            M.toast({html: data.response});
        },
        error: function (data) {
            M.toast({html: data.response});
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
        url: state_url,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if (state) {
                state_url = active_url;
                document.getElementById("activate-member-button").classList.add("disabled");
                document.getElementById("activate-member-button").classList.add("hidden");
                document.getElementById("deactivate-member-button").classList.remove("disabled");
                document.getElementById("deactivate-member-button").classList.remove("hidden");
                if (document.getElementById("activate-member-button").innerText == "MAKE MEMBER") {
                    M.toast({html: data.response});
                } else {
                    M.toast({html: data.response});
                }
            } else {
                state_url = deactive_url;
                document.getElementById("activate-member-button").classList.remove("disabled");
                document.getElementById("activate-member-button").classList.remove("hidden");
                document.getElementById("deactivate-member-button").classList.add("disabled");
                document.getElementById("deactivate-member-button").classList.add("hidden");
                M.toast({html: data.response});
            }
            // not very DRY... ideally should be modularised a bit more...
            $.ajax({
                url: access_url,
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
                    M.toast({html: "unknown error 2 :( "});
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
let get_spacebucks_url;
let add_to_xero_url;

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
    add_to_xero_url = e.getAttribute("data-add_to_xero_url");
    get_spacebucks_url = e.getAttribute("data-get_spacebucks_url");
    document.getElementById('admin-member-modal-name').innerHTML = name;

    // get the edit profile form
    $.ajax({
        url: profile_url,
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
            M.toast({html: "unknown error while getting profile form :( "});

            let elem = document.getElementById("admin-edit-member-profile");
            elem.innerHTML = "";
        }
    });

    // get the access form
    $.ajax({
        url: access_url,
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
            M.toast({html: "unknown error while getting access form :( "});
            let elem = document.getElementById("admin-edit-member-access");
            elem.innerHTML = "";
        }
    });

    // get the member logs
    $.ajax({
        url: get_logs_url,
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
            M.toast({html: "unknown error while getting logs :( "});

            let elem = document.getElementById("admin-edit-member-logs");
            elem.innerHTML = "";
        }
    });

    // get the member spacebucks transactions
    $.ajax({
        url: get_spacebucks_url,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            let elem = document.getElementById("admin-edit-member-spacebucks");
            elem.innerHTML = data.body;

            // init the table
            let table = $('#spacebucksTable').DataTable({});
        },
        error: function () {
            M.toast({html: "unknown error while getting spacebucks data :( "});

            let elem = document.getElementById("admin-edit-member-spacebucks");
            elem.innerHTML = "";
        }
    });

    document.getElementById("activate-member-button").innerText = "Enable Access";
    document.getElementById("resend-welcome-button").classList.remove("hidden");
    document.getElementById("resend-welcome-button").classList.remove("hidden");
    if (member_state == "inactive") {
        document.getElementById("activate-member-button").classList.remove("disabled");
        document.getElementById("activate-member-button").classList.remove("hidden");
        document.getElementById("deactivate-member-button").classList.add("disabled");
        document.getElementById("deactivate-member-button").classList.add("hidden");
    } else if (member_state == "active") {
        document.getElementById("activate-member-button").classList.add("disabled");
        document.getElementById("activate-member-button").classList.add("hidden");
        document.getElementById("deactivate-member-button").classList.remove("disabled");
        document.getElementById("deactivate-member-button").classList.remove("hidden");
    } else if (member_state == "noob") {
        document.getElementById("activate-member-button").innerText = "Make Member";
        document.getElementById("activate-member-button").classList.remove("disabled");
        document.getElementById("activate-member-button").classList.remove("hidden");
        document.getElementById("deactivate-member-button").classList.add("disabled");
        document.getElementById("deactivate-member-button").classList.add("hidden");
        document.getElementById("resend-welcome-button").classList.add("hidden");
        document.getElementById("resend-to-xero-button").classList.add("hidden");
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
            M.toast({html: "unknown error 3 :( "});
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
        url: url,
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
            M.toast({html: "unknown error 4 :( "});
        }
    });
}

function revokeAccess(url, id) {
    $.ajax({
        url: url,
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
            M.toast({html: "unknown error 5 :( "});
        }
    });
}

function requestAccess(url) {
    $.ajax({
        url: url,
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
            M.toast({html: "Unknown error 6 :( "});
        }
    });
}

function unlockDoor(thing) {
    $.ajax({
        url: thing.getAttribute("data-url"),
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Door unlocked successfully."});
            }
            else {
                M.toast({html: "Error while trying to unlock door :("});
            }
        },
        error: function () {
            M.toast({html: "Unknown error while trying to unlock door :( "});
        }
    });
}

function lockDoor(thing) {
    $.ajax({
        url: thing.getAttribute("data-url"),
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Door locked successfully."});
            }
            else {
                M.toast({html: "Error while trying to lock door :("});
            }
        },
        error: function () {
            M.toast({html: "Unknown error while trying to lock door :( "});
        }
    });
}

function unlockInterlock(btn) {
    $.ajax({
        url: btn.getAttribute("data-url"),
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Interlock unlocked successfully."});
            }
            else {
                M.toast({html: "Error while trying to unlock interlock :("});
            }
        },
        error: function () {
            M.toast({html: "Unknown error while trying to unlock interlock :( "});
        }
    });
}

function lockInterlock(btn) {
    $.ajax({
        url: btn.getAttribute("data-url"),
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Interlock locked successfully."});
            }
            else {
                M.toast({html: "Error while trying to lock interlock :("});
            }
        },
        error: function () {
            M.toast({html: "Unknown error while trying to lock interlock :( "});
        }
    });
}

function addSpacebucks(url) {
    let amount = Math.round(document.getElementById("addAmountInput").value * 100);

    $.ajax({
        url: url + amount,
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Successfuly added spacebucks."});
            }
            else {
                M.toast({html: "Failed to add spacebucks :("});
            }
        },
        error: function () {
            M.toast({html: "Unknown error while trying to add spacebucks :( "});
        }
    });
}

function chargeCardForSpacebucks() {
    document.getElementById("spacebucks-progress-bar").classList.add("progress");

    $.ajax({
        url: this.getAttribute("data-url"),
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Successfuly charged your card."});
                setTimeout(() => {location = "/profile/spacebucks/manage/";}, 2000)
            }
            else {
                M.toast({html: "Failed to charge your card :("});
            }
        },
        error: function () {
            M.toast({html: "Unknown error while trying to charge your card :( "});
        }
    });
}