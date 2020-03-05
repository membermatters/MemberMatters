const MainMenuConf = [
  {
    title: 'Dashboard',
    icon: 'fad fa-columns',
    to: { name: 'index' },
  },
  {
    title: 'Public Webcams',
    icon: 'fad fa-webcam',
    to: '#',
  },
  {
    title: 'Member Tools',
    icon: 'fad fa-tools',
    to: '#',
    children: [
      {
        title: 'Report Issue',
        icon: 'fad fa-exclamation-triangle',
        to: '#',
      },
      {
        title: 'Submit Proxy',
        icon: 'fad fa-person-carry',
        to: '#',
      },
      {
        title: 'Recent Swipes',
        icon: 'fad fa-history',
        to: '#',
      },
      {
        title: 'Last Seen',
        icon: 'fad fa-user-clock',
        to: '#',
      },
    ],
  },
  {
    title: 'Profile',
    icon: 'fad fa-user',
    to: '#',
    children: [
      {
        title: 'Profile',
        icon: 'fad fa-user',
        to: '#',
      },
      {
        title: 'Access',
        icon: 'fad fa-user-lock',
        to: '#',
      },
      {
        title: 'Spacebucks',
        icon: 'fad fa-wallet',
        to: '#',
      },
    ],
  },
  {
    title: 'Logout',
    icon: 'fad fa-sign-out',
    to: '#',
  },
];

export default MainMenuConf;
