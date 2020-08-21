<template>
  <div id="graph-info-container" class="full-height" style="overflow-y: auto;">
    <div class="q-ma-lg">
      <q-card class="q-pa-sm full-height">
        <q-card-section>
          <h5 style="margin: 5px 0;">
            Graph Info
          </h5>
        </q-card-section>
        <q-card-section>
          <GraphInfoItem
            title="Graph Name: "
            :content="graphName"
          ></GraphInfoItem>
          <GraphInfoItem
            title="Is Published? "
            :content="isPublished ? '✅' : '❌'"
          ></GraphInfoItem>
          <GraphInfoItem title="Abstract: ">
            <MarkdownSection :input-html="abstract" />
          </GraphInfoItem>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
  export default {
    props: ['graphName', 'isPublished', 'abstract'],
    components: {
      MarkdownSection: () => import('@/components/framework/MarkdownSection'),
      GraphInfoItem: () => import('@/components/tutorial/GraphInfoItem.vue'),
    },
  };
</script>

<style lang="sass"></style>
