<template>
  <div>{{ initElement }}</div>
</template>

<script>
  import {
    _GRAPH_OBJECT_TYPES,
    _LINEAR_CONTAINER_TYPES,
    _PAIR_CONTAINER_TYPES,
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
      return {};
    },
    computed: {
      element() {
        return this.initElement;
      },
      elementType() {
        return this.initElement[_TYPE_HEADER];
      },
      content() {
        return this.element[_REPR_HEADER];
      },
    },
    methods: {
      emitForwardAction(name, element) {
        this.$emit('pushVariableStack', name, element);
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
    },
    watch: {
      element: function(newElements) {
        this.$emit('clearHighlight');

        const graphIds = '';

        if (
          this.isGraphElement(newElements) &&
          this.isSingularElement(newElements)
        ) {
          // TODO change graphIds
          this.$emit('highlight', graphIds);
        } else if (this.isLinearContainerElement(newElements)) {
          // TODO change graphIds
          this.$emit('highlight', graphIds);
        } else if (this.isPairContainerElement(newElements)) {
          // TODO change graphIds
          this.$emit('highlight', graphIds);
        }
      },
    },
  };
</script>
