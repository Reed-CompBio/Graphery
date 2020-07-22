<template>
  <div>
    <q-splitter class="full-height" v-model="splitPos">
      <template v-slot:before>
        <div>
          <textarea></textarea>
        </div>
      </template>
      <template v-slot:separator>
        <div
          style="border-left: 4px solid rgb(179, 179, 179); border-radius: 25px; height: 10%;"
        ></div>
      </template>
      <template v-slot:after>
        <div>
          <MarkdownSection
            ref="markdownSection"
            :source="rawText"
          ></MarkdownSection>
        </div>
      </template>
    </q-splitter>
  </div>
</template>

<script>
  export default {
    components: {
      MarkdownSection: () => import('./MarkdownSection'),
    },
    data() {
      return {
        rawText: '',
        splitPos: 50,
      };
    },
    methods: {
      getRawText() {
        return this.rawText;
      },
      getProcessedHtml() {
        return this.$refs.markdownSection.getProcessedHtml();
      },
    },
  };
</script>
