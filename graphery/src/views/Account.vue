<template>
  <MaterialPage>
    <div>
      <h3 class="material-page-shorter-h3">
        {{ $t('nav.Account') }}
      </h3>
    </div>
    <div>
      <div id="user-info" class="row">
        <div id="user-info-wrapper" class="col-12 flex-center q-my-md">
          <UserInfoCards :userObj="userObj" @logout="logout"></UserInfoCards>
        </div>
      </div>
    </div>
  </MaterialPage>
</template>

<script>
  import { apiCaller } from '@/services/apis';
  import { logoutMutation } from '@/services/queries';
  import { mapState, mapActions } from 'vuex';
  import { errorDialog } from '@/services/helpers';

  export default {
    metaInfo() {
      const titleText = this.$t('nav.Account');
      return { title: titleText };
    },
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      UserInfoCards: () => import('@/components/user/UserInfoCards.vue'),
    },
    computed: {
      ...mapState({
        userObj: (state) => state.user,
      }),
    },
    methods: {
      ...mapActions(['setUser']),
      logout() {
        apiCaller(logoutMutation)
          .then((data) => {
            if (!data) {
              throw Error('Failed to talk to server. Failed to logout.');
            }

            if (data['logout']['success']) {
              this.setUser(null);
            } else {
              throw Error('Cannot logout at this time. Reason unknown.');
            }
          })
          .catch((err) => {
            errorDialog({
              message: 'A error occurs during logging out. ' + err,
            });
          });
      },
    },
    watch: {
      userObj: function() {
        if (this.userObj === null) {
          this.$router.push('/login');
        }
      },
    },
  };
</script>
