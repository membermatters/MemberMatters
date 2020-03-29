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
  webcams: pro ? 'fad fa-webcam' : 'fal fa-webcam',

  cogs: pro ? 'fad fa-cogs' : 'fal fa-cogs',
  members: pro ? 'fad fa-users-cog' : 'fal fa-users-cog',
  meetings: pro ? 'fad fa-clipboard-list' : 'fal fa-clipboard-list',
  groups: pro ? 'fad fa-user-tag' : 'fal fa-user-tag',
  doors: pro ? 'fad fa-door-closed' : 'fal fa-door-closed',
  interlocks: pro ? 'fad fa-plug' : 'fal fa-plug',

  tools: pro ? 'fad fa-tools' : 'fal fa-tools',
  reportIssue: pro ? 'fad fa-exclamation-triangle' : 'fal fa-exclamation-triangle',
  submitProxy: pro ? 'fad fa-box-ballot' : 'fal fa-box-ballot',
  groupMembers: pro ? 'fad fa-user-friends' : 'fal fa-user-friends',
  recentSwipes: pro ? 'fad fa-history' : 'fal fa-history',
  lastSeen: pro ? 'fad fa-user-clock' : 'fal fa-user-clock',
  membership: pro ? 'fad fa-user' : 'fal fa-user',
  profile: pro ? 'fad fa-user' : 'fal fa-user',
  checkAccess: pro ? 'fad fa-user-lock' : 'fal fa-user-lock',
  memberbucks: pro ? 'fad fa-wallet' : 'fal fa-wallet',

  signout: pro ? 'fad fa-sign-out' : 'fal fa-sign-out',
  signin: pro ? 'fad fa-sign-in' : 'fal fa-sign-in',
  register: pro ? 'fad fa-user-plus' : 'fal fa-user-plus',

  search: pro ? 'fad fa-search' : 'fal fa-search',
  warning: pro ? 'fad fa-exclamation-triangle' : 'fal fa-exclamation-triangle',
  clock: pro ? 'fad fa-clock' : 'fal fa-clock',
  calendar: pro ? 'fad fa-calendar' : 'fal fa-calendar',

  comment: pro ? 'fad fa-comment-alt-lines' : 'fal fa-comment-alt-lines',

  close: pro ? 'fad fa-times' : 'fal fa-times',

  success: pro ? 'fad fa-check' : 'fal fa-check',
  fail: pro ? 'fad fa-times' : 'fal fa-times',
  add: pro ? 'fad fa-plus-circle' : 'fal fa-plus-circle',
  remove: pro ? 'fad fa-times-circle' : 'fal fa-times-circle',
  up: pro ? 'fad fa-chevron-down' : 'fal fa-chevron-down',
  down: pro ? 'fad fa-chevron-up' : 'fal fa-chevron-up',
};
