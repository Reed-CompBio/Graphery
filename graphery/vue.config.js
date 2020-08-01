import MonacoEditorWebpackPlugin from 'monaco-editor-webpack-plugin';

module.exports = {
  transpileDependencies: ['quasar'],
  devServer: {
    disableHostCheck: true,
  },
  configureWebpack: {
    plugins: [new MonacoEditorWebpackPlugin({ languages: ['python'] })],
  },
  pluginOptions: {
    quasar: {
      importStrategy: 'manual',
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
