<template>
  <div>
    <MaterialCover :cover-title="$t('account.Register')" />
    <div style="display: flex; margin: -8rem auto 8rem;" class="flex-center">
      <q-card :style="responsiveStyle">
        <q-card-section>
          <div :class="$q.screen.gt.xs ? 'q-pl-xl' : 'q-pl.md'">
            <h3 class="material-page-shorter-h3">
              {{ $t('account.Register') }}
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
                  <q-form @submit="register" @reset="resetForm">
                    <div id="email" class="q-mb-md">
                      <q-input
                        outlined
                        v-model="email"
                        :label="$t('account.Email')"
                        type="email"
                        :rules="[(val) => !!val || $t('account.notEmpty')]"
                        :lazy-rules="true"
                        :loading="loading"
                        :disable="loading"
                      />
                    </div>
                    <div id="username" class="q-my-md">
                      <q-input
                        outlined
                        v-model="username"
                        :label="$t('account.Username')"
                        type="text"
                        :rules="[(val) => !!val || $t('account.notEmpty')]"
                        :lazy-rules="true"
                        :loading="loading"
                        :disable="loading"
                      />
                    </div>
                    <div id="firstName" class="q-my-md">
                      <q-input
                        outlined
                        v-model="firstName"
                        :label="$t('account.firstName')"
                        type="text"
                        :loading="loading"
                        :disable="loading"
                      />
                    </div>
                    <div id="lastName" class="q-my-md">
                      <q-input
                        outlined
                        v-model="lastName"
                        :label="$t('account.lastName')"
                        type="text"
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
                    <div id="confirm-password" class="q-my-md">
                      <q-input
                        outlined
                        v-model="confirmPassword"
                        :label="$t('account.ConfirmPassword')"
                        :type="showPwd ? 'text' : 'password'"
                        :rules="[
                          (val) => !!val || $t('account.notEmpty'),
                          (val) =>
                            val === password || $t('account.twoPwdNotMatch'),
                        ]"
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
                    <div id="invitation-code" class="q-my-md">
                      <q-input
                        outlined
                        v-model="invitationCode"
                        :label="$t('account.InvitationCode')"
                        type="text"
                        :loading="loading"
                        :disable="loading"
                      />
                    </div>
                    <div
                      id="login-actions"
                      style="display: flex; flex-direction: row-reverse; flex-wrap: wrap;"
                      class="q-my-md"
                    >
                      <div class="q-ma-sm">
                        <q-btn
                          flat
                          type="submit"
                          :label="$t('account.Register')"
                          :loading="loading"
                          :disable="loading"
                        ></q-btn>
                      </div>
                      <div class="q-ma-sm">
                        <q-btn
                          flat
                          :label="$t('account.Login')"
                          @click="login"
                          :loading="loading"
                          :disable="loading"
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
  </div>
</template>

<script>
  import { apiCaller } from '@/services/apis';
  import { registerMutation } from '@/services/queries';
  import { errorDialog, successDialog } from '@/services/helpers';
  import MaterialCover from '@/components/framework/MaterialCover';

  export default {
    components: { MaterialCover },
    data() {
      return {
        email: '',
        username: '',
        firstName: '',
        lastName: '',
        password: '',
        confirmPassword: '',
        invitationCode: '',
        showPwd: false,
        loading: false,
        logoSrc: require('@/assets/images/compbio-lab.png'),
      };
    },
    computed: {
      responsiveStyle() {
        return {
          'max-width': '900px',
          width: this.$q.screen.gt.xs
            ? this.$q.screen.gt.md
              ? '50vw'
              : '70vw'
            : '100vw',
        };
      },
    },
    methods: {
      login() {
        this.$router.push({
          name: 'Login',
        });
      },
      register() {
        if (
          !this.email ||
          !this.username ||
          !this.password ||
          !this.firstName ||
          !this.lastName ||
          !this.confirmPassword ||
          !this.invitationCode
        ) {
          errorDialog({
            message: 'Info cannot be empty!',
          });
          return;
        }

        if (this.confirmPassword !== this.password) {
          errorDialog({
            message: 'Two passwords must match!',
          });
          return;
        }

        this.loading = true;

        const registerInfo = {
          email: this.email,
          username: this.username,
          firstName: this.firstName,
          lastName: this.lastName,
          password: this.confirmPassword,
          invitationCode: this.invitationCode,
        };

        apiCaller(registerMutation, registerInfo)
          .then((data) => {
            if (data && data.register.success) {
              successDialog({ message: 'Successfully Registered!' });
              this.resetForm();
              this.$router.push({
                name: 'Login',
              });
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
      resetForm() {
        this.username = '';
        this.password = '';
        this.firstName = '';
        this.lastName = '';
        this.confirmPassword = '';
        this.showPwd = false;
        this.loading = false;
      },
    },
  };
</script>
