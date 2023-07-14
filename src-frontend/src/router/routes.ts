import mainMenu from 'pages/pageAndRouteConfig';
import { RouteRecordRaw } from 'vue-router';

const childRoutes: RouteRecordRaw[] = [];

const menuRoutes: RouteRecordRaw[] = mainMenu.map(
  (menuItem): RouteRecordRaw => {
    if (menuItem.children) {
      menuItem.children.map((child) => {
        childRoutes.push({
          path: child.to ? child.to : '/no-route', // this means we didn't get a path and shouldn't route there
          component: child.component
            ? child.component
            : () => import('pages/Error404.vue'),
          name: child.name,
          props: true,
          meta: {
            title: child.name,
            featureEnabledFlag: child.featureEnabledFlag,
            loggedIn: child.loggedIn,
            kiosk: child.kiosk,
            backButton: child.backButton,
            memberOnly: child.memberOnly,
            bgGradient: child.bgGradient,
          },
        });
      });

      return {
        path: menuItem.to ? menuItem.to : '/no-route', // this means we didn't get a path and shouldn't route there
        component: menuItem.component
          ? menuItem.component
          : () => import('pages/Error404.vue'),
        name: menuItem.name,
        props: true,
        meta: {
          title: menuItem.name,
          featureEnabledFlag: menuItem.featureEnabledFlag,
          loggedIn: menuItem.loggedIn,
          kiosk: menuItem.kiosk,
          backButton: menuItem.backButton,
          memberOnly: menuItem.memberOnly,
          bgGradient: menuItem.bgGradient,
        },
      };
    }

    return {
      path: menuItem.to ?? menuItem.name,
      component: menuItem.component
        ? menuItem.component
        : () => import('pages/Error404.vue'),
      name: menuItem.name,
      props: true,
      meta: {
        title: menuItem.name,
        featureEnabledFlag: menuItem.featureEnabledFlag,
        loggedIn: menuItem.loggedIn,
        kiosk: menuItem.kiosk,
        backButton: menuItem.backButton,
        memberOnly: menuItem.memberOnly,
        bgGradient: menuItem.bgGradient,
      },
    };
  }
);

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      ...menuRoutes,
      ...childRoutes,
      {
        path: '*',
        component: () => import('pages/Error404.vue'),
      },
    ],
  },
];

// Always leave this as last one
routes.push({
  path: '/:catchAll(.*)*',
  component: () => import('pages/Error404.vue'),
});

export default routes;
