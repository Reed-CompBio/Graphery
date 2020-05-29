<template>
  <q-card class="q-pa-md ">
    <q-card-section>
      <h4 class="q-my-sm">
        {{ title }}
      </h4>
    </q-card-section>
    <q-separator />
    <q-card-section>
      <div class="q-pl-md">
        <slot name="toggles"></slot>
      </div>
      <div>
        <slot name="sliders"></slot>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
  export default {
    props: ['title'],
  };
</script>
