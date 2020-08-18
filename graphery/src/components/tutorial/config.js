export const panzoomDefaults = {
  zoomFactor: 0.1, // zoom factor per zoom tick
  zoomDelay: 45, // how many ms between zoom ticks
  minZoom: 0.1, // min zoom level
  maxZoom: 10, // max zoom level
  fitPadding: 50, // padding when fitting
  panSpeed: 10, // how many ms in between pan ticks
  panDistance: 100, // max pan distance per tick
  panDragAreaSize: 75, // the length of the pan drag box in which the vector for panning is calculated (bigger = finer control of pan speed and direction)
  panMinPercentSpeed: 0.25, // the slowest speed we can pan by (as a percent of panSpeed)
  panInactiveArea: 8, // radius of inactive area in pan drag box
  panIndicatorMinOpacity: 0.5, // min opacity of pan indicator (the draggable nib) scales from this to 1.0
  zoomOnly: false, // a minimal version of the ui only with zooming (useful on systems with bad mousewheel resolution)
  fitSelector: undefined, // selector of elements to fit
  animateOnFit: function() {
    // whether to animate on fit
    return false;
  },
  fitAnimationDuration: 1000, // duration of animation on fit
  sliderHandleIcon: 'mdi mdi-minus',
  zoomInIcon: 'mdi mdi-plus',
  zoomOutIcon: 'mdi mdi-minus',
  resetIcon: 'mdi mdi-arrow-expand-all',
};

export const fcoseOptions = {
  name: 'fcose',
  // 'draft', 'default' or 'proof'
  // - "draft" only applies spectral layout
  // - "default" improves the quality with incremental layout (fast cooling rate)
  // - "proof" improves the quality with incremental layout (slow cooling rate)
  quality: 'default',
  // Use random node positions at beginning of layout
  // if this is set to false, then quality option must be "proof"
  randomize: true,
  // Whether or not to animate the layout
  animate: true,
};

export const presetOptions = {
  name: 'preset',

  positions: undefined, // map of (node id) => (position obj); or function(node){ return somPos; }
  zoom: undefined, // the zoom level to set (prob want fit = false if set)
  pan: undefined, // the pan level to set (prob want fit = false if set)
  fit: true, // whether to fit to viewport
  padding: 30, // padding on fit
  animate: false, // whether to transition the node positions
  animationDuration: 500, // duration of animation in ms if enabled
  animationEasing: undefined, // easing of animation if enabled
  animateFilter: function(node, i) {
    return true;
  }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
  ready: undefined, // callback on layoutready
  stop: undefined, // callback on layoutstop
  transform: function(node, position) {
    return position;
  }, // transform a given node position. Useful for changing flow direction in discrete layouts
};

export const dagreOptions = {
  name: 'dagre',
  // dagre algorithm options, uses default value on undefined
  nodeSep: 15, // the separation between adjacent nodes in the same rank
  edgeSep: 10, // the separation between adjacent edges in the same rank
  rankSep: 30, // the separation between adjacent nodes in the same rank
  rankDir: 'TB', // 'TB' for top to bottom flow, 'LR' for left to right
  minLen: function(_) {
    return 1;
  }, // number of ranks to keep between the source and target of the edge
  edgeWeight: function(_) {
    return 1;
  }, // higher weight edges are generally made shorter and straighter than lower weight edges
  // general layout options
  fit: true, // whether to fit to viewport
  padding: 50, // fit padding
  spacingFactor: 1.2, // Applies a multiplicative factor (>0) to expand or compress the overall area that the nodes take up
  animate: true, // whether to transition the node positions
  animationDuration: 500, // duration of animation in ms if enabled
  animationEasing: undefined, // easing of animation if enabled
  boundingBox: undefined, // constrain layout bounds { x1, y1, x2, y2 } or { x1, y1, w, h }
  ready: function() {
    this.layoutReady = true;
    this.layoutStopped = false;
  },
  stop: function() {
    this.layoutStopped = true;
    this.layoutReady = false;
    this.loading = false;
  },
};

export const randomLayout = {
  name: 'random',

  fit: true, // whether to fit to viewport
  padding: 30, // fit padding
  boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
  animate: false, // whether to transition the node positions
  animationDuration: 500, // duration of animation in ms if enabled
  animationEasing: undefined, // easing of animation if enabled
  animateFilter: function(node, i) {
    return true;
  }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
  ready: undefined, // callback on layoutready
  stop: undefined, // callback on layoutstop
  transform: function(node, position) {
    return position;
  }, // transform a given node position. Useful for changing flow direction in discrete layouts
};

export const GraphLayout = {
  dagre: dagreOptions,
  fcose: fcoseOptions,
  preset: presetOptions,
  random: randomLayout,
};
