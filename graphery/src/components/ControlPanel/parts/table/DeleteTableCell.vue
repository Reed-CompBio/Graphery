<template>
  <q-td auto-width class="text-center">
    <q-btn
      size="sm"
      color="negative"
      round
      dense
      @click="showDeleteDialog"
      icon="delete"
    />
  </q-td>
</template>

<script>
  import deleteMixin from '../../mixins/DeleteMixin.vue';
  export default {
    mixins: [deleteMixin],
  };
</script>
