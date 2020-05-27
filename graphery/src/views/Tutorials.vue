<template>
  <MaterialPage>
    <div>
      <div>
        <h3 style="margin-bottom: 20px">
          Tutorials
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
          :hide-hint="searchText || searchLoading"
        >
          <template v-slot:append>
            <q-icon
              v-if="!searchText && !searchLoading"
              name="mdi-magnify"
              @click="search"
              @keydown.enter="search"
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
              ></ArticleCard>
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
        tutorialInfos: [
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
        ],
      };
    },
    methods: {
      toggleLoading() {
        this.searchLoading = true;
      },
      finishLoading() {
        this.searchLoading = false;
      },
      search() {
        if (this.searchLoading) {
          console.log('Is searching, cancel current searching');
          // TODO notify
        }
        console.log('search');
        // this.toggleLoading();
      },
    },
  };
</script>
