<template>
  <div>{{ initElement }}</div>
</template>

<script>
  import {
    _COLOR_HEADER,
    _GRAPH_ELEMENT_SEPARATOR,
    _GRAPH_OBJECT_TYPES,
    _INIT_TYPE_STRING,
    _LABEL_HEADER,
    _LINEAR_CONTAINER_TYPES,
    _PAIR_CONTAINER_TYPES,
    _PAIR_KEY_HEADER,
    _PAIR_VALUE_HEADER,
    _REPR_HEADER,
    _SINGULAR_TYPES,
    _TYPE_HEADER,
  } from '@/components/framework/VariableListComponents/variableListConstants';

  export default {
    props: {
      initElement: {
        type: Object,
      },
    },
    data() {
      return {
        toggleState_: 1,
      };
    },
    computed: {
      element() {
        return this.initElement;
      },
      elementType() {
        return this.element[_TYPE_HEADER];
      },
      variableName() {
        return this.element[_LABEL_HEADER];
      },
      isGraphEle() {
        return this.isGraphElement(this.element);
      },
      isSingularEle() {
        return this.isSingularElement(this.element);
      },
      isLinearContainerEle() {
        return this.isLinearContainerElement(this.element);
      },
      isPairContainerEle() {
        return this.isPairContainerElement(this.element);
      },
      isInitEle() {
        return this.isInitElement(this.element);
      },
      variableColor() {
        return this.element[_COLOR_HEADER];
      },
      variableContent() {
        return this.element[_REPR_HEADER];
      },
      graphElementIds() {
        return this.generateHighlightIds(this.element);
      },
      elementClassName() {
        return this.variableName;
      },
      elementKeyClassName() {
        return `${this.variableName}_${_PAIR_KEY_HEADER}`;
      },
      elementValueClassName() {
        return `${this.variableName}_${_PAIR_VALUE_HEADER}`;
      },
    },
    methods: {
      emitForwardAction(name, element) {
        this.$emit('pushVariableStack', name, element);
      },
      resetToggleState() {
        this.toggleState_ = 1;
      },
      toggleVar() {
        this.toggleState_ += 1;
        if (this.isGraphEle && this.isSingularEle) {
          this.$emit('toggle', this.elementClassName, this.toggleState_);
          this.toggleState_ %= 2;
        } else if (this.isLinearContainerEle) {
          this.$emit('toggle', this.elementClassName, this.toggleState_);
          this.toggleState_ %= 2;
        } else if (this.isPairContainerEle) {
          this.$emit(
            'toggle',
            this.elementKeyClassName,
            !((this.toggleState_ + 1) % 3)
          );
          this.$emit(
            'toggle',
            this.elementValueClassName,
            !((this.toggleState_ - 1) % 3)
          );
        }
      },
      isGraphElement(element) {
        return element in _GRAPH_OBJECT_TYPES;
      },
      isSingularElement(element) {
        return element in _SINGULAR_TYPES;
      },
      isLinearContainerElement(element) {
        return element in _LINEAR_CONTAINER_TYPES;
      },
      isPairContainerElement(element) {
        return element in _PAIR_CONTAINER_TYPES;
      },
      isInitElement(element) {
        return element === _INIT_TYPE_STRING;
      },
      _makeIdFromObj(obj) {
        return `#${obj['id']}`;
      },
      generateHighlightIds(element) {
        if (this.isGraphElement(element) && this.isSingularElement(element)) {
          return this._makeIdFromObj(element);
        } else if (this.isLinearContainerElement(element)) {
          return [
            element
              .map((v) => this._makeIdFromObj(v))
              .join(_GRAPH_ELEMENT_SEPARATOR),
            null,
          ];
        } else if (this.isPairContainerElement(element)) {
          const keys = [];
          const values = [];

          element.forEach((v) => {
            keys.push(v[_PAIR_KEY_HEADER]);
            values.push(v[_PAIR_VALUE_HEADER]);
          });

          return [
            keys.join(_GRAPH_ELEMENT_SEPARATOR),
            values.join(_GRAPH_ELEMENT_SEPARATOR),
          ];
        } else {
          return null;
        }
      },
    },
    watch: {
      element: function(newElements) {
        this.resetToggleState();
        this.$emit('clearHighlight');

        const graphIds = this.generateHighlightIds(newElements);

        if (graphIds === null) {
          return;
        }

        if (typeof graphIds === 'string' || graphIds instanceof String) {
          this.$emit('highlight', this.variableName, graphIds);
        } else if (Array.isArray(graphIds)) {
          if (graphIds[1] === null) {
            this.$emit('highlight', this.variableName, graphIds[0]);
          } else if (graphIds[1] !== null) {
            this.$emit(
              'highlight',
              `${this.variableName}_${_PAIR_KEY_HEADER}`,
              graphIds[0]
            );
            this.$emit(
              'highlight',
              `${this.variableName}_${_PAIR_VALUE_HEADER}`,
              graphIds[1]
            );
          }
        }
      },
    },
  };
</script>
