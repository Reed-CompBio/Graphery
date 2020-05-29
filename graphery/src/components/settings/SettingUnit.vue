<template>
  <q-item>
    <q-item-section>
      <span> {{ name }}</span>
    </q-item-section>
    <q-item-section>
      <slot></slot>
    </q-item-section>
  </q-item>
</template>

<script>
  export default {
    props: ['name'],
  };
</script>
