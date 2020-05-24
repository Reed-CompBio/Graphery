module.exports = {
  transpileDependencies: ['quasar'],

  devServer: {
    disableHostCheck: true,
  },

  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: false,
    },
  },
};
