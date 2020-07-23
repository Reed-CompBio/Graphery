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
        :loading="loadingTutorialContent"
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
            </q-td>

            <!-- tutorial -->
            <q-td key="tutorial" :props="props">
              {{ props.row['tutorial_anchor'] }}
            </q-td>

            <!-- abstract -->
            <q-td key="abstract" :props="props">
              {{ props.row.abstract }}
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
            <q-td key="content_md" :props="props">
              <q-input
                v-model="props.row['content_md']"
                type="textarea"
                readonly
              />
            </q-td>

            <!-- HTML content -->
            <q-td key="content_html" :props="props">
              <q-input
                v-model="props.row['content_html']"
                type="textarea"
                readonly
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    components: {
      OpenInEditorButton: () => import('./OpenInEditorButton'),
      ControlPanelContentFrame: () => import('./ControlPanelContentFrame'),
      RefreshButton: () => import('./RefreshButton'),
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
            name: 'tutorial',
            label: 'Tutorial',
            field: 'tutorial_anchor',
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
          },
          {
            name: 'content_md',
            label: 'Markdown Content',
            field: 'content_md',
          },
          {
            name: 'content_html',
            label: 'HTML Content',
            field: 'content_html',
          },
          {
            name: 'id',
            label: 'ID',
            field: 'id',
          },
        ],
        tableContent: [],
        pagination: {
          sortBy: 'title',
          rowsPerPage: 10,
        },
        loadingTutorialContent: false,
        tableLang: this.$i18n.locale,
      };
    },
    methods: {
      fetchTutorialContent() {
        console.log('fetch');
      },
      changeTableLang(lang) {
        this.tableLang = lang;
      },
    },
  };
</script>
