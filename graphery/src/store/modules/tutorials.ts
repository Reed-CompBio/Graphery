import { TutorialState, RootState } from '@/store/states/state';
import { MutationTree, ActionTree, Action, GetterTree } from 'vuex';
const pseudoContent = {
  title: 'Lorem Ipsum',
  content:
    '<articl><p>' +
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Augue interdum velit euismod in pellentesque massa placerat. Felis imperdiet proin fermentum leo vel orci porta non. Risus sed vulputate odio ut. Pharetra massa massa ultricies mi quis hendrerit. Elementum sagittis vitae et leo duis ut diam. Sodales ut eu sem integer vitae justo eget magna fermentum. Semper risus in hendrerit gravida rutrum quisque non tellus. Tristique et egestas quis ipsum. Nunc scelerisque viverra mauris in aliquam. Varius vel pharetra vel turpis nunc eget lorem dolor.\n' +
    '</p><p>' +
    'Aliquam nulla facilisi cras fermentum. Nunc aliquet bibendum enim facilisis gravida. In ante metus dictum at tempor. Erat imperdiet sed euismod nisi porta lorem. Vitae tempus quam pellentesque nec nam aliquam sem. Ut sem nulla pharetra diam sit. Eget velit aliquet sagittis id consectetur. In metus vulputate eu scelerisque felis imperdiet. Magna etiam tempor orci eu lobortis elementum nibh tellus molestie. Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.\n' +
    '</p><p>' +
    'Amet consectetur adipiscing elit pellentesque habitant morbi tristique. Urna porttitor rhoncus dolor purus. Condimentum id venenatis a condimentum vitae sapien. Ultrices neque ornare aenean euismod elementum nisi quis eleifend quam. Mi tempus imperdiet nulla malesuada pellentesque. Gravida quis blandit turpis cursus in hac habitasse platea. Nunc lobortis mattis aliquam faucibus purus in massa tempor. Mattis enim ut tellus elementum. Lectus sit amet est placerat in egestas erat. Maecenas volutpat blandit aliquam etiam erat velit scelerisque in dictum. Neque volutpat ac tincidunt vitae semper quis lectus nulla. Amet nisl purus in mollis nunc sed id semper risus.\n' +
    '</p><p>' +
    'Vel facilisis volutpat est velit egestas dui id ornare arcu. Sed lectus vestibulum mattis ullamcorper velit sed ullamcorper. Pulvinar neque laoreet suspendisse interdum consectetur libero id faucibus nisl. Quam nulla porttitor massa id neque. Venenatis lectus magna fringilla urna porttitor rhoncus. Turpis massa sed elementum tempus egestas sed sed risus. Diam donec adipiscing tristique risus. In hendrerit gravida rutrum quisque. Consequat id porta nibh venenatis cras. Aliquam sem et tortor consequat id porta. Nulla aliquet enim tortor at auctor. Faucibus a pellentesque sit amet porttitor. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio. Nisi scelerisque eu ultrices vitae auctor eu. Facilisi etiam dignissim diam quis enim lobortis scelerisque fermentum dui. Viverra vitae congue eu consequat ac felis donec.\n' +
    '</p><p>' +
    'In fermentum posuere urna nec tincidunt praesent semper. Semper viverra nam libero justo laoreet sit amet. Quam nulla porttitor massa id. Id diam vel quam elementum pulvinar etiam. Elit ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue. Nulla facilisi nullam vehicula ipsum a arcu cursus vitae. Rutrum quisque non tellus orci ac auctor augue mauris. Amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus. Viverra nam libero justo laoreet sit. Amet mauris commodo quis imperdiet.\n' +
    '</p><p>' +
    'Viverra nam libero justo laoreet sit amet cursus. Blandit cursus risus at ultrices. Pretium aenean pharetra magna ac placerat. Pellentesque id nibh tortor id. Sed vulputate mi sit amet. Risus quis varius quam quisque. Justo laoreet sit amet cursus sit amet dictum sit. Nec dui nunc mattis enim. Lectus arcu bibendum at varius. Odio aenean sed adipiscing diam donec adipiscing tristique. Sed lectus vestibulum mattis ullamcorper velit sed. Cursus turpis massa tincidunt dui ut. Sed vulputate odio ut enim blandit volutpat maecenas. Vitae purus faucibus ornare suspendisse sed nisi lacus. Amet volutpat consequat mauris nunc. Ac tortor vitae purus faucibus ornare suspendisse sed. Aliquam sem fringilla ut morbi tincidunt augue interdum.\n' +
    '</p><p>' +
    'Volutpat est velit egestas dui id. Viverra maecenas accumsan lacus vel facilisis volutpat est velit egestas. Ut ornare lectus sit amet est placerat in egestas erat. Tristique senectus et netus et malesuada fames ac turpis egestas. Vulputate mi sit amet mauris commodo quis imperdiet massa. Pretium aenean pharetra magna ac placerat vestibulum lectus mauris. Urna cursus eget nunc scelerisque viverra mauris in aliquam sem. Gravida neque convallis a cras semper auctor neque vitae tempus. Quis imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper. Faucibus purus in massa tempor nec feugiat nisl pretium. Vulputate mi sit amet mauris commodo quis imperdiet. In fermentum et sollicitudin ac. Venenatis tellus in metus vulputate eu.\n' +
    '</p><p>' +
    'Id aliquet lectus proin nibh nisl. Mauris sit amet massa vitae tortor. Egestas sed sed risus pretium. Nec nam aliquam sem et tortor consequat. Mattis aliquam faucibus purus in. Scelerisque purus semper eget duis at tellus. Nunc id cursus metus aliquam eleifend mi in. Mollis nunc sed id semper risus. Non sodales neque sodales ut. Cras semper auctor neque vitae tempus. Lacus vestibulum sed arcu non odio. Varius duis at consectetur lorem donec massa sapien faucibus et. Sed sed risus pretium quam vulputate dignissim suspendisse. Amet consectetur adipiscing elit duis. In aliquam sem fringilla ut morbi tincidunt augue. Tristique magna sit amet purus gravida. Potenti nullam ac tortor vitae purus faucibus ornare suspendisse sed.\n' +
    '</p><p>' +
    'Fermentum et sollicitudin ac orci phasellus. Imperdiet sed euismod nisi porta lorem mollis. Id neque aliquam vestibulum morbi blandit cursus. Tincidunt eget nullam non nisi. Vulputate mi sit amet mauris commodo quis imperdiet. Sagittis orci a scelerisque purus semper eget duis. Tincidunt augue interdum velit euismod in pellentesque massa. Convallis aenean et tortor at risus. Quis vel eros donec ac. Pellentesque habitant morbi tristique senectus et. Ligula ullamcorper malesuada proin libero nunc consequat interdum varius sit. Eu facilisis sed odio morbi quis commodo odio aenean. Nunc sed blandit libero volutpat. Sit amet consectetur adipiscing elit duis tristique sollicitudin. Non tellus orci ac auctor augue. Aliquet risus feugiat in ante metus dictum at tempor commodo.\n' +
    '</p><p>' +
    'Magna ac placerat vestibulum lectus mauris ultrices eros in. In hac habitasse platea dictumst vestibulum. Sit amet tellus cras adipiscing enim eu. Neque vitae tempus quam pellentesque nec nam aliquam sem et. Turpis egestas sed tempus urna et pharetra pharetra. Velit euismod in pellentesque massa placerat duis ultricies lacus sed. Mauris commodo quis imperdiet massa. Vulputate enim nulla aliquet porttitor lacus luctus accumsan. Vitae elementum curabitur vitae nunc sed. Gravida quis blandit turpis cursus. Lectus vestibulum mattis ullamcorper velit. Habitant morbi tristique senectus et netus et malesuada fames ac.\n' +
    '</p><p>' +
    'Viverra tellus in hac habitasse platea dictumst vestibulum rhoncus est. Magnis dis parturient montes nascetur. Non enim praesent elementum facilisis. Lacinia quis vel eros donec ac odio tempor orci dapibus. Scelerisque in dictum non consectetur. Convallis aenean et tortor at risus viverra. Dui accumsan sit amet nulla. Consequat id porta nibh venenatis cras sed felis eget. Nunc id cursus metus aliquam eleifend mi in nulla posuere. In nibh mauris cursus mattis molestie a iaculis at. Quis varius quam quisque id diam vel. Ligula ullamcorper malesuada proin libero nunc consequat interdum varius. A scelerisque purus semper eget duis at tellus at.\n' +
    '</p><p>' +
    'Velit scelerisque in dictum non consectetur a erat. Elementum integer enim neque volutpat ac tincidunt vitae semper quis. Viverra mauris in aliquam sem fringilla. Cras semper auctor neque vitae tempus. Amet mauris commodo quis imperdiet massa tincidunt nunc. Enim facilisis gravida neque convallis a cras semper. Accumsan in nisl nisi scelerisque eu ultrices vitae. Nulla facilisi etiam dignissim diam quis enim. Ultrices vitae auctor eu augue ut lectus arcu. Habitant morbi tristique senectus et netus et malesuada fames ac. Aliquet eget sit amet tellus cras. Id eu nisl nunc mi ipsum faucibus vitae aliquet. Risus feugiat in ante metus dictum.\n' +
    '</p><p>' +
    'Semper risus in hendrerit gravida rutrum quisque non tellus. Mi proin sed libero enim sed faucibus. A pellentesque sit amet porttitor eget dolor morbi non arcu. Eu ultrices vitae auctor eu augue. Amet cursus sit amet dictum. Blandit libero volutpat sed cras ornare arcu dui vivamus arcu. Arcu vitae elementum curabitur vitae. In hendrerit gravida rutrum quisque non tellus orci. A iaculis at erat pellentesque adipiscing commodo elit at imperdiet. Mattis enim ut tellus elementum. Nisl nisi scelerisque eu ultrices vitae. Justo nec ultrices dui sapien. Bibendum enim facilisis gravida neque convallis a.\n' +
    '</p><p>' +
    'Egestas congue quisque egestas diam in arcu. Aliquet sagittis id consectetur purus. Nibh nisl condimentum id venenatis a condimentum. Ut sem nulla pharetra diam sit amet. Lectus sit amet est placerat. Orci nulla pellentesque dignissim enim sit amet venenatis. Adipiscing elit pellentesque habitant morbi tristique senectus et netus. Nullam non nisi est sit. Pulvinar etiam non quam lacus suspendisse faucibus interdum posuere. Phasellus faucibus scelerisque eleifend donec pretium.\n' +
    '</p><p>' +
    'Tincidunt id aliquet risus feugiat in ante metus dictum at. Massa ultricies mi quis hendrerit dolor magna eget est lorem. Mi bibendum neque egestas congue quisque egestas. Velit dignissim sodales ut eu sem. Quis imperdiet massa tincidunt nunc pulvinar sapien et. Imperdiet sed euismod nisi porta lorem. Quam elementum pulvinar etiam non quam lacus suspendisse faucibus. Nunc scelerisque viverra mauris in aliquam. Sit amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus. Faucibus ornare suspendisse sed nisi lacus sed viverra tellus in. Sit amet volutpat consequat mauris nunc congue nisi vitae suscipit. In nibh mauris cursus mattis molestie a iaculis at. Eget nulla facilisi etiam dignissim diam quis. Tellus rutrum tellus pellentesque eu. Id consectetur purus ut faucibus. Aliquet eget sit amet tellus cras adipiscing enim eu turpis. Ut tortor pretium viverra suspendisse. Fringilla est ullamcorper eget nulla facilisi etiam dignissim diam.\n' +
    '</p><p>' +
    'Convallis a cras semper auctor neque vitae. Vestibulum lectus mauris ultrices eros in cursus turpis massa tincidunt. Sapien pellentesque habitant morbi tristique senectus et. Viverra vitae congue eu consequat ac felis donec et. Vel facilisis volutpat est velit egestas dui id ornare arcu. Donec ultrices tincidunt arcu non sodales neque sodales ut. Cras sed felis eget velit aliquet sagittis id consectetur purus. Condimentum vitae sapien pellentesque habitant. Sed turpis tincidunt id aliquet risus feugiat. Enim tortor at auctor urna nunc. Fermentum et sollicitudin ac orci phasellus. Elementum sagittis vitae et leo duis.\n' +
    '</p><p>' +
    'Volutpat consequat mauris nunc congue nisi vitae suscipit. Dolor sed viverra ipsum nunc aliquet bibendum enim facilisis. Quisque non tellus orci ac auctor augue mauris augue. Pellentesque habitant morbi tristique senectus et. Tristique et egestas quis ipsum suspendisse ultrices gravida. Pellentesque dignissim enim sit amet venenatis urna cursus eget nunc. Pharetra vel turpis nunc eget lorem dolor sed viverra ipsum. Proin sed libero enim sed faucibus turpis in. Elit pellentesque habitant morbi tristique senectus et netus et. Lorem sed risus ultricies tristique.\n' +
    '</p><p>' +
    'Aliquet porttitor lacus luctus accumsan tortor posuere. Iaculis at erat pellentesque adipiscing commodo. Mus mauris vitae ultricies leo integer. Sagittis vitae et leo duis. Nec dui nunc mattis enim. Turpis in eu mi bibendum neque egestas. Amet cursus sit amet dictum sit amet. Sagittis eu volutpat odio facilisis mauris sit amet massa vitae. Sed faucibus turpis in eu mi bibendum neque egestas congue. Nibh tortor id aliquet lectus proin nibh nisl. Sed sed risus pretium quam vulputate dignissim. Amet tellus cras adipiscing enim eu turpis egestas. Fames ac turpis egestas maecenas pharetra convallis posuere. Libero justo laoreet sit amet cursus sit amet dictum sit. Adipiscing at in tellus integer feugiat scelerisque varius. Aliquet sagittis id consectetur purus.\n' +
    '</p><p>' +
    'Consequat semper viverra nam libero justo. Ipsum dolor sit amet consectetur adipiscing elit duis. Nunc sed id semper risus in hendrerit gravida rutrum. Condimentum id venenatis a condimentum vitae sapien. Tincidunt dui ut ornare lectus sit amet est. Et molestie ac feugiat sed. Ac placerat vestibulum lectus mauris ultrices. Augue lacus viverra vitae congue eu consequat ac felis. Venenatis urna cursus eget nunc scelerisque viverra mauris. Integer vitae justo eget magna. Ligula ullamcorper malesuada proin libero nunc consequat interdum varius. Sed arcu non odio euismod lacinia at quis risus. Nec feugiat nisl pretium fusce id velit ut tortor pretium. Sed velit dignissim sodales ut.\n' +
    '</p><p>' +
    'Amet mauris commodo quis imperdiet massa tincidunt nunc. Sed ullamcorper morbi tincidunt ornare massa eget egestas purus. Consequat id porta nibh venenatis cras sed felis eget velit. Elit ullamcorper dignissim cras tincidunt lobortis feugiat vivamus. Eget mi proin sed libero enim sed faucibus turpis. A arcu cursus vitae congue. Odio ut sem nulla pharetra diam sit amet nisl. Elit at imperdiet dui accumsan sit amet. Maecenas volutpat blandit aliquam etiam erat velit scelerisque in. Ut lectus arcu bibendum at varius vel pharetra. Elementum integer enim neque volutpat ac tincidunt. Blandit turpis cursus in hac habitasse platea dictumst. Amet cursus sit amet dictum. Feugiat nisl pretium fusce id velit ut tortor pretium viverra.\n' +
    '</p></articl>',
};

const state: TutorialState = {
  // TODO do I need the ids?
  articleId: null,
  article: null,
  graphIDs: null,
  graphs: null,
  codes: null,
};

const mutations: MutationTree<TutorialState> = {
  LOAD_ARTICLE_ID(state, value) {
    state.articleId = value;
  },
  LOAD_ARTICLES(state, value) {
    state.article = value;
  },
  LOAD_GRAPH_IDS(state, value) {
    state.graphIDs = value;
  },
  LOAD_GRAPHS(state, value) {
    state.graphs = value;
  },
  LOAD_CODES(state, value) {
    state.codes = value;
  },
  // don't know how to write this
  // MODIFY_GRAPH_BY_ID(state, info) {},
};

const actions: ActionTree<TutorialState, RootState> = {
  loadTutorial({ commit }, tutorialId) {
    let article;
    let graphIds;
    // TODO promises
    commit('LOAD_ARTICLES', article);
    commit('LOAD_GRAPH_IDS', graphIds);
  },
  loadGraphsByIds({ commit }, graphIds) {
    let graphs;
    // TODO promises
    commit('LOAD_GRAPHS', graphs);
  },
  loadCodes({ commit }, graphIds) {
    let codes;
    // TODO promises
    commit('LOAD_CODES', codes);
  },
  clearAll({ commit }) {
    commit('LOAD_ARTICLE_ID', null);
    commit('LOAD_ARTICLES', null);
    commit('LOAD_GRAPH_IDS', null);
    commit('LOAD_GRAPHS', null);
    commit('LOAD_CODES', null);
  },
  // don't know how to write this
  // modifyGraphById({ commit, getters }, { graphId, delta }) {},
};

const getters: GetterTree<TutorialState, RootState> = {
  articleEmpty(state) {
    return state.article === null;
  },
  graphsEmpty(state) {
    return state.graphs === null;
  },
  codesEmpty(state) {
    return state.codes === null;
  },
  getGraphById: (state) => (id: string) => {
    return state.graphs ? state.graphs.find((graph) => graph.id == id) : null;
  },
  getGraphByIndex: (state) => (index: number) => {
    return state.graphs ? state.graphs[index] : null;
  },
  getCodeById: (state) => (id: string) => {
    return state.codes ? state.codes[id] : null;
  },
  getCodeByIndex: (state) => (index: number) => {
    return state.codes ? state.codes[index] : null;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
