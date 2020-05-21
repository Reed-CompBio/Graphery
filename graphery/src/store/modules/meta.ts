export default {
  namespaced: true,
  state: {
    siteName: 'Graphery',
    navigationButtons: [
      { name: 'Home', icon: 'mdi-home-circle' },
      { name: 'Tutorials', icon: 'mdi-newspaper-variant' },
      { name: 'Graphs', icon: 'mdi-graph' },
      { name: 'About', icon: 'mdi-clipboard-account-outline' },
      { name: 'Loggin', icon: 'mdi-account-circle' },
      { name: 'Settings', icon: 'mdi-cog' },
    ],
    siteLogo: require('@/assets/images/reed-compbio-logo.png'),
    footerMessage: '',
  },
};
