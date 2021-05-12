# MemberMatters (frontend)

The new MemberMatters frontend. You'll need the backend API to use this UI. Please check the [memberportal](/memberportal) folder for instructions.

The frontend software is a modern JavaScript SPA. It utilises Vue.js, Webpack, NPM, Capacitor and Electron. It also uses eslint for code formatting and linting.
The frontend can be built into a normal SPA web app, a semi native iOS and Android app, and a desktop "kiosk" mode.

# Getting Started
### Node
Ensure you have nvm (node version manager) installed. Once you've installed nvm install node 14 with `node install 14`.

### Linux
If you're using Ubuntu, you may need to install some dependencies with:

`sudo apt install libpng-dev`

If using Fedora, you may need to run the command:

`sudo dnf install libpng-devel`

## Install the dependencies
```bash
npm install
```

**Note:** please see the section above about configuring Font Awesome icons. You will run into issues if you don't correctly configure them.

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
npm run dev
```

Take note of the IP and port. In this case, open your favourite browser and go to `http://127.0.0.1:8080/`. You should
be presented with the home page of the web app. Assuming you loaded the database fixtures in the backend, you can login with the username "default@example.com" and password
"MemberMatters!". You should create a new account, then use the default account to give your new account admin rights. You can do so using the Django admin page for the `user` model which can be accessed at http://localhost:8080/admin/profile/user/. Make sure to select "super user", "staff", and "admin" for your new account. You should change the password of the default admin account or remove it once you've setup your new account.

### Build the app for production
```bash
npm run build
```

### Generate app icons
This will generate the app icons for every supported target of the MemberMatters portal (web, iOS, Android and Electron).

With the icon overlayed on a plain white splashscreen.
```bash
npm run icons
```

With the icon overlayed on a gradient background for the splashscreen.
```bash
npm run icons:bg
```

## Linter
This project uses a combination of eslint and prettier to detect common errors and enforce common code style.

You should set up a file watcher as explained below, but you can also manually lint the front end by running:
`npm run lint`

## Contributing Guidelines
This frontend project uses the Quasar framework for components and building/config. All source code
can be found in the `src` folder.

All code must pass the eslint rules. In fact, the dev server will throw an exception if your code
generates an eslint error. It is recommended that you set up some sort of file watcher in your IDE
that automatically runs `eslint --fix <changed_file>`. You should also set up your IDE to show
you eslint errors or warnings (most can do this).

### Routing and menu config
In the file `pages/pageAndRouteConfig.js` you'll find an object. This is where all of our routes
and main menu pages, page titles and components are specified. If you'd like to add a new page you
must add it to this file. Currently pages one level deep are supported under the `children` property.

#### Example
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
