// Configuration for your app
// https://quasar.dev/quasar-cli/quasar-conf-js

const path = require('path');

// eslint-disable-next-line func-names,no-unused-vars
module.exports = function (ctx) {
  return {
    // https://quasar.dev/quasar-cli/cli-documentation/boot-files
    boot: [
      'sentry',
      'i18n',
      'axios',
      'fontawesome-pro',
      'routeGuards',
      'capacitor',
    ],

    css: [
      'app.sass',
    ],

    extras: [
      'roboto-font', // optional, you are not bound to it
    ],

    framework: {
      cssAddon: true,
      config: {
        dark: 'auto', // or Boolean true/false
        loadingBar: { color: 'accent' },
      },
      iconSet: 'fontawesome-v5-pro', // Quasar icon set
      lang: 'en-us', // Quasar language pack

      all: 'auto',

      components: [],
      directives: [],

      plugins: [
        'Dialog',
        'LoadingBar',
      ],
    },

    // We do *not* support IE
    supportIE: false,

    // Full list of options: https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-build
    build: {
      env: {
        // Set this to false to disable fontawesome pro icons. You need to configure your .npmrc
        // file as per the font awesome pro instructions to download and use FA pro icons.
        proIcons: true,

        // When running with capacitor this value is used for the base URL for all API requests
        apiBaseUrl: JSON.stringify(process.env.API_BASE_URL),
      },

      vueRouterMode: 'history',

      showProgress: false,

      sourceMap: true,
      minify: true,

      // https://quasar.dev/quasar-cli/cli-documentation/handling-webpack
      extendWebpack(cfg) {
        cfg.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /node_modules/,
          options: {
            // eslint-disable-next-line global-require
            formatter: require('eslint')
              .CLIEngine
              .getFormatter('stylish'),
          },
        });

        cfg.resolve.alias = {
          ...cfg.resolve.alias,
          '@components': path.resolve(__dirname, './src/components'),
          '@icons': path.resolve(__dirname, './src/icons'),
          '@store': path.resolve(__dirname, './src/store'),
          '@mixins': path.resolve(__dirname, './src/mixins'),
        };
      },
    },

    // Full list of options: https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-devServer
    devServer: {
      https: false,
      port: ctx.mode.electron ? 8081 : 8080,
      host: '127.0.0.1',
      open: true, // opens browser window automatically
      proxy: {
        // proxy all requests starting with /api to
        '/api': {
          target: 'http://localhost:8001',
          changeOrigin: false,
        },
      },
    },

    animations: [],

    ssr: {
      pwa: false,
    },

    // https://quasar.dev/quasar-cli/developing-pwa/configuring-pwa
    pwa: {
      workboxPluginMode: 'GenerateSW', // 'GenerateSW' or 'InjectManifest'
      workboxOptions: {
        skipWaiting: true,
        clientsClaim: true,
      },
      manifest: {
        name: 'MemberMatters',
        short_name: 'MemberMatters',
        description: 'The MemberMatters frontend',
        display: 'standalone',
        orientation: 'portrait',
        background_color: '#ffffff',
        theme_color: '#7642FF',
        icons: [
          {
            src: 'statics/icons/icon-128x128.png',
            sizes: '128x128',
            type: 'image/png',
          },
          {
            src: 'statics/icons/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: 'statics/icons/icon-256x256.png',
            sizes: '256x256',
            type: 'image/png',
          },
          {
            src: 'statics/icons/icon-384x384.png',
            sizes: '384x384',
            type: 'image/png',
          },
          {
            src: 'statics/icons/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
    },

    // Full list of options: https://quasar.dev/quasar-cli/developing-cordova-apps/configuring-cordova
    cordova: {
      // noIosLegacyBuildFlag: true, // uncomment only if you know what you are doing
      id: 'org.membermatters.app',
    },

    // Full list of options: https://quasar.dev/quasar-cli/developing-capacitor-apps/configuring-capacitor
    capacitor: {
      hideSplashscreen: true,
      iosStatusBarPadding: true,
    },

    // Full list of options: https://quasar.dev/quasar-cli/developing-electron-apps/configuring-electron
    electron: {
      bundler: 'packager', // 'packager' or 'builder'

      packager: {
        // platform: 'all',
        overwrite: true,
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

        appId: 'frontend',
      },

      // More info: https://quasar.dev/quasar-cli/developing-electron-apps/node-integration
      nodeIntegration: true,

      // eslint-disable-next-line no-unused-vars
      extendWebpack(cfg) {
        // do something with Electron main process Webpack cfg
        // chainWebpack also available besides this extendWebpack
      },
    },
  };
};
