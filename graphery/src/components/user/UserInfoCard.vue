<template>
  <div>
    <q-card>
      <q-card-section>
        <UserInfoItem
          :title="$t('account.Username')"
          :content="username"
        ></UserInfoItem>
        <UserInfoItem
          :title="$t('account.Email')"
          :content="userEmail"
        ></UserInfoItem>
        <UserInfoItem
          :title="$t('account.Role')"
          :content="userRole"
        ></UserInfoItem>
      </q-card-section>
      <q-separator />
      <q-card-actions align="center">
        <q-btn
          flat
          :label="$t('account.ControlPanel')"
          to="/control-panel"
          v-if="isAuthor || isTranslator || isAdmin"
        >
        </q-btn>
        <q-btn
          flat
          :label="$t('account.DjangoAdminPage')"
          v-if="isAdmin"
          type="a"
          :href="djangoAdminUrl"
          target="_blank"
        />
        <q-btn flat :label="$t('nav.Home')" :to="{ name: 'Home' }" />
        <q-btn flat :label="$t('account.LogOut')" @click="$emit('logout')" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
  import { BASE_URL } from '../../services/api_entry';
  export default {
    props: ['userObj'],
    components: {
      UserInfoItem: () => import('@/components/user/UserInfoItem.vue'),
    },
    data() {
      return {
        djangoAdminUrl: BASE_URL + '/admin',
      };
    },
    computed: {
      username() {
        if (this.userObj) {
          return this.userObj['username'];
        }
        return '';
      },
      userEmail() {
        if (this.userObj) {
          return this.userObj['email'];
        }
        return '';
      },
      userRole() {
        if (this.userObj) {
          return this.userObj['role'];
        }
        return '';
      },
      isAdmin() {
        return this.userRole === 'Administrator';
      },
      isAuthor() {
        return this.userRole === 'Author';
      },
      isTranslator() {
        return this.userRole === 'Translator';
      },
      isVisitor() {
        return this.userRole === 'Visitor';
      },
    },
  };
</script>
