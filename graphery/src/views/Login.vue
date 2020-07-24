<template>
  <div style="display: flex; margin: auto;" class="flex-center">
    <q-card :style="responsiveStyle">
      <q-card-section>
        <div :class="$q.screen.gt.xs ? 'q-pl-xl' : 'q-pl.md'">
          <h3 class="material-page-shorter-h3">
            {{ $t('nav.Login') }}
          </h3>
        </div>
        <div>
          <div id="login-form" class="row">
            <div
              id="login-module-wrapper"
              :class="[
                $q.screen.gt.md ? 'col-8' : 'full-width',
                $q.screen.gt.xs ? 'q-px-xl' : 'q-px.md',
                'flex-center',
              ]"
            >
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
                        flat
                        :label="$t('account.Login')"
                        type="submit"
                        :loading="loading"
                        :disable="loading"
                      ></q-btn>
                    </div>
                    <div class="q-ma-sm">
                      <q-btn
                        flat
                        :label="$t('account.Register')"
                        @click.prevent="register"
                      ></q-btn>
                    </div>
                  </div>
                </q-form>
              </div>
            </div>

            <div
              id="info-wrapper"
              v-if="$q.screen.gt.md"
              class="col q-ml-md q-pr-xl q-my-md"
            >
              <div style="display: flex;" class="flex-center">
                <q-img :src="logoSrc" style="width: 90%"></q-img>
              </div>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
  import { apiCaller } from '../services/apis';
  import { loginMutation } from '../services/queries';
  import { mapActions, mapState } from 'vuex';
  import { errorDialog, successDialog } from '../services/helpers';

  export default {
    components: {},
    data() {
      return {
        account: '',
        password: '',
        showPwd: false,
        loading: false,
        logoSrc: require('@/assets/images/compbio-lab.png'),
      };
    },
    computed: {
      ...mapState({
        userObj: (state) => state.user,
      }),
      responsiveStyle() {
        return {
          'max-width': '900px',
          width: this.$q.screen.gt.xs
            ? this.$q.screen.gt.md
              ? '50vw'
              : '70vw'
            : '90vw',
        };
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
              throw Error(errors);
            }

            if (data.login.success) {
              // TODO change this
              this.setUser(data['login']['user']);
              successDialog({ message: 'Successfully Logged In!' });
              this.$store.commit('SET_CSRF_TOKEN', null);
              this.resetForm();
            } else {
              throw Error(
                'Login Failed. Please check your username and password.'
              );
            }
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
      register() {
        errorDialog({
          message: this.$t('account.noNewAccount'),
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
