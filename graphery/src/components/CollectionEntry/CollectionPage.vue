<template>
  <MaterialPage>
    <div>
      <div id="title-section">
        <h3 class="material-page-shorter-h3">
          {{ title }}
        </h3>
      </div>
      <div id="search-section">
        <q-input
          outlined
          clearable
          :debounce="50"
          :hint="$t('collectionPage.searchHint')"
          v-model="searchText"
          name="search-input"
          :rules="[]"
          :loading="loadingContent"
          @keydown.enter="search"
        >
          <template v-slot:prepend>
            <q-icon
              name="mdi-magnify"
              @click="search"
              style="cursor: pointer;"
            />
          </template>
        </q-input>
      </div>
      <div id="content-section">
        <div
          :class="{
            row: $q.screen.gt.xs,
            column: $q.screen.lt.sm,
          }"
        >
          <div
            id="left-side-section"
            :class="[
              'col-4',
              'flex-center',
              'q-px-xs',
              'q-my-md',
              $q.screen.lt.sm ? 'row' : '',
            ]"
          >
            <div id="filter-section" class=" full-width">
              <div class="q-mr-lg">
                <h5 style="margin-bottom: 16px;">
                  {{ $t('collectionPage.Filter') }}
                </h5>
              </div>
              <div style="flex: 1 1 auto">
                <CategorySelection v-model="categoryIds" />
              </div>
            </div>
          </div>

          <div
            id="content-list"
            :class="['col-8', $q.screen.lt.sm ? 'full-width' : '']"
          >
            <div id="page-manager" class="flex flex-center">
              <q-pagination
                :max="paginationMax"
                v-model="currentPage"
                :max-pages="6"
                ellipses
                direction-links
                boundary-links
                boundary-numbers
                class="q-mx-auto"
                icon-first="mdi-chevron-double-left"
                icon-last="mdi-chevron-double-right"
                icon-prev="mdi-chevron-left"
                icon-next="mdi-chevron-right"
              >
              </q-pagination>
            </div>
            <div class="q-mx-sm q-mt-lg">
              <div
                class="relative-position"
                id="inner-loader"
                v-show="loadingContent"
              >
                <q-inner-loading :showing="loadingContent">
                  <q-spinner-pie size="64"></q-spinner-pie>
                </q-inner-loading>
              </div>
              <div
                id="empty-indicator"
                v-show="infos.length === 0 && !loadingContent"
              >
                <EmptyEntryCard />
              </div>
              <ArticleCard
                v-for="info in displayedInfos"
                :key="info.url"
                :info="info"
                :moreButtonText="moreButtonText"
                :notClickableWhenNoContent="notClickableWhenNoContent"
                @category-filter="addToCategoryFilter"
              ></ArticleCard>
              <!-- TODO why do you want to filter authors? -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </MaterialPage>
</template>

<script>
  import { mapState } from 'vuex';
  import { apiCaller } from '@/services/apis';
  import { errorDialog } from '@/services/helpers';
  import loadingMixin from '@/components/ControlPanel/mixins/LoadingMixin';

  export default {
    mixins: [loadingMixin],
    components: {
      CategorySelection: () =>
        import('@/components/ControlPanel/parts/selectors/CategorySelection'),
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      ArticleCard: () => import('@/components/CollectionEntry/ArticleCard.vue'),
      EmptyEntryCard: () =>
        import('@/components/CollectionEntry/EmptyEntryCard.vue'),
    },
    props: [
      'title',
      'query',
      'variables',
      'mappingFunction',
      'moreButtonText',
      'notClickableWhenNoContent',
    ],
    data() {
      return {
        searchText: '',
        categoryIds: [],
        infos: [], // Served as a filtered input
        current: 1,
        currentPage: 1,
      };
    },
    computed: {
      ...mapState('settings', ['pageDisplayNum']),
      paginationMax() {
        return Math.ceil(this.infos.length / this.pageDisplayNum);
      },
      displayIndexStart() {
        return (this.currentPage - 1) * this.pageDisplayNum;
      },
      displayedInfos() {
        return this.infos.slice(
          this.displayIndexStart,
          this.displayIndexStart + this.pageDisplayNum
        );
      },
      filteredVariables() {
        return {
          ...this.variables,
          filterContent: {
            categoryIds: this.categoryIds,
            searchText: this.searchText,
          },
        };
      },
    },
    methods: {
      loadInfo() {
        this.startLoading();

        apiCaller(this.query, this.filteredVariables)
          .then((data) => {
            if (!data) {
              throw Error('Invalid data returned.');
            }
            this.infos = this.mappingFunction(data);
          })
          .catch((err) => {
            errorDialog({
              message: 'An error occurs in ' + this.title + ' page. ' + err,
            });
            // TODO translate errors
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      search() {
        this.searchText = this.searchText.trim();
        this.loadInfo();
      },
      addToCategoryFilter(categoryId) {
        if (this.categoryIds.indexOf(categoryId) < 0) {
          this.categoryIds.push(categoryId);
        }
      },
    },
    mounted() {
      this.loadInfo();
    },
    watch: {
      '$i18n.locale': function() {
        this.loadInfo();
      },
      categoryIds: function() {
        this.loadInfo();
      },
    },
  };
</script>

<style lang="sass">
  #inner-loader
    min-height: 100px
</style>
