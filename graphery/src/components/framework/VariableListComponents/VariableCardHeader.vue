<template>
  <div>
    <div class="header">
      <div id="header-wrapper" class="row">
        <div id="back-button" style="display: inline;">
          <q-btn
            flat
            dense
            size="sm"
            :disable="!showPreviousButton"
            icon="mdi-backburger"
            @click="emitBackAction"
          />
          <q-tooltip
            v-if="!showPreviousButton"
            anchor="top middle"
            content-style="font-size: 13px"
            :offset="[10, 35]"
          >
            It's now at the <strong>root</strong>!
          </q-tooltip>
        </div>
        <q-space />
        <div id="name-section" @click="emitToggleAction">
          {{ elementName }}
        </div>
        <q-space />
        <div id="icon-section">
          <q-btn flat dense size="sm" disable :icon="elementIcon" />
        </div>
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

<style scoped lang="sass">
  #name-section
    display: flex
    align-self: center
    font-size: 15px
  .header
    padding: 0px 8px
</style>
