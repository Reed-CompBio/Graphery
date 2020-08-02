<template>
  <q-card>
    <q-card-section>
      <UserInfoItem
        v-for="[label, code] in invitationCodes"
        :title="label"
        :content="code"
        :key="label"
      />
    </q-card-section>
    <q-separator />
    <q-card-actions align="center">
      <q-btn flat @click="refreshInvitationCode" label="Refresh Code" />
    </q-card-actions>
  </q-card>
</template>

<script>
  import { apiCaller } from '@/services/apis';
  import {
    invitationKeyQuery,
    refreshInvitationMutation,
  } from '@/services/queries';

  export default {
    components: {
      UserInfoItem: () => import('@/components/user/UserInfoItem'),
    },
    data() {
      return {
        invitationCodes: { a: 'b', c: 'd' },
      };
    },
    methods: {
      fetchValue() {
        apiCaller(invitationKeyQuery).then((data) => {
          this.invitationCodes = Object.entries(
            JSON.parse(data.invitationCodes)
          );
        });
      },
      refreshInvitationCode() {
        apiCaller(refreshInvitationMutation).then((data) => {
          this.invitationCodes = Object.entries(
            JSON.parse(data.refreshInvitationCode.invitationCodes)
          );
        });
      },
    },
    mounted() {
      this.fetchValue();
    },
  };
</script>
