// eslint-disable-next-line eqeqeq
const pro = typeof process.env.proIcons === 'undefined' || process.env.proIcons;

export default {
  /**
   * This object defines the font awesome classes for each icon. It will also detect if pro icons
   * are enabled (which is by default) or disabled and return the appropriate class. You will need
   * to follow the font awesome instructions for adding your secret key to a .npmrc file to download
   * the required pro libraries.
   */
  sadFace: pro ? 'fad fa-frown' : 'fal fa-frown',

  // all of these are for pages
  login: pro ? 'fad fa-sign-in' : 'fal fa-sign-in',
  dashboard: pro ? 'fad fa-columns' : 'fal fa-columns',
  webcams: pro ? 'fad fa-webcam' : 'far fa-webcam',
  tools: pro ? 'fad fa-tools' : 'far fa-tools',
  reportIssue: pro ? 'fad fa-exclamation-triangle' : 'far fa-exclamation-triangle',
  submitProxy: pro ? 'fad fa-box-ballot' : 'far fa-box-ballot',
  recentSwipes: pro ? 'fad fa-history' : 'far fa-history',
  lastSeen: pro ? 'fad fa-user-clock' : 'far fa-user-clock',
  membership: pro ? 'fad fa-user' : 'far fa-user',
  profile: pro ? 'fad fa-user' : 'far fa-user',
  checkAccess: pro ? 'fad fa-user-lock' : 'far fa-user-lock',
  memberbucks: pro ? 'fad fa-wallet' : 'far fa-wallet',

  signout: pro ? 'fad fa-sign-out' : 'far fa-sign-out',
  signin: pro ? 'fad fa-sign-in' : 'far fa-sign-in',
  register: pro ? 'fad fa-user-plus' : 'far fa-user-plus',

  search: pro ? 'fad fa-search' : 'far fa-search',
};
