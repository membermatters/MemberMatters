const MainMenuConf = [
  {
    title: 'Dashboard',
    icon: 'fad fa-columns',
    to: '/dashboard',
    name: 'dashboard',
  },
  {
    title: 'Public Webcams',
    icon: 'fad fa-webcam',
    to: '/webcams',
    name: 'webcams',
  },
  {
    title: 'Member Tools',
    icon: 'fad fa-tools',
    children: [
      {
        title: 'Report Issue',
        icon: 'fad fa-exclamation-triangle',
        to: '/tools/issue',
        name: 'reportIssue',
      },
      {
        title: 'Submit Proxy Vote',
        icon: 'fad fa-box-ballot',
        to: '/tools/proxy',
        name: 'submitProxy',
      },
      {
        title: 'Recent Swipes',
        icon: 'fad fa-history',
        to: '/tools/swipes/recent',
        name: 'recentSwipes',
      },
      {
        title: 'Last Seen',
        icon: 'fad fa-user-clock',
        to: '/tools/swipes/lastseen',
        name: 'lastSeen',
      },
    ],
  },
  {
    title: 'Membership',
    icon: 'fad fa-user',
    children: [
      {
        title: 'Profile',
        icon: 'fad fa-user',
        to: '/account/profile',
        name: 'profile',
      },
      {
        title: 'Access',
        icon: 'fad fa-user-lock',
        to: '/account/access',
        name: 'checkAccess',
      },
      {
        title: 'Memberbucks',
        icon: 'fad fa-wallet',
        to: '/account/memberbucks',
        name: 'manageMemberbucks',
      },
    ],
  },
  {
    title: 'Logout',
    icon: 'fad fa-sign-out',
    to: '/logout',
    name: 'logout',
  },
];

export default MainMenuConf;
