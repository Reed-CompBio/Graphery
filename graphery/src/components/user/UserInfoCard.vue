<template>
  <div class="q-pa-xs">
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
      <q-card-actions align="center">
        <!-- TODO add a link to admin page -->
        <q-btn
          :label="$t('account.AdminPage')"
          v-if="isAdmin"
          @click="openAdminSite"
        />
        <q-btn :label="$t('nav.Home')" :to="{ name: 'Home' }" />
        <q-btn :label="$t('account.LogOut')" @click="$emit('logout')" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
  import { BASE_URL } from '../../services/apis';
  export default {
    props: ['userObj'],
    components: {
      UserInfoItem: () => import('@/components/user/UserInfoItem.vue'),
    },
    methods: {
      openAdminSite() {
        window.open(this.adminSite);
      },
    },
    computed: {
      adminSite() {
        return BASE_URL + '/admin';
      },
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
