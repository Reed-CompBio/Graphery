<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <!-- this is for displaying graph -->
      </v-col>
      <v-col>
        <!-- this is for displaying tutorials -->
        <article :v-html="articleHtml"></article>
        <!-- the tutorial goes in here -->
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    props: ['name'],
    data() {
      return {
        articleHtml: '',
      };
    },
    methods: {
      getPageContent() {
        // TODO API Calls to get page conentent
      },
    },
  };
</script>
