<template>
  <q-tr :props="passedProps">
    <q-th v-for="col in passedProps.cols" :key="col.name" :props="passedProps">
      {{ col.label }}
    </q-th>
    <DeleteTableHeader />
  </q-tr>
</template>

<script>
  export default {
    props: ['passedProps'],
    components: {
      DeleteTableHeader: () => import('./DeleteTableHeader.vue'),
    },
  };
</script>
