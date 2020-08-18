<template>
  <div class="q-my-lg">
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
              :key="category.id"
              icon="category"
              @click="$emit('category-filter', category.id)"
            >
              {{ category.category }}
            </q-chip>
            <q-chip icon="mdi-calendar-month">
              {{ toLocalDateString($i18n.locale, modifiedTime) }}
            </q-chip>
          </div>
        </section>
        <section class="article-abstract-section q-mx-md">
          <div class="q-mb-sm">
            <MarkdownSection :input-html="abstract" />
          </div>
        </section>
        <q-separator />
        <q-card-actions>
          <q-btn flat :to="url" :disable="noContentNoClick">
            {{ moreButtonText }}
          </q-btn>
        </q-card-actions>
      </q-card>
    </q-intersection>
  </div>
</template>

<script>
  import { toLocalDateString } from '@/services/helpers';
  import { emptyTutorialContentTag } from '@/services/params';
  import MarkdownSection from '@/components/framework/MarkdownSection';

  export default {
    components: { MarkdownSection },
    props: [
      'title',
      'authors',
      'categories',
      'modifiedTime',
      'abstract',
      'url',
      'isTransPublished',
      'isAnchorPublished',
      'moreButtonText',
      'notClickableWhenNoContent',
    ],
    methods: {
      toLocalDateString,
    },
    computed: {
      noContentNoClick() {
        return (
          this.title === emptyTutorialContentTag &&
          this.notClickableWhenNoContent
        );
      },
    },
  };
</script>

<style lang="sass">
  .article-card-wrapper
    padding: 10px 20px 7px
    h5
      margin: 10px 0
    .article-abstract-section
      margin-top: 15px

  .article-abstract-section .markdown-body a
    color: #b12 !important
    text-decoration: none !important
</style>
