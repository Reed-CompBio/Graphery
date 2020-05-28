<template>
  <MaterialPage>
    <div>
      <div id="title-section">
        <h3 style="margin-bottom: 20px">
          Tutorials
        </h3>
      </div>
      <!-- TODO make the components responsive -->
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
          <template v-slot:append>
            <q-icon
              v-if="!searchText && !searchLoading"
              name="mdi-magnify"
              @click="search"
              style="cursor: pointer;"
            />
          </template>
        </q-input>
      </div>
      <div id="content-section">
        <div class="row">
          <div id="filter-section" class="col-4">
            <div>
              <h5>
                Filter
              </h5>
            </div>
            <div>
              <q-select
                filled
                v-model="filterSelections"
                multiple
                :options="filterOptions"
                use-chips
                stack-label
                label="Multiple selection"
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

          <div id="tutorial-list" class="col-8">
            <div class="q-px-md">
              <ArticleCard
                v-for="info in tutorialInfos"
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
              <q-inner-loading :showing="!tutorialInfos.length">
                <q-spinner-pie size="64"></q-spinner-pie>
              </q-inner-loading>
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
    data() {
      return {
        searchText: '',
        searchLoading: false,
        filterSelections: [],
        filterOptions: [],
        // TODO page separation
        // TODO link it with api calls
        tutorialInfos: [],
      };
    },
    methods: {
      toggleLoading() {
        this.searchLoading = true;
      },
      finishLoading() {
        this.searchLoading = false;
      },
      getTutorialInfoList() {
        // TODO API calls to get tutorial lists
        console.debug('start getting tutorial infos');
        this.toggleLoading();
        setTimeout(() => {
          this.tutorialInfos.push(
            ...[
              {
                title: 'Example',
                authors: ['me', 'her'],
                categories: ['1', '2'],
                time: new Date().toLocaleString(),
                abstract:
                  'This is an example article card. And this part is an abstract section that contains the basic info of this example tutorial.',
                id: '1',
              },
              {
                title: 'Example',
                authors: ['me', 'her'],
                categories: ['1', '2'],
                time: new Date().toLocaleString(),
                abstract:
                  'This is an example article card. And this part is an abstract section that contains the basic info of this example tutorial.',
                id: '2',
              },
              {
                title: 'Example',
                authors: ['me', 'her'],
                categories: ['1', '2'],
                time: new Date().toLocaleString(),
                abstract:
                  'This is an example article card. And this part is an abstract section that contains the basic info of this example tutorial.',
                id: '3',
              },
              {
                title: 'Example',
                authors: ['me', 'her'],
                categories: ['1', '2'],
                time: new Date().toLocaleString(),
                abstract:
                  'This is an example article card. And this part is an abstract section that contains the basic info of this example tutorial.',
                id: '4',
              },
              {
                title: 'Example',
                authors: ['me', 'her'],
                categories: ['1', '2'],
                time: new Date().toLocaleString(),
                abstract:
                  'This is an example article card. And this part is an abstract section that contains the basic info of this example tutorial.',
                id: '5',
              },
            ]
          );
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
    },
    mounted() {
      this.getTutorialInfoList();
    },
  };
</script>
