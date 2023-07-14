import icons from '../icons';

const PageAndRouteConfig = [
  {
    icon: icons.signin, // specify the icon to use
    to: '/', // specify the URL route for this page
    name: 'rootIndex', // specify the name of this URL route
    loggedIn: false, // only allow access to logged in users if true or logged out users if false
    kiosk: true, // whether this page should show up in kiosk mode
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Login.vue'), // which component to load as the page
    bgGradient: true,
  },
  {
    icon: icons.signin, // specify the icon to use
    to: '/registersuccess', // specify the URL route for this page
    name: 'registerSuccess', // specify the name of this URL route
    loggedIn: false, // only allow access to logged in users if true or logged out users if false
    kiosk: false, // whether this page should show up in kiosk mode
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/RegisterSuccess.vue'), // which component to load as the page
    bgGradient: true,
  },
  {
    icon: icons.dashboard,
    to: '/dashboard',
    name: 'dashboard',
    loggedIn: true,
    kiosk: true,
    component: () => import('pages/Dashboard.vue'),
  },
  {
    icon: icons.webcams,
    to: '/webcams',
    name: 'webcams',
    loggedIn: true,
    kiosk: true,
    featureEnabledFlag: 'enableWebcams',
    component: () => import('pages/Webcams.vue'),
  },
  {
    icon: icons.admintools,
    name: 'adminTools',
    loggedIn: true,
    admin: true,
    children: [
      {
        icon: icons.manageMembers,
        to: '/manage/members',
        name: 'members',
        loggedIn: true,
        admin: true,
        component: () => import('pages/AdminTools/Members.vue'),
      },
      {
        icon: icons.members,
        to: '/manage/members/:memberId',
        name: 'manageMember',
        loggedIn: true,
        admin: true,
        hiddenMenu: true,
        backButton: '/manage/members',
        component: () => import('pages/AdminTools/ManageMember.vue'),
      },
      {
        icon: icons.meetings,
        to: '/manage/meetings',
        name: 'meetings',
        loggedIn: true,
        admin: true,
        component: () => import('pages/Meetings.vue'),
      },
      {
        icon: icons.plans,
        to: '/manage/tiers',
        name: 'manageTiers',
        loggedIn: true,
        admin: true,
        component: () => import('pages/AdminTools/ManageTiers.vue'),
      },
      {
        icon: icons.members,
        to: '/manage/tiers/:planId',
        name: 'manageTier',
        loggedIn: true,
        admin: true,
        hiddenMenu: true,
        backButton: '/manage/tiers',
        component: () => import('pages/AdminTools/ManageTier.vue'),
      },
      {
        icon: icons.members,
        to: '/manage/plans/:planId',
        name: 'managePlan',
        loggedIn: true,
        admin: true,
        hiddenMenu: true,
        backButton: true,
        component: () => import('pages/AdminTools/ManageTier.vue'),
      },
      {
        icon: icons.interlocks,
        to: '/manage/devices',
        name: 'devices',
        loggedIn: true,
        admin: true,
        component: () => import('pages/AdminTools/Devices.vue'),
      },
      {
        icon: icons.kiosks,
        to: '/manage/kiosks',
        name: 'kiosks',
        loggedIn: true,
        admin: true,
        component: () => import('pages/Kiosks.vue'),
      },
    ],
  },
  {
    icon: icons.tools,
    name: 'memberTools',
    loggedIn: true,
    kiosk: true,
    memberOnly: true,
    children: [
      {
        icon: icons.reportIssue,
        to: '/tools/issue',
        name: 'reportIssue',
        loggedIn: true,
        kiosk: true,
        component: () => import('pages/ReportIssue.vue'),
      },
      {
        icon: icons.submitProxy,
        to: '/tools/proxy',
        name: 'proxy',
        loggedIn: true,
        kiosk: true,
        memberOnly: true,
        featureEnabledFlag: 'enableProxyVoting',
        component: () => import('pages/Proxy.vue'),
      },
      {
        icon: icons.recentSwipes,
        to: '/tools/swipes/recent',
        name: 'recentSwipes',
        loggedIn: true,
        kiosk: true,
        memberOnly: true,
        component: () => import('pages/RecentSwipes.vue'),
      },
      {
        icon: icons.lastSeen,
        to: '/tools/swipes/lastseen',
        name: 'lastSeen',
        loggedIn: true,
        kiosk: true,
        memberOnly: true,
        component: () => import('pages/LastSeen.vue'),
      },
    ],
  },
  {
    icon: icons.membership,
    name: 'membership',
    loggedIn: true,
    kiosk: true,
    children: [
      {
        icon: icons.profile,
        to: '/account/profile',
        name: 'profile',
        loggedIn: true,
        component: () => import('pages/Profile.vue'),
      },
      {
        icon: icons.checkAccess,
        to: '/account/access',
        name: 'checkAccess',
        loggedIn: true,
        kiosk: true,
        component: () => import('pages/CheckAccess.vue'),
      },
      {
        icon: icons.memberbucks,
        featureEnabledFlag: 'enableMemberBucks',
        to: '/account/memberbucks/:dialog',
        defaultParams: { dialog: 'transactions' },
        name: 'memberbucks',
        loggedIn: true,
        component: () => import('pages/MemberBucks.vue'),
      },
      {
        icon: icons.billing,
        featureEnabledFlag: 'enableStripe',
        to: '/account/billing',
        name: 'billing',
        loggedIn: true,
        component: () => import('pages/Billing.vue'),
      },
      {
        icon: icons.plans,
        featureEnabledFlag: 'enableMembershipPayments',
        to: '/account/membership-plan',
        name: 'membershipPlan',
        loggedIn: true,
        component: () => import('pages/MembershipPlan.vue'),
      },
    ],
  },
  {
    icon: icons.signout,
    to: '/logout',
    name: 'logout',
    loggedIn: true,
    kiosk: true,
    component: () => import('pages/Logout.vue'),
    bgGradient: true,
  },
  {
    icon: icons.signin,
    to: '/login',
    name: 'login',
    loggedIn: false,
    kiosk: true,
    component: () => import('pages/Login.vue'),
    bgGradient: true,
  },
  {
    icon: icons.register,
    to: '/register',
    name: 'register',
    loggedIn: false,
    kiosk: true,
    component: () => import('pages/Registration.vue'),
    bgGradient: true,
  },

  // These are endpoints that handle specific tasks and are not directly accessed.
  {
    icon: icons.signin, // specify the icon to use
    to: '/profile/password/reset/:resetToken', // specify the URL route for this page
    name: 'resetPassword', // specify the name of this URL route
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Login.vue'), // which component to load as the page
  },
  {
    icon: icons.register, // specify the icon to use
    to: '/profile/email/:verifyToken/verify', // specify the URL route for this page
    name: 'verifyEmail', // specify the name of this URL route
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/VerifyEmail.vue'), // which component to load as the page
  },
  {
    icon: icons.signin, // specify the icon to use
    to: '/error/403', // specify the URL route for this page
    name: 'Error403', // specify the name of this URL route
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Error403.vue'), // which component to load as the page
  },
  {
    icon: icons.signin, // specify the icon to use
    to: '/error/403MemberOnly', // specify the URL route for this page
    name: 'Error403MemberOnly', // specify the name of this URL route
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Error403MemberOnly.vue'), // which component to load as the page
  },
  {
    icon: icons.signin, // specify the icon to use
    to: '/error/404', // specify the URL route for this page
    name: 'Error404', // specify the name of this URL route
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Error404.vue'), // which component to load as the page
  },
];

export default PageAndRouteConfig;
