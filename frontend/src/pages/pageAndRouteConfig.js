const PageAndRouteConfig = [
  {
    icon: 'fad fa-sign-in',
    to: '/',
    name: 'rootIndex',
    loggedIn: false,
    hiddenMenu: true,
    component: () => import('pages/Login.vue'),
  },
  {
    icon: 'fad fa-columns',
    to: '/dashboard',
    name: 'dashboard',
    loggedIn: true,
    component: () => import('pages/Dashboard.vue'),
  },
  {
    icon: 'fad fa-webcam',
    to: '/webcams',
    name: 'webcams',
    loggedIn: true,
    component: () => import('pages/Webcams.vue'),
  },
  {
    icon: 'fad fa-tools',
    name: 'memberTools',
    loggedIn: true,
    children: [
      {
        icon: 'fad fa-exclamation-triangle',
        to: '/tools/issue',
        name: 'reportIssue',
      },
      {
        icon: 'fad fa-box-ballot',
        to: '/tools/proxy',
        name: 'submitProxy',
      },
      {
        icon: 'fad fa-history',
        to: '/tools/swipes/recent',
        name: 'recentSwipes',
      },
      {
        icon: 'fad fa-user-clock',
        to: '/tools/swipes/lastseen',
        name: 'lastSeen',
      },
    ],
  },
  {
    icon: 'fad fa-user',
    name: 'membership',
    loggedIn: true,
    children: [
      {
        icon: 'fad fa-user',
        to: '/account/profile',
        name: 'profile',
      },
      {
        icon: 'fad fa-user-lock',
        to: '/account/access',
        name: 'checkAccess',
        component: () => import('pages/CheckAccess.vue'),
      },
      {
        icon: 'fad fa-wallet',
        to: '/account/memberbucks',
        name: 'manageMemberbucks',
      },
    ],
  },
  {
    icon: 'fad fa-sign-out',
    to: '/logout',
    name: 'logout',
    loggedIn: true,
    component: () => import('pages/Logout.vue'),
  },
  {
    icon: 'fad fa-sign-in',
    to: '/login',
    name: 'login',
    loggedIn: false,
    component: () => import('pages/Login.vue'),
  },
  {
    icon: 'fad fa-user-plus',
    to: '/register',
    name: 'register',
    loggedIn: false,
  },
];

export default PageAndRouteConfig;
