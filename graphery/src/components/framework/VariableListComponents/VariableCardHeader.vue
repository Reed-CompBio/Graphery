<template>
  <div>
    <div class="q-pa-sm">
      <div id="back-button" v-if="showPreviousButton">
        <q-btn @click="emitBackAction"> </q-btn>
      </div>
      <q-space />
      <div id="name-section" @click="emitToggleAction">
        {{ elementName }}
      </div>
      <q-space />
      <div id="icon-section">
        <q-icon :name="elementIcon" />
      </div>
    </div>
  </div>
</template>

<script>
  import {
    _EMPTY_VALUE_STRING,
    _TYPE_HEADER,
    _TYPE_ICON_ENUM,
  } from '@/components/framework/VariableListComponents/variableListConstants';

  export default {
    props: {
      hasPrevious: {
        type: Boolean,
        default: false,
      },
      initElementName: {
        type: String,
        default: _EMPTY_VALUE_STRING,
      },
      initElement: {
        type: Object,
        default: null,
      },
    },
    computed: {
      element() {
        return this.initElement;
      },
      showPreviousButton() {
        return this.hasPrevious;
      },
      elementType() {
        return this.element[_TYPE_HEADER];
      },
      elementName() {
        return this.initElementName;
      },
      elementIcon() {
        return _TYPE_ICON_ENUM[this.elementType] || 'mdi-comment-question';
      },
    },
    methods: {
      emitBackAction() {
        this.$emit('popVariableStack');
      },
      emitToggleAction() {
        this.$emit('toggleAction');
      },
    },
  };
</script>
