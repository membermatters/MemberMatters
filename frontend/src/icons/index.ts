const pro = typeof process.env.proIcons === "undefined" || process.env.proIcons;

export default {
  /**
   * This object defines the font awesome classes for each icon. It will also detect if pro icons
   * are enabled (which is by default) or disabled and return the appropriate class. You will need
   * to follow the font awesome instructions for adding your secret key to a .npmrc file to download
   * the required pro libraries.
   */
  sadFace: pro ? "fad fa-frown" : "fas fa-frown",

  // all of these are for pages
  dashboard: pro ? "fad fa-columns" : "fas fa-columns",
  webcams: pro ? "fad fa-webcam" : "fas fa-camera",

  menu: pro ? "fal fa-bars" : "fas fa-bars",
  backButton: pro ? "fal fa-arrow-left" : "fas fa-arrow-left",
  settings: pro ? "fal fa-cog" : "fas fa-cog",
  manageMembers: pro ? "fad fa-users-cog" : "fas fa-file-alt",
  meetings: pro ? "fad fa-clipboard-list" : "fas fa-clipboard-list",
  groups: pro ? "fad fa-user-tag" : "fas fa-user-tag",
  plans: pro ? "fad fa-box-usd" : "fas fa-money-bill-wave",
  dollar: pro ? "fad fa-dollar-sign" : "fas fa-dollar-sign",
  doors: pro ? "fad fa-door-closed" : "fas fa-door-closed",
  interlocks: pro ? "fad fa-plug" : "fas fa-plug",
  kiosks: pro ? "fad fa-desktop" : "fas fa-desktop",

  tools: pro ? "fad fa-tools" : "fas fa-tools",
  admintools: pro ? "fad fa-toolbox" : "fas fa-toolbox",
  reportIssue: pro ? "fad fa-exclamation-triangle" : "fas fa-exclamation-triangle",
  submitProxy: pro ? "fad fa-box-ballot" : "fas fa-file-alt",
  groupMembers: pro ? "fad fa-user-friends" : "fas fa-user-friends",
  recentSwipes: pro ? "fad fa-history" : "fas fa-history",
  lastSeen: pro ? "fad fa-user-clock" : "fas fa-user-clock",
  membership: pro ? "fad fa-user" : "fas fa-user",
  profile: pro ? "fad fa-user" : "fas fa-user",
  checkAccess: pro ? "fad fa-user-lock" : "fas fa-user-lock",
  memberbucks: pro ? "fad fa-wallet" : "fas fa-wallet",
  donate: pro ? "fad fa-donate" : "fas fa-donate",

  signout: pro ? "fad fa-sign-out" : "fas fa-sign-out-alt",
  signin: pro ? "fad fa-sign-in" : "fas fa-sign-in-alt",
  register: pro ? "fad fa-user-plus" : "fas fa-user-plus",

  search: pro ? "fad fa-search" : "fas fa-search",
  warning: pro ? "fad fa-exclamation-triangle" : "fas fa-exclamation-triangle",
  clock: pro ? "fad fa-clock" : "fas fa-clock",
  calendar: pro ? "fad fa-calendar" : "fas fa-calendar",

  comment: pro ? "fad fa-comment-alt-lines" : "fas fa-comment-alt",
  close: pro ? "fad fa-times" : "fas fa-times",
  success: pro ? "fad fa-check" : "fas fa-check",
  fail: pro ? "fad fa-times" : "fas fa-times",
  add: pro ? "fad fa-plus-circle" : "fas fa-plus-circle",
  addAlternative: pro ? "fad fa-plus" : "fas fa-plus",
  remove: pro ? "fad fa-trash" : "fas fa-trash",
  up: pro ? "fad fa-chevron-down" : "fas fa-chevron-down",
  down: pro ? "fad fa-chevron-up" : "fas fa-chevron-up",
  edit: pro ? "fad fa-pencil" : "fas fa-pencil-alt",
  delete: pro ? "fad fa-trash-alt" : "fas fa-trash-alt",
  billing: pro ? "fad fa-credit-card" : "fas fa-credit-card",
  visibility: pro ? "fad fa-eye" : "fas fa-eye",
  visibilityOff: pro ? "fad fa-eye-slash" : "fas fa-eye-slash",

  rfid: pro ? "fad fa-wifi" : "fas fa-wifi",
  rfidSlash: pro ? "fad fa-wifi-slash" : "fas fa-times",

  members: pro ? "fad fa-users" : "fas fa-users",
  membersOnSite: pro ? "fad fa-address-book" : "fas fa-address-book",
  export: pro ? "fad fa-archive" : "fas fa-archive",
  email: pro ? "fad fa-mail-bulk" : "fas fa-mail-bulk",
  reboot: pro ? "fad fa-sync" : "fas fa-sync",
  unlock: pro ? "fad fa-unlock" : "fas fa-unlock",
  induction: pro ? "fad fa-user-hard-hat" : "fas fa-user-hard-hat",
  accessCard: pro ? "fad fa-id-card" : "fas fa-user-id-card",
  doorOpen: pro ? "fad fa-door-open" : "fas fa-door-open",
  interlock: pro ? "fad fa-tools" : "fas fa-tools"
};
