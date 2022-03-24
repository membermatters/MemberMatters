// This is an object containing every piece of user visible text used for localisation (currently
// only Australian English is supported)

export default {
  menuLink: {
    rootIndex: "Dashboard",
    dashboard: "Dashboard",
    webcams: "Webcams",
    login: "Login",
    resetPassword: "Reset Password",
    logout: "Logout",
    register: "Register",
    registerSuccess: "Successfully Registered",
    manageTiers: "Membership Plans",
    manageTier: "Manage Tier",

    adminTools: "Admin Tools",
    meetings: "Meetings",
    members: "Members",
    manageMember: "Manage Member",
    doors: "Doors",
    manageDoor: "Manage Door",
    manageInterlock: "Manage Interlock",
    manageDevice: "Manage Device",
    interlocks: "Interlocks",
    devices: "Devices",
    kiosks: "Kiosks",

    memberTools: "Member Tools",
    reportIssue: "Report Issue",
    proxy: "Proxy Votes",
    recentSwipes: "Recent Swipes",
    lastSeen: "Last Seen",
    membership: "Membership",
    billing: "Billing Method",
    profile: "Profile",
    checkAccess: "Access Permissions",
    memberbucks: "Spacebucks",
    membershipPlan: "Membership Plan",

    Error404: "Page Not Found",
    Error403: "Error 403",
  },
  dashboard: {
    usefulResources: "Member Resources",
    quickCards: "Quick Cards",
    quickActions: "Quick Actions",
    signedIn:
      "You are currently signed in. If you are no longer on site, please sign out.",
    signinSuccess:
      "Successfully signed you in. Please remember to sign out when you leave.",
    signoutError:
      "There was a problem signing you out. Please report an issue if this problem persists.",
    signinError:
      "There was a problem signing you in. Please report an issue if this problem persists.",
    signIn: "On-site Check In",
    signOut: "On-site Check Out",
  },
  error: {
    error: "Error",
    contactUs: "Please contact us for help if you continue to see this error.",
    loginFailed: "Your username or password was incorrect.",
    accountAlreadyExists: "Sorry, that email address has already been used.",
    screenNameAlreadyExists: "Sorry, that screen name has already been used.",
    requestFailed:
      "Sorry, we're having trouble performing that action. Please try again later.",
    pageNotFound: "Page not found",
    noValue: "No Value",
    noData: "No records found",
    stripeNotConfigured:
      "There was an error completing that action as Stripe is not configured.",
    postmarkNotConfigured:
      "There was an error completing that action as Postmark is not configured correctly.",
    stripeNotConfiguredFeature:
      "Sorry, but this organisation has not configured Stripe so you are unable to use this feature.",
    400: " Sorry, there was an error with your request. (Error 400)",
    401: " Sorry, you need to be logged in to access this page. (Error 401)",
    403: " Sorry, you don't have permission to access this page. (Error 403)",
    "403MemberOnly":
      "Sorry, you must be an active member to access this page. (Error 403)",
    404: " Sorry, that page could not be found. (Error 404)",
    500: " Sorry, there was a server error. Please try again later. (Error 500)",
    501: " Sorry, this feature hasn't been implemented yet. Please try again later. (Error 501)",
  },
  logoutPage: {
    logoutSuccess: "Logout successful.",
    logoutFailed:
      "There was an error logging out. Please refresh the page and try again.",
  },
  webcams: {
    pageDescription:
      "This page shows our public webcams, updated every minute for your convenience.",
  },
  about: {
    title: "About MemberMatters",
    description:
      "This is an open source, full featured membership portal. It is designed for " +
      "managing makerspaces. It's primary author is Jaimyn Mayer.",
    linkText: "on GitHub",
  },
  button: {
    submit: "Submit",
    ok: "Ok",
    reset: "Reset",
    cancel: "Cancel",
    close: "Close",
    connect: "Connect",
    disconnect: "Disconnect",
    add: "Add",
    tools: "Tools",
    rebootDevice: "Restart Device",
    manage: "Manage",
    actions: "Actions",
    unlockDoor: "Unlock Door",
    remove: "Remove",
    select: "Select",
    continue: "Continue",
    back: "Back",
    contactUs: "Contact Us",
  },
  loginCard: {
    login: "Login",
    resetPassword: "Reset Password",
    loginSuccess: "Login Successful",
    registerHere: "Register Here",
    notAMember: "Not a member? ",
    loginToContinue: "Please login to continue",
    forgottenPassword: "Forgot your password?",
    forgottenPasswordDescription:
      "Please enter your email address and click submit. You will " +
      "receive an email with further instructions.",
    emailLabel: "Email address",
    resetSuccess: "Success. Check your email for further instructions.",
    resetFailed:
      "There was a problem resetting your password. Check your email address or " +
      "try again later.",
    resetInvalid: "Your password reset link is invalid.",
    resetConfirm: "Your password has been reset.",
    resetNotConfirm: "There was a problem resetting your password.",
    backToLogin: "Back to login page",
    unverifiedEmail:
      "Your email address is not verified. We just sent you another link so please try again.",
  },
  changePasswordCard: {
    pageTitle: "Change Password",
    success: "Your new password was saved successfully.",
    fail: "There was an error saving your new password.",
  },
  validation: {
    invalidEmail: "Please enter a valid email.",
    invalidPassword: "Please enter a valid password.",
    invalidPhone: "Please enter a valid phone number.",
    passwordNotMatch: "Sorry, but your passwords don't match.",
    cannotBeEmpty: "This field cannot be empty.",
    futureDate: "Date must be today or in the future.",
    tooMany: "Sorry, the maximum is {number}.",
  },
  access: {
    pageDescription:
      "Your access permissions for doors and interlocks are shown below. Please " +
      "report an issue if you believe you should have access to something that " +
      "you don't.",
    inactive:
      "Your membership is currently inactive. This may affect your access.",
    authorised: "Authorised",
    unauthorised: "Unauthorised",
    door: "Door",
    doors: "Doors",
    noDoors: "There are no doors in the system.",
    interlock: "Interlock",
    interlocks: "Interlocks",
    noInterlocks: "There are no interlocks in the system.",
    defaultAccess: "Members have access by default",
    maintenanceLockout: "Maintenance lockout is enabled",
    playTheme: "Play theme on swipe",
    exemptSignin: "Exempt from site sign in requirement (if enabled)",
    hiddenToMembers: "Hidden from members on their access permissions screen",
  },
  lastseen: {
    pageDescription:
      "Here is a list of when each member last tapped their card.",
  },
  recentSwipes: {
    pageDescription:
      "Here is a list of the last 300 swipes from doors and interlocks.",
    inProgress: "In Progress",
    timedOut: "TIMED OUT",
  },
  reportIssue: {
    pageDescription: "Report an issue",
    success: "Your issue was reported successfully.",
    fail: "There was a problem reporting your issue.",
  },
  form: {
    saved: "Saved",
    error: "Error Saving",
    pageDescription:
      "Edit any of the fields below and they will be automatically saved.",
    noResults: "No Results",
    allFieldsRequired: "All fields are required.",
    featured: "Featured?",
    email: "Email",
    rfidCard: "RFID Card",
    firstName: "First Name",
    lastName: "Last Name",
    phone: "Phone",
    mobile: "Mobile Number",
    screenName: "Screen / Nickname",
    date: "Date",
    dateTime: "Date & Time",
    chair: "Chair",
    meetingType: "Meeting Type",
    meetingDate: "Meeting Date",
    name: "Name",
    description: "Description",
    playTheme: "Play Theme Song",
    ipAddress: "IP Address",
    lastSeen: "Last Seen",
    password: "Password",
    registrationDate: "Registration Date",
    state: "State",
    last_induction: "Last Induction",
    memberType: "Membership Type",
    id: "Member ID",
    admin: "Admin User",
    visibleToMembers: "Visible to members?",
    stripeId: "Stripe ID",
    currency: "Currency",
    cost: "Cost",
    intervalCount: "Interval Count",
    interval: "Interval Period",
  },
  digitalId: {
    title: "Digital ID",
    fullName: "Full Name",
    memberState: "Member Status",
    memberId: "Member ID",
    memberSince: "Member Since",
    inactiveMember: "This person is not an active member.",
  },
  meetings: {
    memberName: "Member Name",
    proxy: "Proxy",
    noProxies: "No Proxy Votes Found",
    dateAssigned: "Date Assigned",
    proxyVotes: "Proxy Votes",
    attendees: "Attendees",
    noAttendees: "No Attendees Found",
  },
  meetingForm: {
    pageDescription: "Fill out the form below to create a new meeting.",
    editDescription: "Fill out the form below to update the meeting.",
    newMeeting: "New Meeting",
    updatePastMeeting: "Sorry, you can't update this field for a past meeting.",
    noUpdateMeetingType:
      "Sorry, you can't update this field for an existing meeting.",
    meeting: "Meeting",
    success: "Successfully created meeting.",
    editSuccess: "Successfully updated meeting.",
    fail: "Failed to create meeting, try again later.",
    editMeeting: "Edit Meeting",
    deleteMeeting: "Are you sure you want to delete this meeting?",
  },
  proxyForm: {
    pageDescription:
      "This form allows you to give someone else your vote for a specific " +
      "meeting. Always check with the other person before submission.",
    proxyBody:
      "I, {memberName}, of {memberCity}, being a member of the association, appoint {proxyName} of {proxyCity} as my proxy to vote for me on my behalf at the {meetingName} meeting, to be held on the day of {meetingDate} and at any adjournment of the meeting.",
    proxySignature: "Signed by {memberName} on this day of {currentDate}. ",
    proxyTo: "To {siteOwner}:",

    noMeetings: "There are no meetings scheduled.",

    meeting: "Meeting",
    yourCity: "Your city",
    proxyName: "Proxy's name",
    proxyCity: "Proxy's city",

    newProxy: "New Proxy",
    editTitle: "Edit Proxy",

    deleteTitle: "Confirm Proxy Deletion",
    delete: "Are you sure you want to delete this proxy?",
  },
  memberbucks: {
    currentBalance: "Current Balance",
    lastPurchase: "Last Purchase",
    addFunds: "Add Funds",
    addFundsDescription:
      "Click one of the buttons above to top up your account. This will " +
      "immediately charge your saved card ending in {savedCard}.",
    noSavedBilling:
      "Sorry, but you don't have any valid billing methods. Please add a new " +
      "billing method by clicking the button below.",
    manageBilling: "Manage Billing",
    selectToContinue: "Select your billing method to continue.",
    addCard: "Add Card",
    addCardDescription:
      "To add a new card please fill out the form. We do not store your credit card information (other than the last 4 digits and expiry) as our payment processor collects this for us.",
    addCardError:
      "There was an error adding your card. Please try again later.",
    saveCard: "Save Card",
    savedCardTitle: "Saved Card",
    savedCardDescription: "Your saved card is shown below.",
    removeCard: "Remove Card",
    removeCardError:
      "There was an error removing your card. Please try again later.",
    addFundsSuccess: "Successfully added funds to your memberbucks account.",
    donateFunds: "Make Payment",
    quickAdd: "Quick Add",
    totalAmount: "Total Amount",
    donateFundsDescription:
      'Click the quick add buttons or enter an amount above, then click "donate funds". You can use this to pay for things that don\'t have a payment terminal.',
    donateFundsSuccess: "Successfully donated funds.",
    donateFundsError:
      "There was an error donating your funds, check your balance or try again later.",
    cardExpiry: "Card Expiry",
    last4: "Card Last 4 Digits",
  },
  loginRfidCard: {
    swipeCard: "Tap Card",
    failed: "Sorry we couldn't log you in. Please check your card.",
  },
  settings: {
    title: "Kiosk Settings",
    description:
      "You've opened the kiosk settings. If this was an accident, please close this " +
      "window.",
    rfidScanner: {
      title: "RFID Scanner",
      hostname: "Hostname",
      connectionStatus: "Connection Status",
      connected: "Connected",
      disconnected: "Disconnected",
    },
    other: {
      title: "Other",
      reloadPage: "Reload Page",
    },
  },
  kiosk: {
    editForm: "Edit Kiosk",
    authorised: "Authorised",
    updated: "Successfully updated kiosk.",
    fail: "Sorry, there was a problem updating the kiosk.",
    delete: "Are you sure you want to delete this kiosk?",
    nodata: "There are no kiosks in the system.",
    kioskId: "Kiosk ID",
  },
  statistics: {
    memberCount: "Member Count",
    onSite: " on site right now.",
    memberList: "Members On Site",
  },
  entityType: "Association",
  members: "Members",
  member: "Member",
  failed: "Action failed",
  success: "Action was successful",
  warning: "Warning",
  confirm: "Confirm",
  confirmAction: "Confirm Action",
  confirmRemove: "Are you sure you want to remove this?",
  edit: "Edit",
  delete: "Delete",
  dataRefreshWarning:
    "There was an error fetching new data. Any data that you see may not be up " +
    "to date.",
  progress: "Progress: {percent}%",
  adminTools: {
    emailAddresses: "Email Addresses",
    exportCsv: "Export CSV",
    exportOptions: "Export Options",
    filterOptions: "Filter",
    all: "All",
    active: "Active",
    inactive: "Inactive",
    new: "New",
    accountOnly: "Account only",
    enableAccess: "Enable Access",
    disableAccess: "Disable Access",
    sendWelcomeEmail: "Send Welcome Email",
    manageMember: "Manage Member",
    makeMember: "Make Member",
    makeMemberSuccess: "Successfully made into member and sent welcome email.",
    makeMemberError: "Unknown error while making into member.",
    makeMemberErrorEmail: "Error, couldn't send welcome email.",
    makeMemberErrorExists:
      'It looks like this person is already a member. To see their profile, change the filter to "all" members.',
    makeMemberSuccessDescription:
      'This person was made into a member and emailed their first invoice and welcome information. To see their profile, change the filter to "all" members.',
    sendWelcomeEmailSuccess: "Successfully sent the welcome email.",
    createInvoiceSuccess: "Successfully created the new invoice.",
    confirmInvoice:
      "Are you sure you want to create a new invoice for this member?",
    confirmInvoiceEmail:
      "Would you like to email the new invoice to this member after it's created?",

    access: "Access",
    accessDescription: "Tap an icon below to change a member's access.",
    log: "Log",
    stats: "Stats",
    mainProfile: "Main Profile",
    otherAttributes: "Other Attributes",
    memberDates: "Important Dates",
    lastInduction: "Last Induction",
    lastUpdatedProfile: "Last Updated Profile",
    registrationDate: "Registration Date",
    lastSeen: "Last Seen",
    openXero: "Open In Xero",
    createInvoice: "Create Invoice",
    billing: "Billing",
    memberState: "Member State",
    memberbucksTransactions: "Memberbucks Transactions",
    subscriptionInfo: "Subscription Info",
    subscriptionStatus: "Stripe Subscription Status",
    billingInfo: "Billing Info",
    billingCycleAnchor: "Billing Cycle Anchor",
    cancelAt: "Cancels At",
    cancelAtPeriodEnd: "Cancels At Period End",
    currentPeriodEnd: "Current Period End",
    startDate: "Start Date",
    noSubscription: "No subscription was found for this member.",
  },
  doors: {
    nodata: "There are no doors in the system.",
    name: "Door Name",
    description: "Door Description",
    ipAddress: "Door IP Address",
    remove: "Remove this door",
  },
  paymentPlans: {
    title: "Membership Plans",
    nodata: "There are no Membership Plans available.",
    name: "Plan Name",
    description: "Membership Plan Description",
    recurringDescription: "Bill for this plan every:",
    remove: "Remove this Membership Plan",
    add: "Add a new Membership Plan",
    success: "Successfully added a new Membership Plan.",
    fail: "Failed to add a new Membership Plan.",
    select: "Plan",
    selected: "Selected Membership Plan",
    confirmSelection: "Confirm",
    selectToContinue: "Select a plan to continue.",
    noPlans: "There are no billing plans available for this membership plan.",
    dueToday: "Due Today: {amount}",
    intervalDescription: "{amount} {currency} every {intervalCount} {interval}",
    interval: {
      day: "day",
      week: "week",
      month: "month",
      year: "year",
    },
    intervalPlurals: {
      day: "days",
      week: "weeks",
      month: "months",
      year: "years",
    },
    signupFailed: "Signup failed",
    signupSuccess: "Signup success",
    signupSuccessDescription:
      "Your payment was processed successfully. This page will refresh in a moment.",
    cancelButton: "Cancel my membership",
    cancelConfirmDescription:
      "Are you sure you want to cancel your membership? Your membership will remain active until the end of your current billing period. You can resume it at any point before the end of your current billing period.",
    cancelSuccessDescription:
      "Your plan was cancelled. This page will reload in a moment.",
    cancelFailed: "Cancel failed",
    resumeFailed: "Resume failed",
    resumeButton: "Resume membership",
    cancelling: "Your membership is about to be cancelled",
    cancellingDescription:
      "Your Membership Plan and membership are scheduled to be cancelled on {date}. If you'd like to resume your plan (listed above), please click below.",
    renewalDate: "Renewal Date",
    signupDate: "Signup Date",
    subscriptionInfo: "Subscription Info",
    accountOnlyWarning:
      "Your profile is currently set to 'account only'. This is because you skipped this process last time. You're welcome to continue using this account for our online services, or you can signup to become a member below. ",
    profileAccountOnlyWarning:
      "Your profile is currently set to 'account only'. This is because you skipped the signup process and did not become a member. You're welcome to continue using this account for our online services, or you can signup to become a member from the menu ('Membership' > 'Membership Plan').",
  },
  signup: {
    induction: "Induction",
    requiredSteps:
      "You must complete the following steps before your membership application can be submitted.",
    completeInduction: "Complete an induction",
    completedInduction: "Induction completed",
    registerAccessCard: "Register your access card",
    completeInductionDescription:
      "Complete your induction via Canvas by clicking the button below. Keep this page open and come back to it once you're finished.",
    emailWarning:
      "Please use the same email address you used during signup ({email}) or your progress won't sync.",
    waitingCompletion: "Waiting for completion...",
    accessCard: "Access Card",
    accessCardNumber: "Access Card Number",
    assignAccessCard: "Access Card",
    assignAccessCardDescription: "Please enter your access card number below.",
    assignAccessCardWarning:
      "Double check before continuing as you will need to contact us to change it.",
    collectAccessCardDescription:
      "Thanks for completing all of the required steps. The final thing you need to do is pop in during our open " +
      "hours to collect your access card. Please bring photo ID with you.",
    submitted: "Membership application submitted",
    submittedDescription:
      "Your membership application has been submitted and you are now a 'member applicant'. Your membership will be officially accepted after 7 days, but we have granted site access immediately. You will receive an email confirming that your access card has been enabled. If for some reason your membership is rejected within this period, you will receive an email with further information.",
    continueToDashboard: "Continue to dashboard",
    error: "Error submitting membership application",
    errorDescription:
      "We're very sorry but there was an unexpected error when submitting your application. Please contact us at {email} for assistance.",
    errorMessageDescription: "Please include the error message below:",
    requirementsNotMet: "Requirements not met:",
    subscriptionFailed:
      "Sorry, but there was a problem creating your subscription. Please check the card you used had enough funds, try again, or contact us for help.",
  },
  tiers: {
    disabledFeature:
      "Warning! This feature is disabled. You can make changes but your users won't be able to use it.",
    select: "Tier",
    selectToContinue: "Select a membership plan to continue.",
    noTiers: "There are no membership plans available right now.",
    selected: "Selected Membership Plan",
    nodata: "There are no membership plans in the system.",
    name: "Tier Name",
    description: "Tier Description",
    remove: "Remove this tier",
    add: "Add a new tier",
    becomeMember: "Become a member",
    confirm:
      "Please confirm your selected membership plan and billing plan. By continuing you agree to pay for your selected plan using the provided credit card. Your first payment will be collected today, and future payments of {intervalDescription}.",
    confirmDelay:
      "Your membership application will be submitted after you complete the next steps.",
    finish: "Pay & Continue",
    plansFrom: "From {plan}",
    skipSignup: "Skip Signup (if you just want an account)",
  },
  tierForm: {
    fail: "Failed to add a new tier.",
    success: "Successfully added new tier.",
  },
  interlocks: {
    nodata: "There are no interlocks in the system.",
    name: "Interlock Name",
    description: "Interlock Description",
    ipAddress: "Interlock IP Address",
    remove: "Remove this interlock",
  },
  registrationCard: {
    register: "Register An Account",
    alreadyAMember: "Already a member? ",
    loginHere: "Login Here",
    registrationComplete:
      "Registration complete. Please check your email and click the link to verify your email address.",
  },
  verifyEmail: {
    error:
      "There was a problem verifying your email address. We just sent you another link so please try again.",
    success: "Your email was verified. You will be logged in shortly.",
  },
};
