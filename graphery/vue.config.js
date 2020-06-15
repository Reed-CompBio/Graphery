const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');

module.exports = {
  transpileDependencies: ['quasar'],
  devServer: {
    disableHostCheck: true,
  },
  configureWebpack: {
    plugins: [new MonacoWebpackPlugin({ languages: ['python'] })],
  },
  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: false,
    },
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: false,
    },
  },
};
