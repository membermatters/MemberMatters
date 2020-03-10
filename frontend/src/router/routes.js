import mainMenu from 'pages/pageAndRouteConfig';

const menuRoutes = mainMenu.map((menuItem) => {
  if (menuItem.children) {
    return {
      path: menuItem.to ? menuItem.to : '/no-route', // this means we didn't get a path and shouldn't route there
      component: menuItem.component
        ? menuItem.component
        : () => import('pages/Error404.vue'),
      name: menuItem.name ? menuItem.name : null,
      meta: { title: menuItem.name, loggedIn: menuItem.loggedIn },
      children: menuItem.children.map((subMenuItem) => ({
        path: subMenuItem.to,
        component: subMenuItem.component
          ? subMenuItem.component
          : () => import('pages/Error404.vue'),
        name: subMenuItem.name ? subMenuItem.name : null,
        meta: { title: subMenuItem.name, loggedIn: menuItem.loggedIn },
      })),
    };
  }

  return {
    path: menuItem.to,
    component: menuItem.component
      ? menuItem.component
      : () => import('pages/Error404.vue'),
    name: menuItem.name ? menuItem.name : null,
    meta: { title: menuItem.name, loggedIn: menuItem.loggedIn },
  };
});

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      ...menuRoutes,
      {
        path: '*',
        component: () => import('pages/Error404.vue'),
      },
    ],
  },
];

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue'),
  });
}

export default routes;
