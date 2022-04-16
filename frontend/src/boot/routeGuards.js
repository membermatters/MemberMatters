import { Platform, Dialog } from "quasar";
import i18n from "boot/i18n";

export default ({ router, store }) => {
  router.beforeEach((to, from, next) => {
    // if we're in kiosk mode disallow certain pages
    if (Platform.is.electron) {
      if (!to.meta.kiosk) {
        return next({ name: "dashboard" });
      }
    }

    if (
      store.getters["profile/profile"]?.memberStatus === "Needs Induction" &&
      to.name !== "membershipPlan" &&
      store.getters["config/features"]?.enableMembershipPayments &&
      to.meta.admin !== true
    ) {
      console.warn("Needs Induction2");
      Dialog.create({
        title: i18n.t("error.error"),
        message: i18n.t("error.403MemberOnly"),
      });
      return;
    }

    // Check if the user must be logged in to access the route
    if (to.meta.loggedIn === true) {
      if (store.getters["profile/loggedIn"] === true) return next();
      else {
        return next({
          name: "login",
          query: {
            nextUrl: to.fullPath,
          },
        });
      }
    }

    // Check if the user must be an admin to access the route
    if (to.meta.admin === true) {
      if (store.getters["profile/profile"].permissions.admin === true)
        return next();
      else {
        return next({ name: "Error403" });
      }
    }

    // check if the user must be a member
    if (
      to.meta.memberOnly &&
      store.getters["profile/profile"].memberStatus !== "Active"
    )
      return next({ name: "Error403MemberOnly" });

    // if we are authenticating via SSO then don't update the route unless we're registering
    if (!from.query.sso || to.name === "register") {
      return next();
    }
  });

  router.afterEach(() => {
    if (typeof ga !== "undefined") {
      ga("send", "pageview");
    }
  });

  router.onError((error) => {
    if (/loading chunk \d* failed./i.test(error.message)) {
      window.location.reload();
    }
  });
};
