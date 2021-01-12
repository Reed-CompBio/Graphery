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
            <!-- TODO: Use predefined tooltip component-->
            <q-tooltip
              v-if="!showPreviousButton"
              anchor="top middle"
              content-style="font-size: 13px"
              :offset="[10, 35]"
            >
              It's now at the <strong>root</strong>!
            </q-tooltip>
          </div>
        </div>

        <div class="col">
          <div
            @click="emitToggleAction"
            class="row no-wrap justify-center"
            style="padding-top: 5px"
          >
            <div
              id="name-section"
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
                :size="btnSize"
                icon="mdi-lightbulb-multiple"
                disable
              >
                <q-menu> </q-menu>
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
  #header-wrapper
    flex-wrap: nowrap
  #name-section
    font-size: 17px
    padding: .2rem .3rem
    border-radius: 2rem
    opacity: .8
    text-overflow: ellipsis
    overflow: hidden

    code
      //text-wrap: normal
      transform: scaleX(0.9)
  .header
    padding: 0 8px

  .name-background
    display: flex
    justify-content: center
    flex: initial
    background-color: yellow
    margin-top: -4px // cover full header height: VariableList.vue > .variable-card
</style>
