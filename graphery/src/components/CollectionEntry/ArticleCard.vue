<template>
  <div class="q-mx-sm q-my-lg">
    <q-intersection once transition="scale" class="expandable-helper">
      <q-card class="article-card-wrapper">
        <section>
          <h5>
            {{ title }}
          </h5>
        </section>
        <section>
          <div>
            <q-chip clickable v-if="!isAnchorPublished" icon="mdi-book-lock">
              Anchor Not Published
            </q-chip>
            <q-chip clickable v-if="!isTransPublished" icon="mdi-book-lock">
              Translation Not Published
            </q-chip>
          </div>
          <div>
            <q-chip v-if="noContentNoClick" icon="link">
              {{ url }}
            </q-chip>
            <q-chip
              clickable
              v-for="author in authors"
              :key="author"
              icon="mdi-card-account-details"
              @click="$emit('author-filter', author)"
            >
              {{ author }}
            </q-chip>
            <q-chip
              clickable
              v-for="category in categories"
              :key="category"
              icon="category"
              @click="$emit('category-filter', category)"
            >
              {{ category }}
            </q-chip>
            <q-chip icon="mdi-calendar-month">
              {{ toLocalDateString($i18n.locale, modifiedTime) }}
            </q-chip>
          </div>
        </section>
        <section class="article-abstract-section q-mx-md">
          <div class="q-mb-sm" v-html="abstract"></div>
        </section>
        <q-card-actions>
          <q-btn :to="`/tutorial/${url}`" :disable="noContentNoClick">
            Read More
          </q-btn>
        </q-card-actions>
      </q-card>
    </q-intersection>
  </div>
</template>

<script>
  import { toLocalDateString } from '../../services/helpers';
  const noContentTitle = '<None>';

  export default {
    props: [
      'title',
      'authors',
      'categories',
      'modifiedTime',
      'abstract',
      'url',
      'isTransPublished',
      'isAnchorPublished',
    ],
    methods: {
      toLocalDateString,
    },
    computed: {
      noContentNoClick() {
        return this.title === noContentTitle;
      },
    },
  };
</script>

<style lang="sass">
  .article-card-wrapper
    padding: 3px 20px
    h5
      margin: 10px 0px
    .article-abstract-section
      margin-top: 15px
</style>
