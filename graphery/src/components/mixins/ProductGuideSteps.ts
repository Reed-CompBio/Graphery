import i18n from '@/i18n';

export const startIntro = [
  {
    title: i18n.tc('product guide.ui.intro title') + ' 👋 ',
    intro: i18n.tc('product guide.ui.intro'),
  },
];

export const tutorialUIProductGuide = [
  {
    element: '#articleWrapper',
    intro: i18n.tc('product guide.ui.tutorial section'),
  },
];

export const graphUIProductGuide = [
  {
    element: '#cy-wrapper',
    intro: i18n.tc('product guide.ui.graph section'),
  },
  {
    element: '#cy-wrapper',
    intro: i18n.tc('product guide.graph window.drag node and view port'),
  },
  {
    element: '#cy-wrapper',
    intro: i18n.tc('product guide.graph window.lasso tool'),
  },
  {
    element: '#graph-selector',
    intro: i18n.tc('product guide.graph window.choose graphs'),
  },
];

export const editorProductGuide = [
  {
    element: '#editor-panel',
    intro: i18n.tc('product guide.ui.editor section'),
  },
  {
    element: '#variable-list-wrapper',
    intro: i18n.tc('product guide.ui.variable list section'),
  },
  {
    element: '#editor-control-unit',
    intro: i18n.tc('product guide.ui.control unit'),
  },
];

export const controlUnitProductGuide = [
  {
    element: '#control-unit-forward-button',
    intro: i18n.tc('product guide.control unit.forward button'),
  },
  {
    element: '#control-unit-step-control-button-group',
    intro: i18n.tc('product guide.control unit.step control group'),
  },
  {
    element: '#control-unit-stepper-slider',
    intro: i18n.tc('product guide.control unit.slider'),
  },
  {
    element: '#control-unit-editor-lock',
    intro: i18n.tc('product guide.control unit.edit lock'),
  },
];
