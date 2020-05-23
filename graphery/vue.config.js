module.exports = {
  transpileDependencies: ['vuetify', 'quasar'],

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
