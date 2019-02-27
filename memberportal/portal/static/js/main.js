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
    M.FormSelect.init(document.querySelectorAll('#id_income_bracket'), {"closeOnClick": true});

    // Modal init
    memberActionsModal = M.Modal.init(document.getElementById('member-actions-modal'), {'endingBottom': '5%'});
    M.Modal.init(document.getElementById('aboutModal'), {});

    // Tabs init
    M.Tabs.init(document.querySelectorAll('.tabs'));

    // Collapsible init
    M.Collapsible.init(document.querySelectorAll('.collapsible'), {});

    // Tooltips init
    M.Tooltip.init(document.querySelectorAll('.tooltipped'), {});

    // Add spacebucks buttons
    let spacebucksButtons = document.getElementsByClassName("add-spacebucks");
    for (var i = 0; i < spacebucksButtons.length; i++) {
        spacebucksButtons[i].addEventListener('click', chargeCardForSpacebucks);
    }
});


function initSelects() {
    M.FormSelect.init(document.querySelectorAll('select'), {});
}

function deleteCause(btn) {
    $.get(btn.getAttribute("data-url"), function (data) {
        location.reload();
    });
}

function bumpDoor(thing) {
    $.ajax({
        url: thing.getAttribute("data-url"),
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Door bumped successfully."});
            }
            else {
                M.toast({html: "Error: " + response.message});
            }
        },
        error: function () {
            M.toast({html: "Unknown server error while trying to bump door :( "});
        }
    });
}

function chargeCardForSpacebucks() {
    if (confirm('Are you sure you want to add Spacebucks?') === false) {
        M.toast({html: "Cancelled :("});
        return false
    }

    document.getElementById("spacebucks-progress-bar").classList.add("progress");

    $.ajax({
        url: this.getAttribute("data-url"),
        type: 'get',
        dataType: 'json',
        success: function (response) {
            if (response.success) {
                M.toast({html: "Successfuly charged your card."});
                setTimeout(() => {
                    location = "/profile/spacebucks/manage/";
                }, 2000)
            }
            else {
                M.toast({html: "Failed to charge your card :("});
            }
        },
        error: function () {
            document.getElementById("spacebucks-progress-bar").classList.remove("progress");
            M.toast({html: "Unknown error while trying to charge your card :( "});
        }
    });
}