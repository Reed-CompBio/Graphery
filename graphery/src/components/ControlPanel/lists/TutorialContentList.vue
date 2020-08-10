<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Tutorial Content
    </template>
    <template>
      <q-table
        :data="tableContent"
        :columns="columns"
        :pagination="pagination"
        :loading="loadingContent"
        no-data-label="No tutorial content is found."
        row-key="id"
        separator="cell"
        class="custom-table"
      >
        <template v-slot:top>
          <RefreshButton :fetch-func="fetchTutorialContent" class="q-mr-sm" />
          <LangSelector
            :current-lang="tableLang"
            :change-callback="changeTableLang"
            :show-header="true"
          />
        </template>
        <template v-slot:header="props">
          <AllTableHeader :passed-props="props" />
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <!-- title -->
            <q-td key="title" :props="props">
              <OpenInEditorButton
                :label="props.row.title"
                :routePath="{
                  name: 'Tutorial Content Editor',
                  params: {
                    anchorId: props.row.tutorialId,
                    contentId: props.row.id,
                  },
                  query: {
                    lang: tableLang,
                    tutorialUrl: props.row.tutorialUrl,
                  },
                }"
              />
              <!-- TODO when the title is None, create a new content -->
            </q-td>

            <q-td key="isPublished" :props="props">
              {{ props.row.isPublished ? '✅' : '❌' }}
            </q-td>

            <!-- tutorial -->
            <q-td key="tutorialName" :props="props">
              {{ props.row.tutorialName }}
            </q-td>

            <q-td key="tutorialUrl" :props="props">
              <OpenInPageButton
                :label="props.row.tutorialUrl"
                :disabled="emptyContent(props.row.title)"
                :routePath="{
                  name: 'Tutorial',
                  params: { url: props.row.tutorialUrl },
                }"
              />
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

            <DeleteTableCell
              :message="
                `Do you want to delete tutorial translation '${props.row.title}' which belongs to tutorial '${props.row.tutorialName}' and has id '${props.row.id}'?`
              "
              :id="props.row.id"
              :content-type="currentDeletionContentType"
            />
          </q-tr>
        </template>
      </q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { apiCaller } from '@/services/apis';
  import { tutorialContentListQuery } from '@/services/queries';
  import { errorDialog, resolveAndOpenLink } from '@/services/helpers';
  import { emptyTutorialContentTag, newModelUUID } from '@/services/params';
  import loadingMixin from '../mixins/LoadingMixin.vue';
  import tableLangMixin from '../mixins/TableLangMixin.vue';
  import AllTableHeader from '@/components/ControlPanel/parts/table/AllTableHeader';

  export default {
    mixins: [loadingMixin, tableLangMixin],
    components: {
      DeleteTableCell: () =>
        import('@/components/ControlPanel/parts/table/DeleteTableCell'),
      AllTableHeader,
      LangSelector: () => import('../parts/selectors/LangSelector.vue'),
      OpenInPageButton: () => import('../parts/buttons/OpenInPageButton.vue'),
      OpenInEditorButton: () =>
        import('../parts/buttons/OpenInEditorButton.vue'),
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      RefreshButton: () => import('../parts/buttons/RefreshButton.vue'),
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
            name: 'tutorialName',
            label: 'Tutorial Name',
            field: 'tutorialName',
            align: 'center',
          },
          {
            name: 'tutorialUrl',
            label: 'Tutorial URL',
            field: 'tutorialUrl',
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
            required: true,
          },
        ],
        tableContent: [],
        pagination: {
          sortBy: 'title',
          rowsPerPage: 10,
        },
        tutorialContentTypeMapping: {
          'en-us': 'ENUS_TUTORIAL_CONTENT',
          'zh-cn': 'ZHCN_TUTORIAL_CONTENT',
        },
      };
    },
    computed: {
      requestVariable() {
        return {
          translation: this.tableLang,
        };
      },
      currentDeletionContentType() {
        const contentType = this.tutorialContentTypeMapping[this.tableLang];
        if (contentType) {
          return contentType;
        } else {
          errorDialog({
            message: 'Internal Error: Unknown deletion content type specified.',
          });
          return undefined;
        }
      },
    },
    methods: {
      fetchTutorialContent() {
        this.startLoading();
        apiCaller(tutorialContentListQuery, this.requestVariable)
          .then((data) => {
            if (!data || !('allTutorialInfo' in data)) {
              throw Error('Invalid data returned.');
            }

            this.tableContent = data['allTutorialInfo'].map((obj) => {
              obj.content.authors = obj.content.authors.map(
                (obj) => obj.username
              );
              obj.content.tutorialId = obj.id;
              obj.content.tutorialName = obj.name;
              obj.content.tutorialUrl = obj.url;
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
      createTutorialContent() {
        resolveAndOpenLink({
          name: 'Tutorial Content Editor',
          params: {
            id: newModelUUID,
          },
        });
      },
      emptyContent(title) {
        return title === emptyTutorialContentTag;
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
