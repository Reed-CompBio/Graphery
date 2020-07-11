<template>
  <MaterialPage>
    <div>
      <h3 class="shorter-h">
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
                  label="Username"
                  type="text"
                  :rules="[account || 'it cannot be empty']"
                  :loading="loading"
                  :disable="loading"
                />
              </div>
              <div id="password" class="q-my-md">
                <q-input
                  outlined
                  v-model="password"
                  label="Password"
                  :type="showPwd ? 'text' : 'password'"
                  :rules="[Boolean(password) || 'it cannot be empty']"
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
                style="display: flex; flex-direction: row-reverse;"
                class="q-my-lg"
              >
                <div class="q-mx-sm">
                  <q-btn
                    label="Login"
                    type="submit"
                    :loading="loading"
                    :disable="loading"
                  ></q-btn>
                </div>
                <div class="q-mx-sm">
                  <q-btn label="Register" disable></q-btn>
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
                <p style="margin: 0;">We don't accept new accounts for now.</p>
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
        loading: true,
        userObj: null,
      };
    },
    computed: {
      showLoginForm() {
        return this.userObj === null;
      },
      showUserInfo() {
        return !this.showLoginForm;
      },
    },
    methods: {
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
              console.error(errors);
            }

            if (data) {
              this.userObj = data['tokenAuth']['user'];
              this.loading = false;
            }
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
              console.error(errors);
            }

            if (data && data['deleteTokenCookie']['deleted']) {
              this.userObj = null;
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
    mounted() {
      apiCaller(userInfoQuery)
        .then(([data, errors]) => {
          if (errors) {
            console.error(errors);
          }

          if (data) {
            this.userObj = data['userInfo'];
          }

          this.loading = false;
        })
        .catch((err) => {
          // TODO handle error
          console.error(err);
        });
    },
  };
</script>
