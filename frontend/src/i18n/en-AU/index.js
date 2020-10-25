// This is an object containing every piece of user visible text used for localisation (currently
// only Australian English is supported)

export default {
  menuLink: {
    rootIndex: 'Dashboard',
    dashboard: 'Dashboard',
    webcams: 'Webcams',
    login: 'Login',
    resetPassword: 'Reset Password',
    logout: 'Logout',
    register: 'Register',
    registerSuccess: 'Successfully Registered',
    plans: 'Membership Plans',

    adminTools: 'Admin Tools',
    groupMembers: 'Group Members',
    meetings: 'Meetings',
    members: 'Members',
    manageMember: 'Manage Member',
    groups: 'Groups',
    doors: 'Doors',
    manageDoor: 'Manage Door',
    manageInterlock: 'Manage Interlock',
    interlocks: 'Interlocks',
    kiosks: 'Kiosks',

    memberTools: 'Member Tools',
    reportIssue: 'Report Issue',
    proxy: 'Proxy Votes',
    recentSwipes: 'Recent Swipes',
    lastSeen: 'Last Seen',
    membership: 'Membership',
    profile: 'Profile',
    checkAccess: 'Check Access',
    memberbucks: 'Spacebucks',

    Error404: 'Page Not Found',
  },
  dashboard: {
    usefulResources: 'Useful Resources',
    statistics: 'Statistics',
    quickActions: 'Quick Actions',
    signinSuccess: 'Successfully signed you in. Please remember to sign out when you leave.',
    signoutError: 'There was a problem signing you out. Please contact the management committee if this problem persists.',
    signinError: 'There was a problem signing you in. Please contact the management committee if this problem persists.',
  },
  error: {
    error: 'Error',
    loginFailed: 'Your username or password was incorrect.',
    accountAlreadyExists: 'Sorry, that email address has already been used.',
    screenNameAlreadyExists: 'Sorry, that screen name has already been used.',
    requestFailed: 'Sorry, we\'re having trouble performing that action. Please try again later.',
    pageNotFound: 'Page not found',
    noValue: 'No Value',
    400: ' Sorry, there was an error with your request. (Error 400)',
    401: ' Sorry, you need to be logged in to access this page. (Error 401)',
    403: ' Sorry, you don\'t have permission to access this page. (Error 403)',
    404: ' Sorry, that page could not be found. (Error 404)',
    500: ' Sorry, there was a server error. Please try again later. (Error 500)',
    501: ' Sorry, this feature hasn\'t been implemented yet. Please try again later. (Error 501)',
  },
  logoutPage: {
    logoutSuccess: 'Logout successful.',
    logoutFailed: 'There was an error logging out. Please refresh the page and try again.',
  },
  webcams: {
    pageDescription: 'This page shows our public webcams, updated every minute for your convenience.',
  },
  about: {
    title: 'About MemberMatters',
    description: 'This is an open source, full featured membership portal. It is designed for '
    + 'HSBNE (Hackerspace Brisbane). It was created by Jaimyn Mayer, with a little help from some '
    + 'HSBNE members.',
    linkText: 'on GitHub',
  },
  button: {
    submit: 'Submit',
    ok: 'Ok',
    reset: 'Reset',
    cancel: 'Cancel',
    close: 'Close',
    connect: 'Connect',
    disconnect: 'Disconnect',
    add: 'Add',
    tools: 'Tools',
    rebootDevice: 'Restart Device',
    manage: 'Manage',
    actions: 'Actions',
    unlockDoor: 'Unlock Door',
    remove: 'Remove',
  },
  loginCard: {
    login: 'Login',
    resetPassword: 'Reset Password',
    loginSuccess: 'Login Successful',
    registerHere: 'Register Here',
    notAMember: 'Not a member? ',
    loginToContinue: 'Please login to continue',
    forgottenPassword: 'Forgot your password?',
    forgottenPasswordDescription: 'Please enter your email address and click submit. You will '
      + 'receive an email with further instructions.',
    emailLabel: 'Email address',
    resetSuccess: 'Success. Check your email for further instructions.',
    resetFailed: 'There was a problem resetting your password. Check your email address or '
      + 'try again later.',
    resetInvalid: 'Your password reset link is invalid.',
    resetConfirm: 'Your password has been reset.',
    resetNotConfirm: 'There was a problem resetting your password.',
    backToLogin: 'Back to login page',
    unverifiedEmail: 'Your email address is not verified. We just sent you another link so please try again.',
  },
  changePasswordCard: {
    pageTitle: 'Change Password',
    success: 'Your new password was saved successfully.',
    fail: 'There was an error saving your new password.',
  },
  validation: {
    invalidEmail: 'Please enter a valid email.',
    invalidPassword: 'Please enter a valid password.',
    invalidPhone: 'Please enter a valid phone number.',
    passwordNotMatch: 'Sorry, but your passwords don\'t match.',
    cannotBeEmpty: 'This field cannot be empty.',
    futureDate: 'Date must be today or in the future.',
  },
  access: {
    pageDescription: 'Your access permissions for doors and interlocks are shown below. Please '
      + 'contact the management committee if you believe you should have access to something that '
      + 'you don\'t.',
    inactive: 'Your membership is currently inactive. This may affect your access.',
    authorised: 'Authorised',
    unauthorised: 'Unauthorised',
    door: 'Door',
    doors: 'Doors',
    interlock: 'Interlock',
    interlocks: 'Interlocks',
    defaultAccess: 'Members have access by default',
    maintenanceLockout: 'Maintenance lockout is enabled',
    playTheme: 'Play theme on swipe',
    exemptSignin: 'Exempt from site sign in requirement (if enabled)',
    hiddenToMembers: 'Hidden from members on their access permissions screen',
  },
  lastseen: {
    pageDescription: 'Here is a list of when each member last tapped their card.',
  },
  recentSwipes: {
    pageDescription: 'Here is a list of the last 50 swipes from doors and interlocks.',
    inProgress: 'In Progress',
    timedOut: 'TIMED OUT',
  },
  reportIssue: {
    pageDescription: 'Report an issue',
    success: 'Your issue was reported successfully.',
    fail: 'There was a problem reporting your issue.',
  },
  memberGroups: {
    pageDescription: 'You can browse our list of groups and see each group\'s membership and '
      + 'quorum.',
    activeMembers: 'Active Members',
    quorum: 'Quorum',
  },
  form: {
    saved: 'Saved',
    error: 'Error Saving',
    pageDescription: 'Edit any of the fields below and they will be automatically saved.',
    noResults: 'No Results',
    allFieldsRequired: 'All fields are required.',

    email: 'Email',
    rfidCard: 'RFID Card',
    firstName: 'First Name',
    lastName: 'Last Name',
    phone: 'Phone',
    mobile: 'Mobile Number',
    screenName: 'Screen / Nickname',
    date: 'Date',
    dateTime: 'Date & Time',
    chair: 'Chair',
    meetingType: 'Meeting Type',
    meetingDate: 'Meeting Date',
    name: 'Name',
    playTheme: 'Play Theme Song',
    ipAddress: 'IP Address',
    lastSeen: 'Last Seen',
    password: 'Password',
    registrationDate: 'Registration Date',
    state: 'State',
    last_induction: 'Last Induction',
    memberType: 'Membership Type',
    id: 'Member ID',
    admin: 'Admin User',
  },
  digitalId: {
    title: 'Digital ID',
    fullName: 'Full Name',
    memberState: 'Member Status',
    memberId: 'Member ID',
    memberSince: 'Member Since',
  },
  meetings: {
    memberName: 'Member Name',
    proxy: 'Proxy',
    noProxies: 'No Proxy Votes Found',
    dateAssigned: 'Date Assigned',
    proxyVotes: 'Proxy Votes',
    attendees: 'Attendees',
    noAttendees: 'No Attendees Found',
  },
  meetingForm: {
    pageDescription: 'Fill out the form below to create a new meeting.',
    editDescription: 'Fill out the form below to update the meeting.',
    newMeeting: 'New Meeting',
    updatePastMeeting: "Sorry, you can't update this field for a past meeting.",
    noUpdateMeetingType: "Sorry, you can't update this field for an existing meeting.",
    meeting: 'Meeting',
    success: 'Successfully created meeting.',
    editSuccess: 'Successfully updated meeting.',
    fail: 'Failed to create meeting, try again later.',
    editMeeting: 'Edit Meeting',
    deleteMeeting: 'Are you sure you want to delete this meeting?',
  },
  proxyForm: {
    pageDescription: 'This form allows you to give someone else your vote for a specific '
      + 'meeting. Always check with the other person before submission.',
    proxyBody: 'I, {memberName}, of {memberCity}, being a member of the association, appoint {proxyName} of {proxyCity} as my proxy to vote for me on my behalf at the {meetingName} meeting, to be held on the day of {meetingDate} and at any adjournment of the meeting.',
    proxySignature: 'Signed by {memberName} on this day of {currentDate}. ',
    proxyTo: 'To {siteOwner}:',

    noMeetings: 'There are no meetings scheduled.',

    meeting: 'Meeting',
    yourCity: 'Your city',
    proxyName: 'Proxy\'s name',
    proxyCity: 'Proxy\'s city',

    newProxy: 'New Proxy',
    editTitle: 'Edit Proxy',

    deleteTitle: 'Confirm Proxy Deletion',
    delete: 'Are you sure you want to delete this proxy?',
  },
  memberbucks: {
    currentBalance: 'Current Balance',
    lastPurchase: 'Last Purchase',
    addFunds: 'Add Funds',
    addFundsDescription: 'Click one of the buttons above to top up your account. This will '
      + 'immediately charge your saved card ending in {savedCard}.',
    noSavedBilling: 'Sorry, but you don\'t have any valid billing methods. Please add a new '
      + 'billing method by clicking the button below.',
    manageBilling: 'Manage Billing',
    addCard: 'Add Card',
    addCardDescription: 'To add a new card please fill out the form. We do not store your credit card information (other than the last 4 digits and expiry) as our payment processor collects this for us.',
    addCardError: 'There was an error adding your card. Please try again later.',
    saveCard: 'Save Card',
    savedCardTitle: 'Saved Card',
    savedCardDescription: 'Your saved card is shown below.',
    removeCard: 'Remove Card',
    removeCardError: 'There was an error removing your card. Please try again later.',
    addFundsSuccess: 'Successfully added funds to your memberbucks account.',
  },
  loginRfidCard: {
    swipeCard: 'Tap Card',
    failed: 'Sorry we couldn\'t log you in. Please check your card.',
  },
  settings: {
    title: 'Kiosk Settings',
    description: 'You\'ve opened the kiosk settings. If this was an accident, please close this '
      + 'window.',
    rfidScanner: {
      title: 'RFID Scanner',
      hostname: 'Hostname',
      connectionStatus: 'Connection Status',
      connected: 'Connected',
      disconnected: 'Disconnected',
    },
    other: {
      title: 'Other',
      reloadPage: 'Reload Page',
    },
  },
  kiosk: {
    editForm: 'Edit Kiosk',
    authorised: 'Authorised',
    updated: 'Successfully updated kiosk.',
    fail: 'Sorry, there was a problem updating the kiosk.',
    delete: 'Are you sure you want to delete this kiosk?',
    nodata: 'There are no kiosks in the system.',
    kioskId: 'Kiosk ID',
  },
  statistics: {
    memberCount: 'Member Count',
    onSite: ' on site right now.',
    memberList: 'Members On Site',
  },
  entityType: 'Association',
  groups: 'Groups',
  members: 'Members',
  group: 'Group',
  member: 'Member',
  failed: 'Action failed',
  success: 'Action was successful',
  warning: 'Warning',
  confirmAction: 'Confirm Action',
  confirmRemove: 'Are you sure you want to remove this?',
  edit: 'Edit',
  delete: 'Delete',
  dataRefreshWarning: 'There was an error fetching new data. Any data that you see may not be up '
    + 'to date.',
  adminTools: {
    emailAddresses: 'Email Addresses',
    exportCsv: 'Export CSV',
    exportOptions: 'Export Options',
    filterOptions: 'Filter Options',
    all: 'All',
    active: 'Active',
    inactive: 'Inactive',
    new: 'New',
    enableAccess: 'Enable Access',
    disableAccess: 'Disable Access',
    sendWelcomeEmail: 'Send Welcome Email',
    manageMember: 'Manage Member',
    makeMember: 'Make Member',
    makeMemberSuccess: 'Successfully made into member and sent welcome email.',
    makeMemberError: 'Unknown error while making into member.',
    makeMemberErrorEmail: 'Error, couldn\'t send welcome email.',
    makeMemberErrorExists: 'It looks like this person is already a member. To see their profile, change the filter to "all" members.',
    makeMemberSuccessDescription: 'This person was made into a member and emailed their first invoice and welcome information. To see their profile, change the filter to "all" members.',
    sendWelcomeEmailSuccess: 'Successfully sent the welcome email.',
    createInvoiceSuccess: 'Successfully created the new invoice.',
    confirmInvoice: 'Are you sure you want to create a new invoice for this member?',
    confirmInvoiceEmail: 'Would you like to email the new invoice to this member after it\'s created?',

    access: 'Access',
    accessDescription: 'Tap an icon below to change a member\'s access.',
    log: 'Log',
    mainProfile: 'Main Profile',
    otherAttributes: 'Other Attributes',
    memberDates: 'Important Dates',
    lastInduction: 'Last Induction',
    lastUpdatedProfile: 'Last Updated Profile',
    registrationDate: 'Registration Date',
    lastSeen: 'Last Seen',
    openXero: 'Open In Xero',
    createInvoice: 'Create Invoice',
  },
  doors: {
    nodata: 'There are no doors in the system.',
    name: 'Door Name',
    description: 'Door Description',
    ipAddress: 'Door IP Address',
    remove: 'Remove this door',
  },
  interlocks: {
    nodata: 'There are no interlocks in the system.',
    name: 'Interlock Name',
    description: 'Interlock Description',
    ipAddress: 'Interlock IP Address',
    remove: 'Remove this interlock',
  },
  registrationCard: {
    register: 'Register An Account',
    alreadyAMember: 'Already a member? ',
    loginHere: 'Login Here',
    registrationComplete: 'Registration complete. Please check your email and click the link to verify your email address.',
  },
  verifyEmail: {
    error: 'There was a problem verifying your email address. We just sent you another link so please try again.',
    success: 'Your email was verified. You can now login.',
  },
};
