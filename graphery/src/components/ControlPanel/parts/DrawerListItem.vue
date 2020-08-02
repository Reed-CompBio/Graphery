<template>
  <q-item clickable :to="destination">
    <q-card-section>
      {{ title }}
    </q-card-section>
  </q-item>
</template>

<script>
  export default {
    props: ['destination', 'title'],
  };
</script>
