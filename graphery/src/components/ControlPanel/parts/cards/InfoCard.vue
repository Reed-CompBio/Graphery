<template>
  <q-card class="q-mb-md">
    <q-card-section>
      <slot name="title"></slot>
    </q-card-section>
    <q-separator />
    <q-card-section>
      <slot></slot>
    </q-card-section>
  </q-card>
</template>
