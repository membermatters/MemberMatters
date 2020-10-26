/**
 * This file is used specifically and only for development. It installs
 * `electron-debug` & `vue-devtools`. There shouldn't be any need to
 *  modify this file, but it can be used to extend your development
 *  environment.
 */

// Install `electron-debug` with `devtron`
// eslint-disable-next-line @typescript-eslint/no-var-requires
require('electron-debug')({ showDevTools: true });

// Install `vue-devtools`
// eslint-disable-next-line @typescript-eslint/no-var-requires
require('electron').app.on('ready', () => {
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const installExtension = require('electron-devtools-installer');
  installExtension.default(installExtension.VUEJS_DEVTOOLS)
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    .then(() => {})
    .catch((err) => {
      console.log('Unable to install `vue-devtools`: \n', err);
    });
});

// Require `main` process to boot app
require('./electron-main');
