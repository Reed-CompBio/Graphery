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
          :debounce="500"
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
            id="filter-section"
            :class="[
              'col-4',
              'flex-center',
              'q-px-xs',
              $q.screen.lt.sm ? 'row' : '',
            ]"
          >
            <div class="q-mr-lg">
              <h5>
                {{ $t('collectionPage.Filter') }}
              </h5>
            </div>
            <div style="flex: 1 1 auto">
              <q-select
                filled
                v-model="categoryFilterSelections"
                multiple
                :options="categoryFilterOptions"
                use-chips
                stack-label
                :label="$t('collectionPage.Categories')"
                dropdown-icon="mdi-menu-down"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      No Items
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
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
              <div id="empty-indicator" v-show="infos.length === 0">
                <EmptyEntryCard />
              </div>
              <ArticleCard
                v-for="info in displayedInfos"
                :key="info.url"
                :url="info.url"
                :categories="info.categories"
                :isAnchorPublished="info.isAnchorPublished"
                :title="info.title"
                :authors="info.authors"
                :modifiedTime="info.modifiedTime"
                :abstract="info.abstract"
                :isTransPublished="info.isTransPublished"
                @category-filter="addToCategoryFilter"
                @author-filter="addToAuthorFilter"
                :moreButtonText="moreButtonText"
                :notClickableWhenNoContent="notClickableWhenNoContent"
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
        categoryFilterSelections: [],
        categoryFilterOptions: [],
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
    },
    methods: {
      loadInfo() {
        this.startLoading();

        apiCaller(this.query, this.variables)
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
        if (this.loadingContent) {
          console.log('Is searching, cancel current searching');
          // TODO notify and cancel axios's request
        }
        console.log('search');
        // this.toggleLoading();
      },
      addToAuthorFilter(author) {
        // TODO apply author filter I don't need this
        console.debug(`add ${author} to author filter`);
      },
      addToCategoryFilter(category) {
        // TODO apply category filters
        console.debug(`add ${category} to category filter`);
      },
    },
    mounted() {
      this.loadInfo();
    },
    watch: {
      '$i18n.locale': function() {
        this.loadInfo();
      },
    },
  };
</script>

<style lang="sass">
  #inner-loader
    min-height: 100px
</style>
