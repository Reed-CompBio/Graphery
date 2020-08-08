<template>
  <q-dialog persistent seamless square>
    <q-card>
      <div class="q-ma-sm">
        <div class="row">
          <div class="row-xs col-md-8">
            <q-img :src="resourceLink" />
          </div>
          <div class="row-xs col-md-4">
            <div class="row" id="upload-info-box">
              <q-input
                disable
                readonly
                label="URL"
                outlined
                v-model="fullLink"
              />
            </div>
            <div class="row" id="upload-action-box">
              <UploadActionButton title="Copy Relative URL" />
              <UploadActionButton title="Copy Absolute URL" />
              <UploadActionButton title="Delete PERMANENTLY" color="negative" />
            </div>
          </div>
        </div>
      </div>
    </q-card>
  </q-dialog>
</template>

<script>
  import { BASE_URL } from '@/services/api_entry';
  import UploadActionButton from '@/components/ControlPanel/parts/buttons/UploadActionButton';

  export default {
    components: { UploadActionButton },
    props: {
      resourceLink: {
        type: String,
      },
    },
    computed: {
      fullLink() {
        return BASE_URL + this.resourceLink;
      },
    },
  };
</script>
