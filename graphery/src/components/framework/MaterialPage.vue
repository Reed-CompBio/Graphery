<template>
  <q-page class="page">
    <div class="container q-mx-auto">
      <div class="content-container-wrapper">
        <slot></slot>
      </div>
    </div>
  </q-page>
</template>

<style lang="sass" scoped>
  @import "src/styles/quasar.variables"

  .page
    clear: both
    // accord with Material Cover
    top: -8rem

  .page
    @media (max-width: $breakpoint-xs-max)
      padding-left: 0px
      padding-right: 0px
    @media (min-width: $breakpoint-sm-min) and (max-width: $breakpoint-md-max)
      padding-left: 32px
      padding-right: 32px
    @media (min-width: $breakpoint-lg-min)
      padding-left: 64px
      padding-right: 64px

  .container
    min-height: inherit
    max-width: 1200px
    box-shadow: rgba(0, 0, 0, 0.25) 0px 25px 50px -12px

  .body--light .container
    background-color: #ffffff
  .body--dark .container
    background-color: #272727

  .content-container-wrapper
    display: flex
    flex-direction: column
    min-height: 100%

  .container
    @media (max-width: $breakpoint-xs-max)
      padding: 16px 7% 50px
    @media (min-width: $breakpoint-sm-min) and (max-width: $breakpoint-md-max)
      margin-bottom: 24px
      padding: 16px 6% 50px
    @media (min-width: $breakpoint-lg-min)
      margin-bottom: 24px
      padding: 16px 0 50px

  .content-container-wrapper
    margin: 0 auto
    max-width: 900px
</style>
