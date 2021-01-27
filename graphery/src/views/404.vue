<template>
  <div>
    <MaterialCover cover-title="404" />
    <MaterialPage>
      <!--    ugliest 404 page ever    -->
      <div title="404" id="err">
        404
      </div>
      <span class="text-h5">
        The page <a class="err-url" :href="pageUrl">{{ pageUrl }}</a> is not
        found
      </span>
    </MaterialPage>
  </div>
</template>

<script>
  import MaterialCover from '@/components/framework/MaterialCover';
  export default {
    components: {
      MaterialCover,
      MaterialPage: () => import('@/components/framework/MaterialPage.vue'),
    },
    computed: {
      pageUrl() {
        return this.$route.params.pathMatch;
      },
    },
    metaInfo: {
      title: '404 Not Found',
    },
  };
</script>

<style>
  .err-url,
  .err-url:visited {
    color: red;
  }

  #err {
    font-size: 128px;
    animation: glitch 2s linear infinite;
  }

  @keyframes glitch {
    2%,
    64% {
      transform: translate(2px, 0) skew(0deg);
    }
    4%,
    60% {
      transform: translate(-2px, 0) skew(0deg);
    }
    62% {
      transform: translate(0, 0) skew(5deg);
    }
  }

  #err:before,
  #err:after {
    content: attr(title);
    position: absolute;
    left: 0;
  }

  #err:before {
    animation: glitchTop 1s linear infinite;
    clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
    -webkit-clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
  }

  @keyframes glitchTop {
    2%,
    64% {
      transform: translate(2px, -2px);
    }
    4%,
    60% {
      transform: translate(-2px, 2px);
    }
    62% {
      transform: translate(13px, -1px) skew(-13deg);
    }
  }

  #err:after {
    animation: glitchBotom 1.5s linear infinite;
    clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
    -webkit-clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
  }

  @keyframes glitchBotom {
    2%,
    64% {
      transform: translate(-2px, 0);
    }
    4%,
    60% {
      transform: translate(-2px, 0);
    }
    62% {
      transform: translate(-22px, 5px) skew(21deg);
    }
  }
</style>
