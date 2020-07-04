import icons from '../icons';

const PageAndRouteConfig = [
  {
    icon: icons.signin, // specify the icon to use
    to: '/', // specify the URL route for this page
    name: 'rootIndex', // specify the name of this URL route
    loggedIn: false, // only allow access to logged in users if true or logged out users if false
    kiosk: true, // whether this page should show up in kiosk mode
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Login'), // which component to load as the page
  },
  {
    icon: icons.dashboard,
    to: '/dashboard',
    name: 'dashboard',
    loggedIn: true,
    kiosk: true,
    component: () => import('pages/Dashboard'),
  },
  {
    icon: icons.webcams,
    to: '/webcams',
    name: 'webcams',
    loggedIn: true,
    kiosk: true,
    component: () => import('pages/Webcams'),
  },
  {
    icon: icons.cogs,
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
        component: () => import('pages/AdminTools/Members'),
      },
      {
        icon: icons.meetings,
        to: '/manage/meetings',
        name: 'meetings',
        loggedIn: true,
        admin: true,
        component: () => import('pages/Meetings'),
      },
      {
        icon: icons.groups,
        to: '/manage/groups',
        name: 'groups',
        loggedIn: true,
        admin: true,
        component: () => import('pages/Error501'),
      },
      {
        icon: icons.doors,
        to: '/manage/doors',
        name: 'doors',
        loggedIn: true,
        admin: true,
        component: () => import('pages/AdminTools/Doors'),
      },
      {
        icon: icons.interlocks,
        to: '/manage/interlocks',
        name: 'interlocks',
        loggedIn: true,
        admin: true,
        component: () => import('pages/AdminTools/Interlocks'),
      },
      {
        icon: icons.kiosks,
        to: '/manage/kiosks',
        name: 'kiosks',
        loggedIn: true,
        admin: true,
        component: () => import('pages/Kiosks'),
      },
    ],
  },
  {
    icon: icons.tools,
    name: 'memberTools',
    loggedIn: true,
    kiosk: true,
    children: [
      {
        icon: icons.reportIssue,
        to: '/tools/issue',
        name: 'reportIssue',
        loggedIn: true,
        kiosk: true,
        component: () => import('pages/ReportIssue'),
      },
      {
        icon: icons.submitProxy,
        to: '/tools/proxy',
        name: 'proxy',
        loggedIn: true,
        kiosk: true,
        component: () => import('pages/Proxy'),
      },
      {
        icon: icons.groupMembers,
        to: '/tools/groups/',
        name: 'groupMembers',
        loggedIn: true,
        kiosk: true,
        component: () => import('pages/MemberGroups'),
      },
      {
        icon: icons.recentSwipes,
        to: '/tools/swipes/recent',
        name: 'recentSwipes',
        loggedIn: true,
        kiosk: true,
        component: () => import('pages/RecentSwipes'),
      },
      {
        icon: icons.lastSeen,
        to: '/tools/swipes/lastseen',
        name: 'lastSeen',
        loggedIn: true,
        kiosk: true,
        component: () => import('pages/LastSeen'),
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
        component: () => import('pages/Profile'),
      },
      {
        icon: icons.checkAccess,
        to: '/account/access',
        name: 'checkAccess',
        loggedIn: true,
        kiosk: true,
        component: () => import('pages/CheckAccess'),
      },
      {
        icon: icons.memberbucks,
        to: '/account/memberbucks/:dialog',
        defaultParams: { dialog: 'transactions' },
        name: 'memberbucks',
        loggedIn: true,
        component: () => import('pages/MemberBucks'),
      },
    ],
  },
  {
    icon: icons.signout,
    to: '/logout',
    name: 'logout',
    loggedIn: true,
    kiosk: true,
    component: () => import('pages/Logout'),
  },
  {
    icon: icons.signin,
    to: '/login',
    name: 'login',
    loggedIn: false,
    kiosk: true,
    component: () => import('pages/Login'),
  },
  {
    icon: icons.register,
    to: '/register',
    name: 'register',
    loggedIn: false,
    kiosk: true,
    component: () => import('pages/Registration'),
  },

  // These are endpoints that handle specific tasks and are not normally accessed.
  {
    icon: icons.signin, // specify the icon to use
    to: '/profile/password/reset/:resetToken', // specify the URL route for this page
    name: 'resetPassword', // specify the name of this URL route
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Login'), // which component to load as the page
  },
  {
    icon: icons.signin, // specify the icon to use
    to: '/error/403', // specify the URL route for this page
    name: 'Error403', // specify the name of this URL route
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Error403'), // which component to load as the page
  },
];

export default PageAndRouteConfig;
