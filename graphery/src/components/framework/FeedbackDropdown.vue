<template>
  <q-btn-dropdown size="lg" :label="$t('nav.Feedback')">
    <q-list>
      <q-item tag="a" :href="issueLink" target="_blank">
        <q-item-section>
          <q-item-label class="feedback-item">
            GitHub Issues
          </q-item-label>
        </q-item-section>
      </q-item>
      <q-item tag="a" :href="mailToLink" target="_blank">
        <q-item-section>
          <q-item-label class="feedback-item">
            {{ $t('nav.EmailMe') }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
  export default {
    data() {
      return {
        issueLink: 'https://github.com/FlickerSoul/Graphery/issues',
        mailToLink:
          'mailto:graphery@groups.reed.edu?subject=Graphery%20Feedback&body=Please%20describe%20in%20detail%3A%0D%0A1.%20if%20something%20looks%20wrong%2C%20please%20tell%20us%20what%20it%20should%20be%20like%20and%20how%20we%20can%20reproduce%20the%20problem%0D%0A2.%20if%20something%20can%20be%20better%2C%20please%20tell%20us%20how%20we%20can%20improve%20and%20the%20reasons%0D%0A%0D%0AThank%20you%20so%20much!',
      };
    },
  };
</script>
