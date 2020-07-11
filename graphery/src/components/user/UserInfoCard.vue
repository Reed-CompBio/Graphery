<template>
  <div class="q-pa-xs">
    <q-card>
      <q-card-section>
        <UserInfoItem title="Username" :content="username"></UserInfoItem>
        <UserInfoItem title="Email" :content="userEmail"></UserInfoItem>
        <UserInfoItem title="Role" :content="userRole"></UserInfoItem>
      </q-card-section>
      <q-card-actions align="center">
        <q-btn label="Admin Page" v-if="isAdmin" />
        <q-btn label="Home" :to="{ name: 'Home' }" />
        <q-btn label="Log Out" @click="$emit('logout')" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
  export default {
    props: ['userObj'],
    components: {
      UserInfoItem: () => import('@/components/user/UserInfoItem.vue'),
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
