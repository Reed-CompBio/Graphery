<template>
  <q-page-container class="q-my-lgi page-container">
    <div class="row q-mx-auto">
      <div class="col">
        <div class="content-container">
          <slot></slot>
        </div>
      </div>
    </div>
  </q-page-container>
</template>

<style>
  .page-container {
    display: flex;
    min-height: 100%;
  }
  .content-container {
    max-width: 1200px;
  }
</style>
