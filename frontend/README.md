# MemberMatters (frontend)

The new MemberMatters frontend

## Install the dependencies
```bash
npm install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
npm run dev
```

### Lint the files
```bash
npm run lint
```

### Build the app for production
```bash
npm run build
```
### Contributing Guidelines
This frontend project uses the Quasar framework for components and building/config. All source code
can be found in the `src` folder.

All code must pass the eslint rules. In fact, the dev server will throw an exception if your code
does not pass the linter. It is recommended that you setup some sort of file watcher in your IDE
that automatically runs `eslint --fix <changed_file>`. You should also set up your IDE to show
you eslint errors or warnings (most can do this).

#### Routing and menu config
In the file `pages/pageAndRouteConfig.js` you'll find an object. This is where all of our routes
and main menu pages, page titles and components are specified. If you'd like to add a new page you
must add it to this file. Currently pages one level deep are supported under the `children` property.

##### Example
```
{
    title: 'Dashboard', // this is the page title
    icon: 'fad fa-columns', // this is the icon to use in the main menu
    to: '/dashboard', // this is the how the URL should appear in the browser
    name: 'dashboard', // this is the page and tab title
    component: () => import('pages/Dashboard.vue'), // this specifies the component to use
  }
```

**NOTE:** you *must* specify the component as a generator like above for lazy loading to work correctly.
