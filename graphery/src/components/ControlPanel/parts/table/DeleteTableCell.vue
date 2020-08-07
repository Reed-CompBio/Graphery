<template>
  <q-td auto-width class="text-center">
    <q-btn
      size="sm"
      color="negative"
      round
      dense
      @click="deleteContent"
      icon="delete"
    />
  </q-td>
</template>

<script>
  export default {
    props: { deleteContent: { default: () => () => null } },
  };
</script>
