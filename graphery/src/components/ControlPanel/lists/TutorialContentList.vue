<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Tutorial Contents
    </template>
    <template>
      <q-table
        :data="tableContent"
        :columns="columns"
        :pagination="pagination"
        :loading="loadingTable"
        no-data-label="No tutorial content is found."
        row-key="id"
        separator="cell"
        class="custom-table"
      >
        <template v-slot:top>
          <RefreshButton :fetch-func="fetchTutorialContent" class="q-mr-sm" />
          <q-btn-dropdown flat dense icon="mdi-translate" :label="$i18n.locale">
            <q-list>
              <q-item
                v-for="lang in $i18n.availableLocales"
                :key="lang"
                clickable
                v-close-popup
                @click="changeTableLang(lang)"
              >
                <q-item-section thumbnail>
                  <q-icon
                    v-if="$i18n.locale === lang"
                    name="keyboard_arrow_right"
                  />
                </q-item-section>
                <q-item-section>
                  <q-item-label class="lang-label">{{ lang }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <!-- title -->
            <q-td key="title" :props="props">
              <OpenInEditorButton :label="props.row.title" />
              <!-- TODO when the title is None, create a new content -->
            </q-td>

            <q-td key="isPublished" :props="props">
              {{ props.row.isPublished ? '✅' : '❌' }}
            </q-td>

            <!-- tutorial -->
            <q-td key="tutorial" :props="props">
              {{ props.row.name }}
            </q-td>

            <!-- abstract -->
            <q-td key="abstract" :props="props">
              <q-input v-model="props.row.abstract" type="textarea" readonly />
            </q-td>

            <!-- authors -->
            <q-td key="authors" :props="props">
              <q-select
                multiple
                use-chips
                readonly
                :option="props.row.authors"
                v-model="props.row.authors"
              ></q-select>
            </q-td>

            <!-- markdown content -->
            <q-td key="contentMd" :props="props">
              <q-input v-model="props.row.contentMd" type="textarea" readonly />
            </q-td>

            <!-- HTML content -->
            <q-td key="contentHtml" :props="props">
              <q-input
                v-model="props.row.contentHtml"
                type="textarea"
                readonly
              />
            </q-td>

            <q-td key="id" :props="props">
              {{ props.row.id }}
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { apiCaller } from '../../../services/apis';
  import loadingMixin from './LoadingMixin.vue';
  import { tutorialContentListQuery } from '../../../services/queries';
  import { errorDialog } from '../../../services/helpers';

  export default {
    mixins: [loadingMixin],
    components: {
      OpenInEditorButton: () => import('../parts/OpenInEditorButton'),
      ControlPanelContentFrame: () => import('../ControlPanelContentFrame'),
      RefreshButton: () => import('../parts/RefreshButton'),
    },
    data() {
      return {
        columns: [
          {
            name: 'title',
            label: 'Title',
            field: 'title',
            align: 'center',
            sortable: true,
            sort: (a, b) => {
              if (a === b) {
                return 0;
              }
              return a < b ? -1 : 1;
            },
          },
          {
            name: 'isPublished',
            label: 'Published?',
            field: 'isPublished',
            align: 'center',
          },
          {
            name: 'tutorial',
            label: 'Tutorial',
            field: 'name',
            align: 'center',
          },
          {
            name: 'abstract',
            label: 'Abstract',
            field: 'abstract',
            align: 'center',
          },
          {
            name: 'authors',
            label: 'Authors',
            field: 'authors',
            align: 'center',
          },
          {
            name: 'contentMd',
            label: 'Markdown Content',
            field: 'contentMd',
            align: 'center',
          },
          {
            name: 'contentHtml',
            label: 'HTML Content',
            field: 'contentHtml',
            align: 'center',
          },
          {
            name: 'id',
            label: 'ID',
            field: 'id',
            align: 'center',
          },
        ],
        tableContent: [],
        pagination: {
          sortBy: 'title',
          rowsPerPage: 10,
        },
        tableLang: this.$i18n.locale,
      };
    },
    computed: {
      requestVariable() {
        return {
          translation: this.$i18n.locale,
        };
      },
    },
    methods: {
      fetchTutorialContent() {
        this.startLoading();
        apiCaller(tutorialContentListQuery, this.requestVariable)
          .then(([data, errors]) => {
            if (errors) {
              throw Error(errors);
            }

            if (!data || !('allTutorialInfo' in data)) {
              throw Error('Invalid data returned');
            }

            this.tableContent = data['allTutorialInfo'].map((obj) => {
              obj.content.name = obj.name;
              return obj.content;
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurs during fetching tutorial contents of ${this.$i18n.locale} language. ${err}`,
            });
          })
          .finally(() => {
            this.finishedLoading();
          });
      },
      changeTableLang(lang) {
        this.tableLang = lang;
      },
    },
    mounted() {
      this.fetchTutorialContent();
    },
    watch: {
      requestVariable: function() {
        this.fetchTutorialContent();
      },
    },
  };
</script>
