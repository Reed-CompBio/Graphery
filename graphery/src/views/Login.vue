<template>
  <MaterialPage>
    <div>
      <h3 class="material-page-shorter-h3">
        {{ $t('nav.Login') }}
      </h3>
    </div>
    <div>
      <div id="login-form" class="row">
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
                <!-- TODO pull messages from database  -->
                <p style="margin: 0;">{{ $t('account.noNewAccount') }}</p>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </MaterialPage>
</template>

<script>
  import { apiCaller } from '../services/apis';
  import { loginMutation } from '../services/queries';
  import { mapActions, mapState } from 'vuex';
  import { errorDialog, successDialog } from '../services/helpers';

  export default {
    components: {
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
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
              throw Error(errors);
            }

            if (data) {
              // TODO change this
              this.setUser(data['login']['user']);
              successDialog({ message: 'Successfully Logged In!' });
              this.resetForm();
            }

            this.$store.commit('SET_CSRF_TOKEN', null);
          })
          .catch((err) => {
            errorDialog({
              message: 'An error occurs during logging in. ' + err,
            });
          })
          .finally(() => {
            this.loading = false;
          });
      },
      resetForm() {
        this.account = '';
        this.password = '';
        this.showPwd = false;
        this.loading = false;
      },
    },
    watch: {
      userObj: function() {
        if (this.userObj !== null) {
          this.$router.push('/account');
        }
      },
    },
  };
</script>
