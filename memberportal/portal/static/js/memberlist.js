let memberActionsModal;

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
let generate_invoice_url;
let xero_account_id;

let can_send_cause_emails = false;
let can_manage_access = false;
let can_disable_members = false;
let can_see_members_personal_details = false;
let can_see_members_spacebucks = false;
let can_see_members_logs = false;
let can_manage_access_devices = false;
let can_manage_causes = false;
let can_generate_invoice = false;

function resendWelcome() {
    if (confirm('Are you sure you want to resend the welcome email?') === false) {
        M.toast({html: "Cancelled :o"});
        return false
    }

    document.getElementById("btn-loader").classList.add("progress");
    $.ajax({
        url: resend_welcome_url,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            document.getElementById("btn-loader").classList.remove("progress");
            console.log(data.message);
            M.toast({html: data.message});
        },
        error: function (data) {
            document.getElementById("btn-loader").classList.remove("progress");
            console.log(data.message);
            M.toast({html: data.message});
        }
    });
}

function generateInvoice() {
    if (can_generate_invoice) {
        if (confirm('Are you sure you want to generate a new invoice? The due date will be set to the first of next month.') === false) {
            M.toast({html: "Cancelled :o"});
            return false
        }

        if (confirm('Would you like to send the invoice via email?') === true) {
            generate_invoice_url += "email/"
        }

        document.getElementById("btn-loader").classList.add("progress");
        $.ajax({
            url: generate_invoice_url,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                document.getElementById("btn-loader").classList.remove("progress");
                console.log(data.message);
                M.toast({html: data.message});
            },
            error: function (data) {
                document.getElementById("btn-loader").classList.remove("progress");
                console.log(data.message);
                M.toast({html: data.message});
            }
        });
    }
}

function addToXero() {
    if (confirm('Are you sure you want to try to re-add them to Xero?') === false) {
        M.toast({html: "Cancelled :o"});
        return false
    }

    document.getElementById("btn-loader").classList.add("progress");
    $.ajax({
        url: add_to_xero_url,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            document.getElementById("btn-loader").classList.remove("progress");
            console.log(data.message);
            M.toast({html: data.message});
        },
        error: function (data) {
            document.getElementById("btn-loader").classList.remove("progress");
            console.log(data.message);
            M.toast({html: data.message});
        }
    });
}

function setState(state) {
    if (can_disable_members) {
        document.getElementById("btn-loader").classList.add("progress");
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
                if (data.success) {
                    document.getElementById("btn-loader").classList.remove("progress");
                    console.log(data.message);
                    M.toast({html: data.message});
                    document.getElementById("resend-welcome-button").classList.remove("hidden");
                    if (can_generate_invoice) {
                        document.getElementById("generate-invoice-button").classList.remove("hidden");
                    }
                    try {
                        document.querySelectorAll("#admin-member-modal-name > span")[0].innerHTML = "";
                    } catch (err) {
                        // do nothing
                    }

                    if (state && member_state !== "noob") {
                        document.getElementById("activate-member-button").classList.add("hidden");
                        document.getElementById("activate-member-button").classList.add("disabled");
                        document.getElementById("deactivate-member-button").classList.remove("disabled");
                        document.getElementById("deactivate-member-button").classList.remove("hidden");
                    } else {
                        document.getElementById("activate-member-button").innerText = "Enable Access";
                        document.getElementById("activate-member-button").setAttribute("data-tooltip", "Enable Access");
                        document.getElementById("activate-member-button").classList.remove("disabled");
                        document.getElementById("activate-member-button").classList.remove("hidden");
                        document.getElementById("deactivate-member-button").classList.add("disabled");
                        document.getElementById("deactivate-member-button").classList.add("hidden");
                    }

                    // refresh the access tab
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
                            M.toast({html: "There was an error processing the request 2. :("});
                            document.getElementById("btn-loader").classList.remove("progress");
                        }
                    });
                } else {
                    M.toast({html: data.message});
                    document.getElementById("btn-loader").classList.remove("progress");

                }

            },
            error: function (data) {
                document.getElementById("btn-loader").classList.remove("progress");
                console.log(data.message);
                M.toast({html: "There was an error processing the request. :("});
            }
        });
    }
}

function openMemberActionsModal(e) {
    name = e.getAttribute("data-name");
    member_state = e.getAttribute("data-state");
    member_id = e.getAttribute("id");
    profile_url = e.getAttribute("data-url");
    access_url = e.getAttribute("data-access_url");
    active_url = e.getAttribute("data-active_url");
    deactive_url = e.getAttribute("data-deactive_url");
    resend_welcome_url = e.getAttribute("data-resend_welcome_url");
    generate_invoice_url = e.getAttribute("data-generate_invoice_url");
    get_logs_url = e.getAttribute("data-get_logs_url");
    add_to_xero_url = e.getAttribute("data-add_to_xero_url");
    get_spacebucks_url = e.getAttribute("data-get_spacebucks_url");
    xero_account_id = e.getAttribute("data-xero_account_id");

    document.getElementById('admin-member-modal-name').innerHTML = name;
    let xeroButton = document.getElementById("resend-to-xero-button");
    let openXeroButton = document.getElementById("admin-member-modal-open-xero");

    if (name.indexOf("NOT IN XERO") > 0 && member_state !== "noob") {
        xeroButton.style.display = "inline-block";
        openXeroButton.style.display = "none";
    } else {
        xeroButton.style.display = "none";
        openXeroButton.style.display = "inline-block";
        openXeroButton.setAttribute("href", "https://go.xero.com/Contacts/View/" + xero_account_id)
    }

    if (can_see_members_personal_details) {
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
    }

    if (can_manage_access) {
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
    }

    if (can_see_members_logs) {
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
    }

    if (can_see_members_spacebucks) {
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
                table.order([2, 'desc']).draw();
            },
            error: function () {
                M.toast({html: "unknown error while getting spacebucks data :( "});

                let elem = document.getElementById("admin-edit-member-spacebucks");
                elem.innerHTML = "";
            }
        });
    }

    if (can_disable_members) {
        let activeButton = document.getElementById("activate-member-button");
        let deactiveButton = document.getElementById("deactivate-member-button");
        let resendWelcomeButton = document.getElementById("resend-welcome-button");
        let xeroButton = document.getElementById("resend-to-xero-button");
        let generateInvoiceButton = document.getElementById("generate-invoice-button");

        activeButton.innerText = "Enable Access";
        activeButton.setAttribute("data-tooltip", "Enable Site Access");
        resendWelcomeButton.classList.remove("hidden");
        resendWelcomeButton.classList.remove("hidden");
        xeroButton.classList.remove("hidden");

        if (member_state === "inactive") {
            activeButton.classList.remove("disabled");
            activeButton.classList.remove("hidden");
            deactiveButton.classList.add("disabled");
            deactiveButton.classList.add("hidden");
            if (can_generate_invoice) {
                generateInvoiceButton.classList.remove("hidden");
                generateInvoiceButton.classList.remove("disabled");
            }

        } else if (member_state === "active") {
            activeButton.classList.add("disabled");
            activeButton.classList.add("hidden");
            deactiveButton.classList.remove("disabled");
            deactiveButton.classList.remove("hidden");
            if (can_generate_invoice) {
                generateInvoiceButton.classList.remove("hidden");
                generateInvoiceButton.classList.remove("disabled");
            }
        } else if (member_state === "noob") {
            activeButton.innerText = "Make Member";
            activeButton.setAttribute("data-tooltip", "Send welcome email, add to xero, and create first invoice.");
            activeButton.classList.remove("disabled");
            activeButton.classList.remove("hidden");
            deactiveButton.classList.add("disabled");
            deactiveButton.classList.add("hidden");
            resendWelcomeButton.classList.add("hidden");
            xeroButton.classList.add("hidden");
            if (can_generate_invoice) {
                generateInvoiceButton.classList.add("hidden");
                generateInvoiceButton.classList.add("disabled");
            }
        }
    }

    memberActionsModal.open();
}

$("#member-actions-modal").on("submit", ".member-edit-form", function () {
    if (can_see_members_personal_details) {
        let form = $(this);

        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid === true) {
                    M.toast({html: "Saved successfully :D"});
                    let elem = document.getElementById("admin-edit-member-profile");
                    elem.innerHTML = data.html_form;
                    setTimeout(function () {
                        initSelects();
                    }, 0);
                } else {
                    M.toast({html: "Error saving data. Probably duplicate RFID or email."});
                    let elem = document.getElementById("admin-edit-member-profile");
                    elem.innerHTML = data.html_form;
                    setTimeout(function () {
                        initSelects();
                    }, 0);
                }
            },
            error: function () {
                M.toast({html: "Unknown server error 3 :( "});
            }
        });
        return false;
    }
});

function addSpacebucks(url) {
    if (can_see_members_spacebucks) {
        if (confirm('Are you sure you want to add Spacebucks?') === false) {
            M.toast({html: "Cancelled :o"});
            return false
        }

        let amount = Math.round(document.getElementById("addAmountInput").value * 100);

        $.ajax({
            url: url + amount,
            type: 'get',
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    M.toast({html: "Successfuly added spacebucks."});
                } else {
                    M.toast({html: "Failed to add spacebucks :("});
                }
            },
            error: function () {
                M.toast({html: "Unknown error while trying to add spacebucks :( "});
            }
        });
    }
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
                M.toast({html: "Access Granted 🔓"});
            } else {
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
                M.toast({html: "Access Revoked 🔒"});
            } else {
                M.toast({html: "Error :( " + response.reason});
            }
        },
        error: function () {
            M.toast({html: "unknown error 5 :( "});
        }
    });
}