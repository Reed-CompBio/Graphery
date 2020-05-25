<template>
  <div>
    <q-dialog v-model="show" persistent seamless position="bottom">
      <q-card style="width: 600px">
        <q-linear-progress :value="0.6" color="pink" />

        <q-card-section class="row items-center no-wrap">
          <div>
            <div class="text-weight-bold">The Walker</div>
            <div class="text-grey">Fitz & The Tantrums</div>
          </div>

          <q-space />

          <q-btn flat round icon="mdi-play" />
          <q-btn flat round icon="mdi-pause" />
          <q-btn flat round icon="mdi-window-close" v-close-popup />
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
  export default {
    props: ['show'],
  };
</script>
