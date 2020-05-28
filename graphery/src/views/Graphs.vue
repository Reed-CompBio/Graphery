<template>
  <MaterialPage>
    <div>
      <div id="title-section">
        <h3 style="margin-bottom: 20px">
          Graphs
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
    },
  };
</script>
