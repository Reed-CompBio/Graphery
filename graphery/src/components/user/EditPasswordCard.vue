<template>
  <q-card>
    <q-card-section>
      <q-form>
        <UserInfoEditItem
          name="old_password"
          :type="showOldPwd ? 'text' : 'password'"
          v-model="oldPassword"
          :rules="[(val) => !!val || $t('account.notEmpty')]"
          :lazy-rules="true"
          :label="$t('account.Old Password')"
        >
          <template v-slot:append>
            <q-icon
              :name="showOldPwd ? 'visibility' : 'visibility_off'"
              class="cursor-pointer"
              @click="showOldPwd = !showOldPwd"
            />
          </template>
        </UserInfoEditItem>
        <UserInfoEditItem
          name="new_password"
          :type="showNewPwd ? 'text' : 'password'"
          v-model="newPassword"
          :rules="[(val) => !!val || $t('account.notEmpty')]"
          :lazy-rules="true"
          :label="$t('account.New Password')"
        >
          <template v-slot:append>
            <q-icon
              :name="showNewPwd ? 'visibility' : 'visibility_off'"
              class="cursor-pointer"
              @click="showNewPwd = !showNewPwd"
            />
          </template>
        </UserInfoEditItem>
        <UserInfoEditItem
          name="confirm_password"
          :type="showConfirmedPwd ? 'text' : 'password'"
          v-model="confirmedPassword"
          :rules="[
            (val) => !!val || $t('account.notEmpty'),
            (val) => val === newPassword || $t('account.twoPwdNotMatch'),
          ]"
          :lazy-rules="true"
          :label="$t('account.Confirm New Password')"
        >
          <template v-slot:append>
            <q-icon
              :name="showConfirmedPwd ? 'visibility' : 'visibility_off'"
              class="cursor-pointer"
              @click="showConfirmedPwd = !showConfirmedPwd"
            />
          </template>
        </UserInfoEditItem>
      </q-form>
    </q-card-section>
    <q-separator />
    <q-card-actions align="center">
      <q-btn flat @click="updateInfo" :label="$t('account.Update Password')" />
    </q-card-actions>
  </q-card>
</template>

<script>
  import UserInfoEditItem from '@/components/user/UserInfoEditItem';
  import { apiCaller } from '@/services/apis';
  import { changePasswordMutation } from '@/services/queries';
  import { errorDialog, successDialog } from '@/services/helpers';

  export default {
    components: { UserInfoEditItem },
    props: ['userObj'],
    data() {
      return {
        oldPassword_: '',
        newPassword_: '',
        confirmedPassword_: '',
        showOldPwd: false,
        showNewPwd: false,
        showConfirmedPwd: false,
      };
    },
    computed: {
      oldPassword: {
        set(d) {
          this.oldPassword_ = d;
        },
        get() {
          return this.oldPassword_;
        },
      },
      newPassword: {
        set(d) {
          this.newPassword_ = d;
        },
        get() {
          return this.newPassword_;
        },
      },
      confirmedPassword: {
        set(d) {
          this.confirmedPassword_ = d;
        },
        get() {
          return this.confirmedPassword_;
        },
      },
    },
    methods: {
      updateInfo() {
        apiCaller(changePasswordMutation, {
          oldPassword: this.oldPassword,
          newPassword: this.newPassword,
        })
          .then((data) => {
            if (!data || !('changePassword' in data)) {
              throw Error;
            }
            if (!data['changePassword']['success']) {
              throw Error;
            }
            const userObj = data['changePassword']['user'];
            this.$store.dispatch('setUser', userObj);

            successDialog({
              message: 'Update Password Successfully!',
            });
          })
          .catch((err) => {
            errorDialog({
              message: `An error occurred during changing the password. Error: ${err}`,
            });
          });
      },
    },
  };
</script>
