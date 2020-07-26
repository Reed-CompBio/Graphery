<template>
  <ControlPanelContentFrame ref="contentFrame">
    <template v-slot:title>
      Category Editor
    </template>
    <template>
      <div style="display: flex; flex-direction: column;" class="flex-center">
        <InfoCard class="half-width-card q-mb-md">
          <template v-slot:title>
            ID
          </template>
          <div class="text-center">
            {{ displayedId }}
          </div>
        </InfoCard>
        <InfoCard class="half-width-card">
          <template v-slot:title>
            Category
          </template>
          <q-input
            outlined
            v-model="category"
            hint="Please input the name of this category."
          />
        </InfoCard>
        <InfoCard class="half-width-card">
          <template v-slot:title>
            Published?
          </template>
          <q-checkbox
            v-model="categoryPublished"
            :label="categoryPublished ? '✅' : '❌'"
          />
        </InfoCard>

        <q-btn class="half-width-card" label="Submit" />
      </div>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  import { newModelUUID } from '../../../services/params';
  import { apiCaller } from '../../../services/apis';
  import { categoryMutation } from '../../../services/queries';

  export default {
    props: {
      id: {
        default: newModelUUID,
      },
    },
    components: {
      ControlPanelContentFrame: () =>
        import('../frames/ControlPanelContentFrame.vue'),
      InfoCard: () => import('../parts/InfoCard.vue'),
    },
    data() {
      return {
        category: '',
        categoryPublished: false,
      };
    },
    computed: {
      newCategory() {
        return this.id === newModelUUID;
      },
      displayedId() {
        if (this.newCategory) {
          return 'Pending';
        } else {
          return this.id;
        }
      },
    },
    methods: {
      fetchValue() {
        this.$refs.contentFrame.startLoading();

        if (!this.newCategory) {
          apiCaller(categoryMutation, {
            id: this.id,
            category: this.category,
            isPublished: this.categoryPublished,
          })
            .then((data) => {
              if (!data) {
                throw Error(
                  'Invalid data returned. Cannot modify current entry.'
                );
              }
            })
            .then(() => {
              this.$refs.contentFrame.finishedLoading();
            });
        }
      },
    },
    watch: {
      id: function(newVal, oldVal) {
        if (oldVal === newModelUUID) {
          this.$router.push(this.$route.fullPath.replace(newModelUUID, newVal));
        }
      },
    },
  };
</script>
