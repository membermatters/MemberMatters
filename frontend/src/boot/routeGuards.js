import { Platform } from 'quasar';

export default ({ router, store }) => {
  router.beforeEach((to, from, next) => {
    // if we're in kiosk mode disallow certain pages
    if (Platform.is.electron) {
      if (!to.meta.kiosk) {
        next({ name: 'dashboard' });
      }
    }

    // Check if the user must be logged in to access the route
    if (to.meta.loggedIn === true) {
      if (store.getters['profile/loggedIn'] === true) next();
      else {
        next({ name: 'login' });
      }
    }

    // If we're already logged in and try to hit the login page go to dashboard
    if ((to.path === '/login' || to.path === '/') && store.getters['profile/loggedIn'] === true) {
      next({ name: 'dashboard' });
    }

    next();
  });
};
