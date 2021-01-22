<template>
  <div class="q-my-lg">
    <q-intersection once transition="scale" class="expandable-helper">
      <q-card class="article-card-wrapper">
        <section>
          <div class="tutorial-title-wrapper text-h5">
            <div v-if="info.rank" class="tutorial-rank">
              {{ rankText }}
            </div>
            <div class="text-h5">
              <router-link
                class="tutorial-title"
                :to="info.url"
                style="color: #000"
              >
                {{ info.title }}
              </router-link>
            </div>
          </div>
        </section>
        <section>
          <div>
            <q-chip
              clickable
              v-if="!info.isAnchorPublished"
              icon="mdi-book-lock"
            >
              Anchor Not Published
            </q-chip>
            <q-chip
              clickable
              v-if="!info.isTransPublished"
              icon="mdi-book-lock"
            >
              Translation Not Published
            </q-chip>
          </div>
          <div>
            <q-chip v-if="noContent" icon="link">
              {{ info.url }}
            </q-chip>
            <q-chip
              v-for="author in info.authors"
              :key="author.username"
              icon="mdi-card-account-details"
              @click="$emit('author-filter', author)"
            >
              {{ author.firstName }} {{ author.lastName }}
            </q-chip>
            <q-chip
              clickable
              v-for="category in info.categories"
              :key="category.id"
              icon="category"
              @click="$emit('category-filter', category.id)"
            >
              {{ category.category }}
            </q-chip>
            <q-chip icon="mdi-calendar-month">
              {{ toLocalDateString($i18n.locale, info.modifiedTime) }}
            </q-chip>
          </div>
        </section>
        <section class="article-abstract-section q-mx-md">
          <div class="q-mb-sm">
            <MarkdownSection :input-html="info.abstract" :doc-id="info.url" />
          </div>
        </section>
        <q-separator />
        <q-card-actions>
          <q-btn
            outline
            color="primary"
            rounded
            class="q-mt-sm"
            type="a"
            target="__blank"
            :href="info.url"
            :disable="noContentNoClick"
          >
            {{ moreButtonText }}
          </q-btn>
        </q-card-actions>
      </q-card>
    </q-intersection>
  </div>
</template>

<script>
  import { rankToText, toLocalDateString } from '@/services/helpers';
  import { emptyTutorialContentTag } from '@/services/params';
  import MarkdownSection from '@/components/framework/md/MarkdownSection';

  export default {
    components: { MarkdownSection },
    props: ['info', 'moreButtonText', 'notClickableWhenNoContent'],
    methods: {
      toLocalDateString,
    },
    computed: {
      noContent() {
        return this.info.title === emptyTutorialContentTag;
      },
      noContentNoClick() {
        return this.noContent && this.notClickableWhenNoContent;
      },
      rankText() {
        return rankToText(this.info.rank);
      },
    },
  };
</script>

<style lang="sass">
  .article-card-wrapper
    padding: 10px 20px 7px
    .text-h5
      margin: 10px 0
      div
        display: inline-block
        margin-right: 7px
    .article-abstract-section
      margin-top: 15px

  .article-abstract-section .markdown-body a
    color: #b12 !important
    text-decoration: none !important
  .tutorial-title-wrapper
    .tutorial-rank
      display: inline-block
      margin-bottom: 2px
    & > .text-h5
      display: inline-block
    .tutorial-title
      &:after
        content: ''
        width: 0
        height: 2px
        display: block
        background: black
        transition: 300ms
      &:hover:after
        width: 100%
</style>
