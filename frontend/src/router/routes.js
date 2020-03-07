import mainMenu from '../layouts/MainMenu.conf';

const menuRoutes = mainMenu.map((menuItem) => {
  if (menuItem.children) {
    return {
      path: menuItem.to ? menuItem.to : '/no-route', // this means we didn't get a path and shouldn't route there
      component: menuItem.component
        ? menuItem.component
        : () => import('pages/Error404.vue'),
      name: menuItem.name ? menuItem.name : null,
      meta: { title: menuItem.title },
      children: menuItem.children.map((subMenuItem) => ({
        path: subMenuItem.to,
        component: subMenuItem.component
          ? subMenuItem.component
          : () => import('pages/Error404.vue'),
        name: subMenuItem.name ? subMenuItem.name : null,
        meta: { title: subMenuItem.title },
      })),
    };
  }

  return {
    path: menuItem.to,
    component: menuItem.component
      ? menuItem.component
      : () => import('pages/Error404.vue'),
    name: menuItem.name ? menuItem.name : null,
    meta: { title: menuItem.title },
  };
});

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '*',
        component: () => import('pages/Error404.vue'),
      },
      ...menuRoutes,
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
