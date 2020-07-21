<template>
  <MaterialPage>
    <div>
      <h3 class="material-page-shorter-h3">
        {{ $t('nav.Account') }}
      </h3>
    </div>
    <div>
      <div id="login-form" class="row" v-if="showLoginForm">
        <div id="login-module-wrapper" class="col-7 q-pr-md flex-center">
          <div id="login-content">
            <q-form @submit="login" @reset="resetForm">
              <div id="account" class="q-my-md">
                <q-input
                  outlined
                  v-model="account"
                  :label="$t('account.Username')"
                  type="text"
                  :rules="[(val) => !!val || $t('account.notEmpty')]"
                  :lazy-rules="true"
                  :loading="loading"
                  :disable="loading"
                />
              </div>
              <div id="password" class="q-my-md">
                <q-input
                  outlined
                  v-model="password"
                  :label="$t('account.Password')"
                  :type="showPwd ? 'text' : 'password'"
                  :rules="[(val) => !!val || $t('account.notEmpty')]"
                  :lazy-rules="true"
                  :loading="loading"
                  :disable="loading"
                >
                  <template v-slot:append>
                    <q-icon
                      :name="showPwd ? 'visibility' : 'visibility_off'"
                      class="cursor-pointer"
                      @click="showPwd = !showPwd"
                    />
                  </template>
                </q-input>
              </div>
              <div
                id="login-actions"
                style="display: flex; flex-direction: row-reverse; flex-wrap: wrap;"
                class="q-my-md"
              >
                <div class="q-ma-sm">
                  <q-btn
                    :label="$t('account.Login')"
                    type="submit"
                    :loading="loading"
                    :disable="loading"
                  ></q-btn>
                </div>
                <div class="q-ma-sm">
                  <q-btn :label="$t('account.Register')" disable></q-btn>
                </div>
              </div>
            </q-form>
          </div>
        </div>
        <div id="info-wrapper" class="col q-ml-md q-mt-lg">
          <div class="q-pa-sm">
            <q-card>
              <q-card-section>
                <!-- TODO database pull -->
                <p style="margin: 0;">{{ $t('account.noNewAccount') }}</p>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
      <div id="user-info" class="row" v-if="showUserInfo">
        <div id="user-info-wrapper" class="col-12 flex-center q-ma-md">
          <UserInfoCard :userObj="userObj" @logout="logout"></UserInfoCard>
        </div>
      </div>
    </div>
  </MaterialPage>
</template>

<script>
  import { apiCaller } from '../services/apis.ts';
  import {
    loginMutation,
    logoutMutation,
    userInfoQuery,
  } from '../services/queries';
  import { mapState, mapActions } from 'vuex';

  export default {
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
      UserInfoCard: () => import('@/components/user/UserInfoCard.vue'),
    },
    data() {
      return {
        account: '',
        password: '',
        showPwd: false,
        loading: false,
      };
    },
    computed: {
      ...mapState({
        userObj: (state) => state.user,
      }),
      showLoginForm() {
        return this.userObj === null;
      },
      showUserInfo() {
        return !this.showLoginForm;
      },
    },
    methods: {
      ...mapActions(['setUser']),
      login() {
        const loginCredential = {};
        if (this.account && this.password) {
          loginCredential['username'] = this.account;
          loginCredential['password'] = this.password;
        }

        this.loading = true;
        apiCaller(loginMutation, loginCredential)
          .then(([data, errors]) => {
            if (errors) {
              // TODO handle error
              console.error(errors);
            }

            if (data) {
              // TODO change this
              this.setUser(data['login']['user']);
              this.loading = false;
              this.resetForm();
            }

            this.$store.commit('SET_CSRF_TOKEN', null);
          })
          .catch((err) => {
            // TODO handle error
            console.error(err);
          });
      },
      logout() {
        apiCaller(logoutMutation)
          .then(([data, errors]) => {
            if (errors) {
              // TODO add error handling
              console.error(errors);
            }

            if (data && data['logout']['success']) {
              this.setUser(null);
            } else {
              throw Error('Cannot logout at this time');
            }
          })
          .catch((err) => {
            // TODO handle error
            console.log(err);
          });
      },
      resetForm() {
        this.account = '';
        this.password = '';
        this.showPwd = false;
        this.loading = false;
      },
    },
  };
</script>
