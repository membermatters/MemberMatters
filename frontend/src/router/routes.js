import mainMenu from 'pages/pageAndRouteConfig';

const childRoutes = [];

const menuRoutes = mainMenu.map((menuItem) => {
  if (menuItem.children) {
    // eslint-disable-next-line array-callback-return
    menuItem.children.map((child) => {
      childRoutes.push({
        path: child.to ? child.to : '/no-route', // this means we didn't get a path and shouldn't route there
        component: child.component
          ? child.component
          : () => import('pages/Error404.vue'),
        name: child.name ? child.name : null,
        props: true,
        meta: { title: child.name, loggedIn: child.loggedIn },
      });
    });

    return {
      path: menuItem.to ? menuItem.to : '/no-route', // this means we didn't get a path and shouldn't route there
      component: menuItem.component
        ? menuItem.component
        : () => import('pages/Error404.vue'),
      name: menuItem.name ? menuItem.name : null,
      props: true,
      meta: { title: menuItem.name, loggedIn: menuItem.loggedIn },
    };
  }

  return {
    path: menuItem.to,
    component: menuItem.component
      ? menuItem.component
      : () => import('pages/Error404.vue'),
    name: menuItem.name ? menuItem.name : null,
    props: true,
    meta: { title: menuItem.name, loggedIn: menuItem.loggedIn },
  };
});

const routes = [
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
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue'),
  });
}

export default routes;
