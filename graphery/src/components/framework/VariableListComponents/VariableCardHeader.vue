<template>
  <div>
    <div class="header">
      <div id="header-wrapper" class="row q-my-xs">
        <div id="back-button" style="display: inline;">
          <q-btn
            flat
            dense
            :size="btnSize"
            :disable="!showPreviousButton"
            icon="mdi-backburger"
            @click="emitBackAction"
          />
        </div>
        <q-space />
        <div
          id="name-section"
          @click="emitToggleAction"
          :style="{ 'background-color': elementColor }"
        >
          <code>
            {{ elementName }}
          </code>
        </div>
        <q-space />
        <div id="toggle-section">
          <q-btn flat dense :size="btnSize" icon="mdi-lightbulb-multiple">
            <q-menu>
              <q-list dense>
                <q-item>
                  <q-btn
                    dense
                    flat
                    :size="btnSize"
                    icon="mdi-lightbulb-multiple"
                  />
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
        <div id="icon-section">
          <q-btn flat dense :size="btnSize" disable :icon="elementIcon" />
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
      initElementColor: {
        type: String,
      },
    },
    data() {
      return {
        dropdownModel: false,
        btnSize: 'md',
      };
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
      elementColor() {
        return this.initElementColor;
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
    font-size: 17px
    padding: .01rem .3rem
    border-radius: 2rem
    opacity: .8
    code
      text-wrap: normal
      transform: scaleX(0.9)
  .header
    padding: 0 8px
</style>
