module.exports = {
  transpileDependencies: ['quasar'],

  devServer: {
    disableHostCheck: true,
  },

  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      // TODO
      //     importStrategy: 'manual',
      rtlSupport: false,
    },
  },
};
