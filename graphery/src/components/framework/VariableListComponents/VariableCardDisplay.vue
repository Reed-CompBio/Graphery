<template>
  <div id="display-wrapper">
    <div id="singular-element" v-if="isSingularEle || isInitEle">
      <SingularElementLayout :init-element="element" v-on="$listeners" />
    </div>
    <div id="linear-container-element" v-if="isLinearContainerEle">
      <LinearContainerElementLayout :init-element="element" v-on="$listeners" />
    </div>
    <div id="pair-container-element" v-if="isPairContainerEle">
      <PairContainerElementLayout :init-element="element" v-on="$listeners" />
    </div>
  </div>
</template>

<script>
  import {
    _COLOR_HEADER,
    _GRAPH_ELEMENT_SEPARATOR,
    _LABEL_HEADER,
    _PAIR_KEY_HEADER,
    _PAIR_VALUE_HEADER,
    _REPR_HEADER,
    _TYPE_HEADER,
  } from '@/components/framework/VariableListComponents/variableListConstants';
  import {
    isGraphElement,
    isInitElement,
    isLinearContainerElement,
    isPairContainerElement,
    isSingularElement,
    makeIdFromObject,
    nameComboToClassName,
  } from '@/components/framework/GraphEditorControls/ElementsUtils';
  import SingularElementLayout from '@/components/framework/VariableListComponents/layouts/SingularElementLayout';
  import PairContainerElementLayout from '@/components/framework/VariableListComponents/layouts/PairContainerElementLayout';
  import LinearContainerElementLayout from '@/components/framework/VariableListComponents/layouts/LinearContainerElementLayout';

  export default {
    components: {
      LinearContainerElementLayout,
      PairContainerElementLayout,
      SingularElementLayout,
    },
    props: {
      initElement: {
        type: Object,
      },
      initRootElementName: {
        type: String,
      },
    },
    computed: {
      element() {
        return this.initElement;
      },
      elementType() {
        return this.element[_TYPE_HEADER];
      },
      variableLabel() {
        return this.element[_LABEL_HEADER];
      },
      isGraphEle() {
        return isGraphElement(this.element);
      },
      isSingularEle() {
        return isSingularElement(this.element);
      },
      isLinearContainerEle() {
        return isLinearContainerElement(this.element);
      },
      isPairContainerEle() {
        return isPairContainerElement(this.element);
      },
      isInitEle() {
        return isInitElement(this.element);
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
        return nameComboToClassName(this.initRootElementName);
      },
      elementKeyClassName() {
        return `${this.elementClassName}_${_PAIR_KEY_HEADER}`;
      },
      elementValueClassName() {
        return `${this.elementClassName}_${_PAIR_VALUE_HEADER}`;
      },
    },
    methods: {
      emitForwardAction(name, element) {
        this.$emit('pushVariableStack', name, element);
      },
      toggleVar(toggleState) {
        toggleState += 1;
        if (this.isGraphEle && this.isSingularEle) {
          this.$emit(
            'toggle',
            this.graphElementIds,
            this.elementClassName,
            toggleState % 2
          );
          this.$emit('toggleStateChange', toggleState % 2);
        } else if (this.isLinearContainerEle) {
          this.$emit(
            'toggle',
            this.graphElementIds[0],
            this.elementClassName,
            toggleState % 2
          );
          this.$emit('toggleStateChange', toggleState % 2);
        } else if (this.isPairContainerEle) {
          this.$emit(
            'toggle',
            this.graphElementIds[0],
            this.elementKeyClassName,
            !((toggleState + 1) % 3)
          );
          this.$emit(
            'toggle',
            this.graphElementIds[1],
            this.elementValueClassName,
            !((toggleState - 1) % 3)
          );
          this.$emit('toggleStateChange', toggleState % 3);
        } else {
          this.$emit('toggleStateChange', toggleState % 2);
        }
      },
      generateHighlightIds(element) {
        if (isGraphElement(element) && isSingularElement(element)) {
          return makeIdFromObject(element);
        } else if (isLinearContainerElement(element)) {
          const temp = [];
          const elementReprObj = element[_REPR_HEADER];
          for (let i = 0; i < elementReprObj.length; i++) {
            const elementObject = elementReprObj[i];
            if (isGraphElement(elementObject)) {
              temp.push(makeIdFromObject(elementObject));
            }
          }
          return [temp.join(_GRAPH_ELEMENT_SEPARATOR), null];
        } else if (isPairContainerElement(element)) {
          const keys = [];
          const values = [];

          element[_REPR_HEADER].forEach((v) => {
            const keyElement = v[_PAIR_KEY_HEADER];
            if (isGraphElement(keyElement)) {
              keys.push(makeIdFromObject(keyElement));
            }
            const valueElement = v[_PAIR_VALUE_HEADER];
            if (isGraphElement(valueElement)) {
              values.push(makeIdFromObject(valueElement));
            }
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
        const elementClassName = this.elementClassName;
        const elementClassKeyName = `${elementClassName}_${_PAIR_KEY_HEADER}`;
        const elementClassValueName = `${elementClassName}_${_PAIR_VALUE_HEADER}`;

        this.$emit('clearHighlight', elementClassName);
        this.$emit('clearHighlight', elementClassKeyName);
        this.$emit('clearHighlight', elementClassValueName);

        const graphIds = this.generateHighlightIds(newElements);

        if (!graphIds) {
          return;
        }

        if (typeof graphIds === 'string' || graphIds instanceof String) {
          this.$emit('highlight', elementClassName, graphIds);
        } else if (Array.isArray(graphIds) && graphIds.length === 2) {
          if (graphIds[1] === null) {
            this.$emit('highlight', elementClassName, graphIds[0]);
          } else if (graphIds[1] !== null) {
            this.$emit('highlight', elementClassKeyName, graphIds[0]);
            this.$emit('highlight', elementClassValueName, graphIds[1]);
          }
        }
      },
    },
  };
</script>

<style lang="sass" scoped>
  #display-wrapper
    padding: 0 5px
</style>
