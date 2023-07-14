/* eslint-env node */

/*
 * This file runs in a Node context (it's NOT transpiled by Babel), so use only
 * the ES6 features that are supported by your Node version. https://node.green/
 */

// Configuration for your app
// https://v2.quasar.dev/quasar-cli-vite/quasar-config-js

const { configure } = require('quasar/wrappers');
const path = require('path');
const NodeModulesPolyfillPlugin = require('@esbuild-plugins/node-modules-polyfill');
const NodeGlobalsPolyfillPlugin = require('@esbuild-plugins/node-globals-polyfill');
const rollupNodePolyFill = require('rollup-plugin-node-polyfills');
const tsconfigPaths = require('vite-tsconfig-paths');

module.exports = configure(function (ctx) {
  return {
    eslint: {
      // fix: true,
      // include: [],
      // exclude: [],
      // rawOptions: {},
      warnings: true,
      errors: true,
    },

    // https://v2.quasar.dev/quasar-cli-vite/prefetch-feature
    // preFetch: true,

    // app boot file (/src/boot)
    // --> boot files are part of "main.js"
    // https://v2.quasar.dev/quasar-cli-vite/boot-files
    boot: ['sentry', 'i18n', 'axios', 'routeGuards', 'capacitor'],

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#css
    css: ['app.scss'],

    // https://github.com/quasarframework/quasar/tree/dev/extras
    extras: [
      'mdi-v5',
      'roboto-font', // optional, you are not bound to it
    ],

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#build
    build: {
      target: {
        browser: ['es2019', 'edge88', 'firefox78', 'chrome87', 'safari13.1'],
        node: 'node18',
      },

      htmlFilename: 'index.html',

      env: {
        // When running with capacitor this value is used for the base URL for all API requests
        apiBaseUrl: process.env.API_BASE_URL,
      },

      vueRouterMode: 'history', // available values: 'hash', 'history'
      // vueRouterBase,
      // vueDevtools,
      polyfillModulePreload: true,
      vueOptionsAPI: true,

      // rebuildCache: true, // rebuilds Vite/linter/etc cache on startup

      showProgress: true,
      minify: true,

      extendViteConf(viteConf, { isServer, isClient }) {
        viteConf.plugins.push({
          name: 'fix-node-globals-polyfill',
          setup(build) {
            build.onResolve({ filter: /util\.js/ }, ({ path }) => ({ path }));
          },
        });

        viteConf.plugins.push(tsconfigPaths.default());

        viteConf.build = {
          ...viteConf.build,
          build: {
            rollupOptions: {
              plugins: [
                // Enable rollup polyfills plugin
                // used during production bundling
                rollupNodePolyFill(),
              ],
            },
          },
        };

        viteConf.optimizeDeps.esbuildOptions = {
          ...viteConf.optimizeDeps.esbuildOptions,
          define: {
            global: 'globalThis',
          },
          plugins: [
            NodeGlobalsPolyfillPlugin.NodeGlobalsPolyfillPlugin({
              process: true,
              buffer: true,
            }),
            NodeModulesPolyfillPlugin.NodeModulesPolyfillPlugin(),
            {
              name: 'fix-node-globals-polyfill',
              setup(build) {
                build.onResolve(
                  { filter: /_virtual-process-polyfill_\.js/ },
                  ({ path }) => ({ path })
                );
              },
            },
          ],
        };
      },
      // viteVuePluginOptions: {},

      alias: {
        '@components': path.join(__dirname, 'src/components/'),
        '@icons': path.join(__dirname, 'src/icons/'),
        '@store': path.join(__dirname, 'src/store/'),
        '@mixins': path.join(__dirname, 'src/mixins/'),
        '@assets': path.join(__dirname, 'src/assets/'),

        util: 'util',
        sys: 'util',
        events: 'rollup-plugin-node-polyfills/polyfills/events',
        stream: 'rollup-plugin-node-polyfills/polyfills/stream',
        path: 'rollup-plugin-node-polyfills/polyfills/path',
        querystring: 'rollup-plugin-node-polyfills/polyfills/qs',
        punycode: 'rollup-plugin-node-polyfills/polyfills/punycode',
        url: 'rollup-plugin-node-polyfills/polyfills/url',
        string_decoder: 'rollup-plugin-node-polyfills/polyfills/string-decoder',
        http: 'rollup-plugin-node-polyfills/polyfills/http',
        https: 'rollup-plugin-node-polyfills/polyfills/http',
        os: 'rollup-plugin-node-polyfills/polyfills/os',
        assert: 'rollup-plugin-node-polyfills/polyfills/assert',
        constants: 'rollup-plugin-node-polyfills/polyfills/constants',
        _stream_duplex:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/duplex',
        _stream_passthrough:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/passthrough',
        _stream_readable:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/readable',
        _stream_writable:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/writable',
        _stream_transform:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/transform',
        timers: 'rollup-plugin-node-polyfills/polyfills/timers',
        console: 'rollup-plugin-node-polyfills/polyfills/console',
        vm: 'rollup-plugin-node-polyfills/polyfills/vm',
        zlib: 'rollup-plugin-node-polyfills/polyfills/zlib',
        tty: 'rollup-plugin-node-polyfills/polyfills/tty',
        domain: 'rollup-plugin-node-polyfills/polyfills/domain',
      },

      vitePlugins: [
        [
          '@intlify/vite-plugin-vue-i18n',
          {
            // if you want to use Vue I18n Legacy API, you need to set `compositionOnly: false`
            compositionOnly: false,

            // if you want to use named tokens in your Vue I18n messages, such as 'Hello {name}',
            // you need to set `runtimeOnly: false`
            runtimeOnly: false,

            // you need to set i18n resource including paths !
            include: path.join(__dirname, './src/i18n/**'),
          },
        ],
      ],
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#devServer
    devServer: {
      https: false,
      port: 8080,
      open: true, // opens browser window automatically
      proxy: {
        // proxy requests when running dev server
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: false,
        },
        '/admin': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
        '/static': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    },

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#framework
    framework: {
      lang: 'en-US', // Quasar language pack
      iconSet: 'mdi-v7',
      config: {
        dark: 'auto', // or Boolean true/false
        loadingBar: { color: 'accent', skipHijack: ctx.mode.capacitor },
        iconSet: 'mdi-v7', // Quasar icon set

        // For special cases outside of where the auto-import strategy can have an impact
        // (like functional components as one of the examples),
        // you can manually specify Quasar components/directives to be available everywhere:
        //
        // components: [],
        // directives: [],

        // Quasar plugins
        plugins: ['Dialog', 'LoadingBar', 'Cookies'],
      },

      // animations: 'all', // --- includes all animations
      // https://v2.quasar.dev/options/animations
      // animations: ['fadeIn', 'fadeOut', 'bounceInLeft', 'bounceOutRight'],

      // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#sourcefiles
      // sourceFiles: {
      //   rootComponent: 'src/App.vue',
      //   router: 'src/router/index',
      //   store: 'src/store/index',
      //   registerServiceWorker: 'src-pwa/register-service-worker',
      //   serviceWorker: 'src-pwa/custom-service-worker',
      //   pwaManifestFile: 'src-pwa/manifest.json',
      //   electronMain: 'src-electron/electron-main',
      //   electronPreload: 'src-electron/electron-preload'
      // },

      // https://v2.quasar.dev/quasar-cli-vite/developing-ssr/configuring-ssr
      ssr: {
        // ssrPwaHtmlFilename: 'offline.html', // do NOT use index.html as name!
        // will mess up SSR

        // extendSSRWebserverConf (esbuildConf) {},
        // extendPackageJson (json) {},

        pwa: false,

        // manualStoreHydration: true,
        // manualPostHydrationTrigger: true,

        prodPort: 3000, // The default port that the production server should use
        // (gets superseded if process.env.PORT is specified at runtime)

        middlewares: [
          'render', // keep this as last one
        ],
      },

      // https://v2.quasar.dev/quasar-cli-vite/developing-pwa/configuring-pwa
      pwa: {
        workboxMode: 'generateSW', // or 'injectManifest'
        injectPwaMetaTags: true,
        swFilename: 'sw.js',
        manifestFilename: 'manifest.json',
        useCredentialsForManifestTag: false,
      },

      // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-cordova-apps/configuring-cordova
      cordova: {
        // noIosLegacyBuildFlag: true, // uncomment only if you know what you are doing
      },

      // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-capacitor-apps/configuring-capacitor
      capacitor: {
        hideSplashscreen: false,
        iosStatusBarPadding: true,
      },

      // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-electron-apps/configuring-electron
      electron: {
        // extendElectronMainConf (esbuildConf)
        // extendElectronPreloadConf (esbuildConf)

        inspectPort: 5858,

        bundler: 'packager', // 'packager' or 'builder'

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

          appId: 'membermatters',
        },

        nodeIntegration: true,
      },

      // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/configuring-bex
      bex: {
        // contentScripts: [
        //   'my-content-script'
        // ],
        // extendBexScriptsConf (esbuildConf) {}
        // extendBexManifestJson (json) {}
      },
    },
  };
});
