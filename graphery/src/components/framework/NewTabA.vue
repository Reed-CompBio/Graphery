<template>
  <a
    :href="link"
    target="_blank"
    rel="nofollow"
    :class="customClass"
    :style="customStyle"
  >
    <slot></slot>
  </a>
</template>

<script>
  export default {
    props: ['link', 'customClass', 'customStyle'],
  };
</script>
