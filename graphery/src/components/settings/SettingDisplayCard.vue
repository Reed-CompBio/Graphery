<template>
  <section class="q-my-lg">
    <q-card class="q-pa-md ">
      <q-card-section>
        <h4 class="q-my-sm">
          {{ title }}
        </h4>
      </q-card-section>
      <q-separator />
      <q-card-section>
        <div>
          <slot name="toggles"></slot>
        </div>
        <div>
          <slot name="sliders"></slot>
        </div>
      </q-card-section>
    </q-card>
  </section>
</template>

<script>
  export default {
    props: ['title'],
  };
</script>
