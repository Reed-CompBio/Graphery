<template>
  <q-page class="page">
    <div class="container q-mx-auto q-mb-lg shadow-4">
      <div class="content-container-wrapper flex-center">
        <slot></slot>
      </div>
    </div>
    <!-- TODO add protocol section -->
  </q-page>
</template>

<style scoped lang="sass">
  .page
    clear: both

  .page
    /* TODO use quasar sass variables */
    @media (max-width: 599px)
      padding-left: 0px
      padding-right: 0px
    @media (min-width: 600px) and (max-width: 1439px)
      padding-left: 32px
      padding-right: 32px
    @media (min-width: 1440px)
      padding-left: 64px
      padding-right: 64px
  .container
    min-height: inherit
    max-width: 1200px
    background-color: #ffffff

  .content-container-wrapper
    display: flex
    flex-direction: column
    min-height: 100%
</style>
