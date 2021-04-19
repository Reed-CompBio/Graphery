const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');

module.exports = {
  transpileDependencies: ['quasar'],
  devServer: {
    disableHostCheck: true,
  },
  configureWebpack: {
    plugins: [new MonacoWebpackPlugin({ languages: ['python'] })],
  },
  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0]['prod'] = process.env.NODE_ENV === 'production';
      return args;
    });
    config.module
      .rule('markdown-load')
      .test(/\.md$/i)
      .use('raw-loader')
      .loader('raw-loader')
      .end();
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
