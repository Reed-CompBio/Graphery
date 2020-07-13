import {
  Graph,
  ResultJsonType,
  RootState,
  TutorialArticleContent,
  TutorialDetailResponse,
  TutorialGraph,
  TutorialMetaState,
  TutorialState,
} from '@/store/states/state';
import { ActionTree, GetterTree, MutationTree } from 'vuex';

/** Do not use Vuex since you can't maintain multiple pages with one state
 * Or I can add a object mapping the time of opening the page to the
 * corresponding object
 */
const pseudoContent = {
  title: 'Lorem Ipsum',
  contentHtml:
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
  authors: ['Me'],
  categories: ['hhh'],
  modifiedTime: Date(),
  isPublished: false,
};

const pseudoResultJson =
  '[{"line": 6, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": null, "graphery_count_degree_by_edges#edge": null, "graphery_count_degree_by_edges#degree_dict": null}}, {"line": 7, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": null, "graphery_count_degree_by_edges#edge": null, "graphery_count_degree_by_edges#degree_dict": "{}"}}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": null, "graphery_count_degree_by_edges#edge": {"id": 1, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n2))"}, "graphery_count_degree_by_edges#degree_dict": "{}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n1", "color": "#A6CEE3", "label": "Node(id: n1)"}, "graphery_count_degree_by_edges#edge": {"id": 1, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n2))"}, "graphery_count_degree_by_edges#degree_dict": "{}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n1", "color": "#A6CEE3", "label": "Node(id: n1)"}, "graphery_count_degree_by_edges#edge": {"id": 1, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n2))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n2", "color": "#A6CEE3", "label": "Node(id: n2)"}, "graphery_count_degree_by_edges#edge": {"id": 1, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n2))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n2", "color": "#A6CEE3", "label": "Node(id: n2)"}, "graphery_count_degree_by_edges#edge": {"id": 1, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n2))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n2", "color": "#A6CEE3", "label": "Node(id: n2)"}, "graphery_count_degree_by_edges#edge": {"id": 7, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n5))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n4", "color": "#A6CEE3", "label": "Node(id: n4)"}, "graphery_count_degree_by_edges#edge": {"id": 7, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n5))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n4", "color": "#A6CEE3", "label": "Node(id: n4)"}, "graphery_count_degree_by_edges#edge": {"id": 7, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n5))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n5", "color": "#A6CEE3", "label": "Node(id: n5)"}, "graphery_count_degree_by_edges#edge": {"id": 7, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n5))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n5", "color": "#A6CEE3", "label": "Node(id: n5)"}, "graphery_count_degree_by_edges#edge": {"id": 7, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n5))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n5", "color": "#A6CEE3", "label": "Node(id: n5)"}, "graphery_count_degree_by_edges#edge": {"id": 13, "color": "#1F78B4", "label": "(Node(id: n12), Node(id: n13))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n12", "color": "#A6CEE3", "label": "Node(id: n12)"}, "graphery_count_degree_by_edges#edge": {"id": 13, "color": "#1F78B4", "label": "(Node(id: n12), Node(id: n13))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n12", "color": "#A6CEE3", "label": "Node(id: n12)"}, "graphery_count_degree_by_edges#edge": {"id": 13, "color": "#1F78B4", "label": "(Node(id: n12), Node(id: n13))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n13", "color": "#A6CEE3", "label": "Node(id: n13)"}, "graphery_count_degree_by_edges#edge": {"id": 13, "color": "#1F78B4", "label": "(Node(id: n12), Node(id: n13))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n13", "color": "#A6CEE3", "label": "Node(id: n13)"}, "graphery_count_degree_by_edges#edge": {"id": 13, "color": "#1F78B4", "label": "(Node(id: n12), Node(id: n13))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n13", "color": "#A6CEE3", "label": "Node(id: n13)"}, "graphery_count_degree_by_edges#edge": {"id": 10, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n9))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n8", "color": "#A6CEE3", "label": "Node(id: n8)"}, "graphery_count_degree_by_edges#edge": {"id": 10, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n9))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n8", "color": "#A6CEE3", "label": "Node(id: n8)"}, "graphery_count_degree_by_edges#edge": {"id": 10, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n9))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n9", "color": "#A6CEE3", "label": "Node(id: n9)"}, "graphery_count_degree_by_edges#edge": {"id": 10, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n9))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n9", "color": "#A6CEE3", "label": "Node(id: n9)"}, "graphery_count_degree_by_edges#edge": {"id": 10, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n9))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n9", "color": "#A6CEE3", "label": "Node(id: n9)"}, "graphery_count_degree_by_edges#edge": {"id": 0, "color": "#1F78B4", "label": "(Node(id: n0), Node(id: n1))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n0", "color": "#A6CEE3", "label": "Node(id: n0)"}, "graphery_count_degree_by_edges#edge": {"id": 0, "color": "#1F78B4", "label": "(Node(id: n0), Node(id: n1))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n0", "color": "#A6CEE3", "label": "Node(id: n0)"}, "graphery_count_degree_by_edges#edge": {"id": 0, "color": "#1F78B4", "label": "(Node(id: n0), Node(id: n1))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n1", "color": "#A6CEE3", "label": "Node(id: n1)"}, "graphery_count_degree_by_edges#edge": {"id": 0, "color": "#1F78B4", "label": "(Node(id: n0), Node(id: n1))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 1, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n1", "color": "#A6CEE3", "label": "Node(id: n1)"}, "graphery_count_degree_by_edges#edge": {"id": 0, "color": "#1F78B4", "label": "(Node(id: n0), Node(id: n1))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n1", "color": "#A6CEE3", "label": "Node(id: n1)"}, "graphery_count_degree_by_edges#edge": {"id": 6, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n16))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n3", "color": "#A6CEE3", "label": "Node(id: n3)"}, "graphery_count_degree_by_edges#edge": {"id": 6, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n16))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n3", "color": "#A6CEE3", "label": "Node(id: n3)"}, "graphery_count_degree_by_edges#edge": {"id": 6, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n16))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n16", "color": "#A6CEE3", "label": "Node(id: n16)"}, "graphery_count_degree_by_edges#edge": {"id": 6, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n16))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n16", "color": "#A6CEE3", "label": "Node(id: n16)"}, "graphery_count_degree_by_edges#edge": {"id": 6, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n16))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n16", "color": "#A6CEE3", "label": "Node(id: n16)"}, "graphery_count_degree_by_edges#edge": {"id": 3, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n7))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n2", "color": "#A6CEE3", "label": "Node(id: n2)"}, "graphery_count_degree_by_edges#edge": {"id": 3, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n7))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 1, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n2", "color": "#A6CEE3", "label": "Node(id: n2)"}, "graphery_count_degree_by_edges#edge": {"id": 3, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n7))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n7", "color": "#A6CEE3", "label": "Node(id: n7)"}, "graphery_count_degree_by_edges#edge": {"id": 3, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n7))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n7", "color": "#A6CEE3", "label": "Node(id: n7)"}, "graphery_count_degree_by_edges#edge": {"id": 3, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n7))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n7", "color": "#A6CEE3", "label": "Node(id: n7)"}, "graphery_count_degree_by_edges#edge": {"id": 9, "color": "#1F78B4", "label": "(Node(id: n6), Node(id: n8))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n6", "color": "#A6CEE3", "label": "Node(id: n6)"}, "graphery_count_degree_by_edges#edge": {"id": 9, "color": "#1F78B4", "label": "(Node(id: n6), Node(id: n8))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n6", "color": "#A6CEE3", "label": "Node(id: n6)"}, "graphery_count_degree_by_edges#edge": {"id": 9, "color": "#1F78B4", "label": "(Node(id: n6), Node(id: n8))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n8", "color": "#A6CEE3", "label": "Node(id: n8)"}, "graphery_count_degree_by_edges#edge": {"id": 9, "color": "#1F78B4", "label": "(Node(id: n6), Node(id: n8))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 1, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n8", "color": "#A6CEE3", "label": "Node(id: n8)"}, "graphery_count_degree_by_edges#edge": {"id": 9, "color": "#1F78B4", "label": "(Node(id: n6), Node(id: n8))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n8", "color": "#A6CEE3", "label": "Node(id: n8)"}, "graphery_count_degree_by_edges#edge": {"id": 12, "color": "#1F78B4", "label": "(Node(id: n11), Node(id: n12))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n11", "color": "#A6CEE3", "label": "Node(id: n11)"}, "graphery_count_degree_by_edges#edge": {"id": 12, "color": "#1F78B4", "label": "(Node(id: n11), Node(id: n12))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n11", "color": "#A6CEE3", "label": "Node(id: n11)"}, "graphery_count_degree_by_edges#edge": {"id": 12, "color": "#1F78B4", "label": "(Node(id: n11), Node(id: n12))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n12", "color": "#A6CEE3", "label": "Node(id: n12)"}, "graphery_count_degree_by_edges#edge": {"id": 12, "color": "#1F78B4", "label": "(Node(id: n11), Node(id: n12))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 1, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n12", "color": "#A6CEE3", "label": "Node(id: n12)"}, "graphery_count_degree_by_edges#edge": {"id": 12, "color": "#1F78B4", "label": "(Node(id: n11), Node(id: n12))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n12", "color": "#A6CEE3", "label": "Node(id: n12)"}, "graphery_count_degree_by_edges#edge": {"id": 2, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n3))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n1", "color": "#A6CEE3", "label": "Node(id: n1)"}, "graphery_count_degree_by_edges#edge": {"id": 2, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n3))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 2, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n1", "color": "#A6CEE3", "label": "Node(id: n1)"}, "graphery_count_degree_by_edges#edge": {"id": 2, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n3))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n3", "color": "#A6CEE3", "label": "Node(id: n3)"}, "graphery_count_degree_by_edges#edge": {"id": 2, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n3))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 1, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n3", "color": "#A6CEE3", "label": "Node(id: n3)"}, "graphery_count_degree_by_edges#edge": {"id": 2, "color": "#1F78B4", "label": "(Node(id: n1), Node(id: n3))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 2, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n3", "color": "#A6CEE3", "label": "Node(id: n3)"}, "graphery_count_degree_by_edges#edge": {"id": 15, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n15))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 2, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n13", "color": "#A6CEE3", "label": "Node(id: n13)"}, "graphery_count_degree_by_edges#edge": {"id": 15, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n15))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 1, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 2, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n13", "color": "#A6CEE3", "label": "Node(id: n13)"}, "graphery_count_degree_by_edges#edge": {"id": 15, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n15))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 2, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n15", "color": "#A6CEE3", "label": "Node(id: n15)"}, "graphery_count_degree_by_edges#edge": {"id": 15, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n15))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 2, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n15", "color": "#A6CEE3", "label": "Node(id: n15)"}, "graphery_count_degree_by_edges#edge": {"id": 15, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n15))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 2, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n15", "color": "#A6CEE3", "label": "Node(id: n15)"}, "graphery_count_degree_by_edges#edge": {"id": 5, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n4))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 2, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n3", "color": "#A6CEE3", "label": "Node(id: n3)"}, "graphery_count_degree_by_edges#edge": {"id": 5, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n4))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 2, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n3", "color": "#A6CEE3", "label": "Node(id: n3)"}, "graphery_count_degree_by_edges#edge": {"id": 5, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n4))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n4", "color": "#A6CEE3", "label": "Node(id: n4)"}, "graphery_count_degree_by_edges#edge": {"id": 5, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n4))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 1, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n4", "color": "#A6CEE3", "label": "Node(id: n4)"}, "graphery_count_degree_by_edges#edge": {"id": 5, "color": "#1F78B4", "label": "(Node(id: n3), Node(id: n4))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 2, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n4", "color": "#A6CEE3", "label": "Node(id: n4)"}, "graphery_count_degree_by_edges#edge": {"id": 11, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n10))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 2, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n8", "color": "#A6CEE3", "label": "Node(id: n8)"}, "graphery_count_degree_by_edges#edge": {"id": 11, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n10))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 2, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 2, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n8", "color": "#A6CEE3", "label": "Node(id: n8)"}, "graphery_count_degree_by_edges#edge": {"id": 11, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n10))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 2, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n10", "color": "#A6CEE3", "label": "Node(id: n10)"}, "graphery_count_degree_by_edges#edge": {"id": 11, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n10))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 2, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n10", "color": "#A6CEE3", "label": "Node(id: n10)"}, "graphery_count_degree_by_edges#edge": {"id": 11, "color": "#1F78B4", "label": "(Node(id: n8), Node(id: n10))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 2, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n10", "color": "#A6CEE3", "label": "Node(id: n10)"}, "graphery_count_degree_by_edges#edge": {"id": 8, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n6))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 2, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n4", "color": "#A6CEE3", "label": "Node(id: n4)"}, "graphery_count_degree_by_edges#edge": {"id": 8, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n6))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 2, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n4", "color": "#A6CEE3", "label": "Node(id: n4)"}, "graphery_count_degree_by_edges#edge": {"id": 8, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n6))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n6", "color": "#A6CEE3", "label": "Node(id: n6)"}, "graphery_count_degree_by_edges#edge": {"id": 8, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n6))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 1, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n6", "color": "#A6CEE3", "label": "Node(id: n6)"}, "graphery_count_degree_by_edges#edge": {"id": 8, "color": "#1F78B4", "label": "(Node(id: n4), Node(id: n6))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n6", "color": "#A6CEE3", "label": "Node(id: n6)"}, "graphery_count_degree_by_edges#edge": {"id": 14, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n14))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n13", "color": "#A6CEE3", "label": "Node(id: n13)"}, "graphery_count_degree_by_edges#edge": {"id": 14, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n14))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 2, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n13", "color": "#A6CEE3", "label": "Node(id: n13)"}, "graphery_count_degree_by_edges#edge": {"id": 14, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n14))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 3, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n14", "color": "#A6CEE3", "label": "Node(id: n14)"}, "graphery_count_degree_by_edges#edge": {"id": 14, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n14))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 3, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1}"}}, {"line": 11, "variables": null}, {"line": 14, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n14", "color": "#A6CEE3", "label": "Node(id: n14)"}, "graphery_count_degree_by_edges#edge": {"id": 14, "color": "#1F78B4", "label": "(Node(id: n13), Node(id: n14))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 3, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1, Node(id: n14): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n14", "color": "#A6CEE3", "label": "Node(id: n14)"}, "graphery_count_degree_by_edges#edge": {"id": 4, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n11))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 3, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1, Node(id: n14): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n2", "color": "#A6CEE3", "label": "Node(id: n2)"}, "graphery_count_degree_by_edges#edge": {"id": 4, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n11))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 2, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 3, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1, Node(id: n14): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n2", "color": "#A6CEE3", "label": "Node(id: n2)"}, "graphery_count_degree_by_edges#edge": {"id": 4, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n11))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 3, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 3, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1, Node(id: n14): 1}"}}, {"line": 10, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n11", "color": "#A6CEE3", "label": "Node(id: n11)"}, "graphery_count_degree_by_edges#edge": {"id": 4, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n11))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 3, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 3, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 1, Node(id: n15): 1, Node(id: n10): 1, Node(id: n14): 1}"}}, {"line": 11, "variables": null}, {"line": 12, "variables": {"global#accessed var": null, "graphery_count_degree_by_edges#node": {"id": "n11", "color": "#A6CEE3", "label": "Node(id: n11)"}, "graphery_count_degree_by_edges#edge": {"id": 4, "color": "#1F78B4", "label": "(Node(id: n2), Node(id: n11))"}, "graphery_count_degree_by_edges#degree_dict": "{Node(id: n1): 3, Node(id: n2): 3, Node(id: n4): 3, Node(id: n5): 1, Node(id: n12): 2, Node(id: n13): 3, Node(id: n8): 3, Node(id: n9): 1, Node(id: n0): 1, Node(id: n3): 3, Node(id: n16): 1, Node(id: n7): 1, Node(id: n6): 2, Node(id: n11): 2, Node(id: n15): 1, Node(id: n10): 1, Node(id: n14): 1}"}}, {"line": 10, "variables": null}, {"line": 10, "variables": null}, {"line": 9, "variables": null}, {"line": 9, "variables": null}]\n';

const pseudoGraphList: Graph[] = [
  {
    id: 'eiaofj',
    isPublished: true,
    cyjs: '',
    content: {
      title: 'name2',
      abstract: 'this is a random graph',
      isPublished: true,
    },
    priority: 60,
  },
  {
    id: 'dfijaowe',
    isPublished: true,
    cyjs: '',
    content: {
      title: 'name2',
      abstract: 'this is another random graph',
      isPublished: true,
    },
    priority: 40,
  },
];

const pseudoVariableObj = {
  i: 10,
  j: 5,
  node: {
    id: 10,
    color: '#A6CEE3',
    label: 'Node(id: 10)',
  },
  edge: {
    id: 18,
    color: '#A6CEE3',
    label: 'Edge(id: 18)',
  },
};

// TODO remove the pseudo content!
const state: TutorialState = {
  metaState: null,
  articleContent: pseudoContent,
  currentGraphId: null,
  graphs: null,
  codes: null,
  resultJsonList: null,
  variableObj: null,
  // use v-for to spread graphs and make :key bind to id (or serial code?)
};

const mutations: MutationTree<TutorialState> = {
  LOAD_META_STATE(state, value: TutorialMetaState) {
    state.metaState = value;
  },
  LOAD_ARTICLE_CONTENT(state, value: TutorialArticleContent) {
    state.articleContent = value;
  },
  LOAD_CURRENT_GRAPH_ID(state, value: string) {
    state.currentGraphId = value;
  },
  LOAD_GRAPHS(state, value: TutorialGraph[]) {
    state.graphs = value;
  },
  LOAD_CODES(state, value: string) {
    state.codes = value;
  },
  LOAD_RESULT_JSON_LIST(state, value: ResultJsonType[]) {
    state.resultJsonList = value;
  },
  LOAD_VARIABLE_OBJ(state, obj) {
    state.variableObj = obj;
  },

  // clear states
  CLEAR_META_STATE(state) {
    state.metaState = null;
  },
  CLEAR_ARTICLE_CONTENT(state) {
    state.articleContent = null;
  },
  CLEAR_CURRENT_GRAPH_ID(state) {
    state.currentGraphId = null;
  },
  CLEAR_GRAPHS(state) {
    state.graphs = null;
  },
  CLEAR_CODES(state) {
    state.codes = null;
  },
  CLEAR_RESULT_JSON_LIST(state) {
    state.resultJsonList = null;
  },
  CLEAR_VARIABLE_OBJ(state) {
    state.variableObj = null;
  },
};

const actions: ActionTree<TutorialState, RootState> = {
  // TODO API calls go here
  loadTutorialMetaState({ commit }, tutorialObj: TutorialDetailResponse) {
    const metaState: TutorialMetaState = {
      articleId: tutorialObj.id,
      isAnchorPublished: tutorialObj.isPublished,
      isTransPublished: tutorialObj.content.isPublished,
      authors: tutorialObj.content.authors,
      categories: tutorialObj.categories,
      modifiedTime: tutorialObj.content.modifiedTime,
    };
    commit('LOAD_META_STATE', metaState);
  },
  loadTutorialArticleContent({ commit }, tutorialObj: TutorialDetailResponse) {
    const articleContent: TutorialArticleContent = {
      title: tutorialObj.content.title,
      contentHtml: tutorialObj.content.contentHtml,
    };
    commit('LOAD_ARTICLE_CONTENT', articleContent);
  },
  loadTutorialGraphs({ commit }, tutorialObj: TutorialDetailResponse) {
    const graphs: Graph[] = tutorialObj.graphSet;
    commit('LOAD_GRAPHS', graphs);
  },
  loadTutorialCode({ commit }, tutorialObj: TutorialDetailResponse) {
    const code: string = tutorialObj.code.code;
    commit('LOAD_CODES', code);
  },
  loadTutorialResultJsonList({ commit }, tutorialObj: TutorialDetailResponse) {
    const resultJsonList: ResultJsonType[] = [];
    tutorialObj.code.execresultjsonSet.forEach((resultJsonObj) => {
      resultJsonList.push({
        json: resultJsonObj.json,
        graphId: resultJsonObj.graph.id,
      });
    });
    commit('LOAD_RESULT_JSON_LIST', resultJsonList);
  },
  loadTutorial({ dispatch }, tutorialObj: TutorialDetailResponse) {
    console.debug('received tutorial detail obj', tutorialObj);

    dispatch('loadTutorialMetaState', tutorialObj);
    dispatch('loadTutorialArticleContent', tutorialObj);
    dispatch('loadTutorialGraphs', tutorialObj);
    dispatch('loadTutorialCode', tutorialObj);
    dispatch('loadTutorialResultJsonList', tutorialObj);
  },
  loadVariableObj({ commit }, list) {
    commit('LOAD_VARIABLE_OBJ', list);
  },
  clearAll({ commit }) {
    commit('CLEAR_META_STATE');
    commit('CLEAR_ARTICLE_CONTENT');
    commit('CLEAR_CURRENT_GRAPH_ID');
    commit('CLEAR_GRAPHS');
    commit('CLEAR_CODES');
    commit('CLEAR_RESULT_JSON_LIST');
    commit('CLEAR_VARIABLE_OBJ');
  },
};

const getters: GetterTree<TutorialState, RootState> = {
  title(state) {
    return state.articleContent && state.articleContent.title;
    // return state.articleContent ? state.articleContent.title : null;
  },
  htmlContent(state) {
    return state.articleContent && state.articleContent.contentHtml;
    // return state.articleContent ? state.articleContent.content : null;
  },
  authors(state) {
    return state.metaState && state.metaState.authors;
  },
  categories(state) {
    return state.metaState && state.metaState.categories;
  },
  articleModTime(state) {
    return state.metaState && state.metaState.modifiedTime;
  },
  articleEmpty(state) {
    return state.articleContent === null;
  },
  isAnchorPublished(state) {
    return state.metaState && state.metaState.isAnchorPublished;
  },
  isTransPublished(state) {
    return state.metaState && state.metaState.isTransPublished;
  },
  graphsEmpty(state) {
    return state.graphs === null;
  },
  codesEmpty(state) {
    return state.codes === null;
  },
  resultJsonArrEmpty(state, getter) {
    return getter.resultJsonArr.length === 0;
  },
  resultJsonArr(state, getter) {
    if (getter.resultJson === null) {
      return [];
    }
    return JSON.parse(getter.resultJson);
  },
  variableObjEmpty(state, getter) {
    return (
      getter.codesEmpty || getter.graphsEmpty || state.variableObj === null
    );
  },
  getGraphList(state) {
    const arr: { label: string; value: string }[] = [];
    if (!state.graphs) {
      return arr;
    }

    state.graphs.forEach((value) => {
      arr.push({
        label: value.content.title,
        value: value.id,
      });
    });

    return arr;
  },
  resultJson(state) {
    if (state.resultJsonList) {
      const resultJsonObj = state.resultJsonList.find(
        (r) => r.graphId === state.currentGraphId
      );
      if (resultJsonObj) {
        return resultJsonObj.json;
      }
    }

    return null;
  },
  getGraphById: (state) => (id: string) => {
    // TODO may return undefined
    return state.graphs && state.graphs.find((g) => g.id === id);
  },
  getGraphByIndex: (state) => (index: number) => {
    return state.graphs && state.graphs[index];
  },
  currentGraph(state, getter) {
    return getter.getGraphById(state.currentGraphId) || null;
  },
  currentGraphJsonObj(state, getter) {
    if (getter.currentGraph && getter.currentGraph.cyjs) {
      // which should always happen since the graphs are chosen by ids which corresponds
      // defined graphs
      return JSON.parse(getter.currentGraph.cyjs);
    }
    return null;
  },
  currentGraphContent(state, getter) {
    if (getter.currentGraph && getter.currentGraph.content) {
      return getter.currentGraph.content;
    }
    return null;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
