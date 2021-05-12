/*
 * This file runs in a Node context (it's NOT transpiled by Babel), so use only
 * the ES6 features that are supported by your Node version. https://node.green/
 */

// Configuration for your app
// https://quasar.dev/quasar-cli/quasar-conf-js
/* eslint-env node */
/* eslint func-names: 0 */
/* eslint global-require: 0 */
/* eslint-disable @typescript-eslint/no-var-requires */
const path = require("path");
const { configure } = require("quasar/wrappers");

module.exports = configure((ctx) => ({
  // https://quasar.dev/quasar-cli/supporting-ts
  supportTS: {
    tsCheckerConfig: {
      eslint: true,
    },
  },

  // https://quasar.dev/quasar-cli/prefetch-feature
  // preFetch: true,

  // app boot file (/src/boot)
  // --> boot files are part of "main.js"
  // https://quasar.dev/quasar-cli/boot-files
  boot: [
    "vueCompositionApi",
    "sentry",
    "i18n",
    "axios",
    "routeGuards",
    "capacitor",
  ],

  // https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-css
  css: [
    "app.scss",
  ],

  // https://github.com/quasarframework/quasar/tree/dev/extras
  extras: [
    // 'ionicons-v4',
    "mdi-v5",
    // 'fontawesome-v5',
    // 'eva-icons',
    // 'themify',
    // 'line-awesome',
    // 'roboto-font-latin-ext', // this or either 'roboto-font', NEVER both!

    "roboto-font", // optional, you are not bound to it
    // 'material-icons', // optional, you are not bound to it
  ],

  // Full list of options: https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-build
  build: {
    vueRouterMode: "history", // available values: 'hash', 'history'
    env: {
      // When running with capacitor this value is used for the base URL for all API requests
      apiBaseUrl: process.env.API_BASE_URL,
    },

    showProgress: true,

    sourceMap: true,
    minify: true,

    transpile: true,

    // Add dependencies for transpiling with Babel (Array of string/regex)
    // (from node_modules, which are by default not transpiled).
    // Applies only if "transpile" is set to true.
    transpileDependencies: ["vuex-composition-helpers"],

    // rtl: false, // https://quasar.dev/options/rtl-support
    // preloadChunks: true,
    // showProgress: false,
    // gzip: true,
    // analyze: true,

    // Options below are automatically set depending on the env, set them if you want to override
    // extractCSS: false,

    // https://quasar.dev/quasar-cli/handling-webpack
    extendWebpack (cfg) {
      // linting is slow in TS projects, we execute it only for production builds
      if (ctx.prod) {
        cfg.module.rules.push({
          enforce: "pre",
          test: /\.(js|vue)$/,
          loader: "eslint-loader",
          exclude: /node_modules/,
        });
      }

      cfg.module.rules.push(
        {
          test: /\.(afphoto)$/,
          use: "null-loader",
        },
      );
      cfg.module.rules.push(
        {
          test: /(LICENSE)$/,
          use: "null-loader",
        },
      );

      cfg.resolve.alias = {
        ...cfg.resolve.alias,
        "@components": path.resolve(__dirname, "src/components/"),
        "@icons": path.resolve(__dirname, "src/icons/"),
        "@store": path.resolve(__dirname, "src/store/"),
        "@mixins": path.resolve(__dirname, "src/mixins/"),
        "@assets": path.resolve(__dirname, "src/assets/"),
      };
    },
  },

  // Full list of options: https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-devServer
  devServer: {
    https: false,
    port: 8080,
    open: true, // opens browser window automatically
    proxy: {
      // proxy all requests starting with /api to
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: false,
      },
      "/admin": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/static": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },

  // https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-framework
  framework: {
    lang: "en-us", // Quasar language pack
    config: {
      dark: "auto", // or Boolean true/false
      loadingBar: { color: "accent", skipHijack: ctx.mode.capacitor },
    },
    iconSet: "mdi-v5", // Quasar icon set

    // Possible values for "importStrategy":
    // * 'auto' - (DEFAULT) Auto-import needed Quasar components & directives
    // * 'all'  - Manually specify what to import
    importStrategy: "auto",

    // For special cases outside of where "auto" importStrategy can have an impact
    // (like functional components as one of the examples),
    // you can manually specify Quasar components/directives to be available everywhere:
    //
    // components: [],
    // directives: [],

    // Quasar plugins
    plugins: [
      "Dialog",
      "LoadingBar",
      "Cookies",
    ],
  },

  // animations: 'all', // --- includes all animations
  // https://quasar.dev/options/animations
  animations: [],

  // https://quasar.dev/quasar-cli/developing-ssr/configuring-ssr
  ssr: {
    pwa: false,
  },

  // https://quasar.dev/quasar-cli/developing-pwa/configuring-pwa
  pwa: {
    workboxPluginMode: "GenerateSW", // 'GenerateSW' or 'InjectManifest'
    workboxOptions: {}, // only for GenerateSW
    manifest: {
      name: "MemberMatters",
      short_name: "MemberMatters",
      description: "The MemberMatters frontend",
      display: "standalone",
      orientation: "portrait",
      background_color: "#ffffff",
      theme_color: "#7642FF",
      icons: [
        {
          src: "icons/icon-128x128.png",
          sizes: "128x128",
          type: "image/png",
        },
        {
          src: "icons/icon-192x192.png",
          sizes: "192x192",
          type: "image/png",
        },
        {
          src: "icons/icon-256x256.png",
          sizes: "256x256",
          type: "image/png",
        },
        {
          src: "icons/icon-384x384.png",
          sizes: "384x384",
          type: "image/png",
        },
        {
          src: "icons/icon-512x512.png",
          sizes: "512x512",
          type: "image/png",
        },
      ],
    },
  },

  // Full list of options: https://quasar.dev/quasar-cli/developing-cordova-apps/configuring-cordova
  cordova: {
    // noIosLegacyBuildFlag: true, // uncomment only if you know what you are doing
  },

  // Full list of options: https://quasar.dev/quasar-cli/developing-capacitor-apps/configuring-capacitor
  capacitor: {
    hideSplashscreen: false,
    iosStatusBarPadding: true,
  },

  // Full list of options: https://quasar.dev/quasar-cli/developing-electron-apps/configuring-electron
  electron: {
    bundler: "packager", // 'packager' or 'builder'

    packager: {
      // https://github.com/electron-userland/electron-packager/blob/master/docs/api.md#options

      // OS X / Mac App Store
      // appBundleId: '',
      // appCategoryType: '',
      // osxSign: '',
      // protocol: 'myapp://path',

      // Windows only
      // win32metadata: { ... }
    },

    builder: {
      // https://www.electron.build/configuration/configuration

      appId: "membermatters",
    },

    // More info: https://quasar.dev/quasar-cli/developing-electron-apps/node-integration
    nodeIntegration: true,

    extendWebpack (/* cfg */) {
      // do something with Electron main process Webpack cfg
      // chainWebpack also available besides this extendWebpack
    },
  },
}));
