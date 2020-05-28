<template>
  <MaterialPage>
    <div>
      <div id="title-section">
        <h3 class="shorter-h">
          {{ title }}
        </h3>
      </div>
      <div id="search-section">
        <q-input
          outlined
          clearable
          :debounce="500"
          hint="press enter to search"
          v-model="searchText"
          name="search-input"
          :rules="[]"
          :loading="searchLoading"
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
            row: $q.screen.gt.sm || $q.screen.sm,
            column: $q.screen.lt.sm,
          }"
        >
          <div
            id="filter-section"
            :class="{
              'col-4': true,
              'flex-center': $q.screen.lt.sm,
              row: $q.screen.lt.sm,
            }"
          >
            <div class="q-mr-lg">
              <h5>
                Filter
              </h5>
            </div>
            <div style="flex: 1 1 auto">
              <q-select
                filled
                v-model="filterSelections"
                multiple
                :options="filterOptions"
                use-chips
                stack-label
                label="Categories"
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

          <div id="content-list" class="col-8">
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
              >
              </q-pagination>
            </div>
            <div class="q-px-md">
              <div
                class="relative-position"
                id="inner-loader"
                v-show="!infos.length"
              >
                <q-inner-loading :showing="!infos.length">
                  <q-spinner-pie size="64"></q-spinner-pie>
                </q-inner-loading>
              </div>
              <ArticleCard
                v-for="info in displayedInfos"
                :key="info.id"
                :title="info.title"
                :authors="info.authors"
                :categories="info.categories"
                :time="info.time"
                :abstract="info.abstract"
                :id="info.id"
                @category-filter="addToCategoryFilter"
                @author-filter="addToAuthorFilter"
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
  export default {
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      ArticleCard: () => import('@/components/framework/ArticleCard.vue'),
    },
    props: {
      api: String,
      title: String,
    },
    data() {
      return {
        searchText: '',
        searchLoading: false,
        filterSelections: [],
        filterOptions: [],
        // TODO page separation
        // TODO link it with api calls
        rawInfos: [],
        infos: [], // Served as a filtered input
        // TODO add this to the settings
        pageDisplayNum: 5,
        current: 1,
        currentPage: 1,
      };
    },
    computed: {
      paginationMax() {
        return Math.ceil(this.infos.length / this.pageDisplayNum);
      },
      displayIndexStart() {
        return (this.currentPage - 1) * this.pageDisplayNum;
      },
      displayedInfos() {
        return this.infos.slice(
          this.displayIndexStart,
          this.displayIndexStart + 5
        );
      },
    },
    methods: {
      toggleLoading() {
        this.searchLoading = true;
      },
      finishLoading() {
        this.searchLoading = false;
      },
      getInfoList() {
        console.debug('api call path: ', this.api);
        // TODO API calls to get tutorial lists
        console.debug('start getting tutorial infos');
        this.toggleLoading();
        setTimeout(() => {
          for (let i = 0; i < 10; i++) {
            this.infos.push({
              title: 'Example',
              authors: ['me', 'her'],
              categories: ['1', '2'],
              time: new Date().toLocaleString(),
              abstract:
                'This is an example article card. And this part is an abstract section that contains the basic info of this example tutorial.',
              id: i.toString(),
            });
          }
          // TODO modify this to accommodate the real apis
          this.finishLoading();
          console.debug('finished loading tutorial infos');
        }, 1000);
      },
      search() {
        if (this.searchLoading) {
          console.log('Is searching, cancel current searching');
          // TODO notify
        }
        console.log('search');
        // this.toggleLoading();
      },
      addToAuthorFilter(author) {
        // TODO apply author filter
        console.debug(`add ${author} to author filter`);
      },
      addToCategoryFilter(category) {
        // TODO apply category filters
        console.debug(`add ${category} to category filter`);
      },
      useTimeFilter(option) {
        console.debug(`using time filter with option ${option}.`);
      },
    },
    mounted() {
      this.getInfoList();
    },
    // TODO maybe add a watch which emits an event once the info list is updated
  };
</script>

<style lang="sass">
  .shorter-h
    margin-bottom: 20px
  #inner-loader
    min-height: 100px
</style>
