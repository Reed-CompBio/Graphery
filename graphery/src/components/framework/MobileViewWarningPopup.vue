<template>
  <q-dialog v-model="show" persistent>
    <q-card>
      <q-card-section class="row items-center">
        <div>
          <q-avatar icon="announcement" color="negative" />
        </div>
        <div class="q-ma-sm q-mt-md">
          <p>{{ $t('dialog.mobileWarning') }}</p>
          <p v-if="extraInfo">{{ extraInfo }}</p>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat :label="$t('dialog.ok')" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
  export default {
    props: ['extraInfo'],
    data() {
      return {
        show: true,
      };
    },
  };
</script>
