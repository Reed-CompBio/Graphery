<template>
  <div id="tippy-component">
    <q-card flat>
      <div id="tippy-element-id-wrapper">
        <code id="tippy-element-id-code">
          {{ elementName }}
        </code>
      </div>
      <div>
        <TippyElementPropertyDisplay :initElementProperty="elementProperty" />
      </div>
    </q-card>
  </div>
</template>

<script>
  import TippyElementPropertyDisplay from '@/components/framework/TippyComponents/TippyElementPropertyDisplay';
  export default {
    components: { TippyElementPropertyDisplay },
    props: ['initElement'],
    computed: {
      elementName() {
        return this.initElement['name'];
      },
      elementProperty() {
        return this.initElement['property'];
      },
    },
  };
</script>

<style lang="sass" scoped>
  #tippy-element-id-code
    padding: .2em .4em
    margin: 0
    font-size: 85%
    background-color: rgba(27, 31, 35, 0.15)
    border-radius: 6px
</style>
