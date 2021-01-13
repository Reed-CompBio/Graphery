<template>
  <div>
    <div class="header">
      <div id="header-wrapper" class="row q-my-xs justify-center">
        <div id="back-button" class="col" style="flex-grow: 1;">
          <div class="row" style="flex-wrap: nowrap; justify-content: left;">
            <q-btn
              flat
              dense
              :size="btnSize"
              :disable="!showPreviousButton"
              icon="mdi-backburger"
              @click="emitBackAction"
            />
          </div>
        </div>
        <div class="col" style="flex-wrap: nowrap;">
          <div class="row justify-center">
            <div
              id="name-section"
              :class="toggleStateClass"
              :style="{ 'background-color': elementColor }"
            >
              <code>
                {{ elementName }}
              </code>
            </div>
          </div>
        </div>
        <div id="right-section" class="col" style="flex-grow: 1;">
          <div class="row justify-end" style="flex-wrap: nowrap;">
            <div id="toggle-section">
              <q-btn
                flat
                dense
                :disable="isInitEle"
                :size="btnSize"
                :icon="hightlightButtonIcon"
                @click="emitToggleAction"
              >
              </q-btn>
            </div>
            <div id="icon-section">
              <div>
                <q-btn
                  flat
                  dense
                  round
                  :size="btnSize"
                  :icon="elementIcon"
                  @click="typeButtonClickHandler"
                >
                  <SwitchTooltip :text="`Type: ${displayedElementType}`" />
                </q-btn>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {
    _EMPTY_VALUE_STRING,
    _INIT_ICON,
    _INIT_TYPE_STRING,
    _TYPE_HEADER,
    _TYPE_ICON_ENUM,
  } from '@/components/framework/VariableListComponents/variableListConstants';
  import SwitchTooltip from '@/components/framework/SwitchTooltip';
  import { successDialog } from '@/services/helpers';
  import {
    isInitElement,
    isLinearContainerElement,
    isPairContainerElement,
    isSingularElement,
  } from '@/components/framework/GraphEditorControls/ElementsUtils';

  export default {
    components: { SwitchTooltip },
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
      initToggleState: {
        type: Number,
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
      displayedElementType() {
        if (this.elementType === _INIT_TYPE_STRING) {
          return 'Unknown';
        }
        return this.elementType;
      },
      elementName() {
        return this.initElementName;
      },
      elementColor() {
        return this.initElementColor;
      },
      elementIcon() {
        return _TYPE_ICON_ENUM[this.elementType] || _INIT_ICON;
      },
      toggleState() {
        return this.initToggleState;
      },
      isInitEle() {
        return isInitElement(this.element);
      },
      hightlightButtonIcon() {
        if (
          isSingularElement(this.element) ||
          isLinearContainerElement(this.element)
        ) {
          if (this.toggleState) {
            return 'mdi-lightbulb';
          } else {
            return 'mdi-lightbulb-off-outline';
          }
        } else if (isPairContainerElement(this.element)) {
          switch (this.toggleState) {
            case 1:
              return 'mdi-alpha-k';
            case 2:
              return 'mdi-alpha-v';
            case 0:
              return 'mdi-lightbulb-off-outline';
          }
        }
        // which should never happen
        return 'mdi-close-circle-outline';
      },
      toggleStateClass() {
        if (
          isSingularElement(this.element) ||
          isLinearContainerElement(this.element)
        ) {
          return {
            'toggle-on': Boolean(this.toggleState),
            'toggle-off': Boolean(!this.toggleState),
          };
        } else if (isPairContainerElement(this.element)) {
          return {
            'toggle-key-on': this.toggleState === 1,
            'toggle-value-on': this.toggleState === 2,
            'toggle-off': this.toggleState === 0,
          };
        } else {
          return ['toggle-off'];
        }
      },
    },
    methods: {
      emitBackAction() {
        this.$emit('popVariableStack');
      },
      emitToggleAction() {
        this.$emit('toggleAction');
      },
      typeButtonClickHandler() {
        successDialog(
          {
            message: `The element '${this.elementName}' has type ${this.displayedElementType}`,
          },
          2000
        );
      },
    },
  };
</script>

<style scoped lang="sass">
  #name-section
    font-size: 17px
    padding: .15rem .3rem
    border-radius: 0.4rem
    opacity: .8
    text-overflow: ellipsis
    overflow: hidden
    &.toggle-off
      opacity: .3
    code
      text-wrap: normal
      transform: scaleX(0.9)
  .header
    padding: 0 8px
</style>
