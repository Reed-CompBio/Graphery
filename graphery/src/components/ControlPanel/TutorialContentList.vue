<template>
  <ControlPanelContentFrame>
    <template v-slot:title>
      Tutorial Contents
    </template>
    <template>
      <q-table> </q-table>
    </template>
  </ControlPanelContentFrame>
</template>

<script>
  export default {
    components: {
      ControlPanelContentFrame: () => import('./ControlPanelContentFrame'),
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
            name: 'authors',
            label: 'Authors',
            field: 'authors',
          },
        ],
      };
    },
  };
</script>
