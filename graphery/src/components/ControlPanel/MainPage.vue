<template>
  <div>
    <h1>Welcome {{ userObj.username }}</h1>
    <div class="text-h4">
      <p>
        There ain't much you can do in this page, but I promise I will add more
        fun.
      </p>
    </div>
  </div>
</template>

<script>
  import { mapState } from 'vuex';

  export default {
    computed: {
      ...mapState({
        userObj: (state) => state.user,
      }),
    },
  };
</script>
