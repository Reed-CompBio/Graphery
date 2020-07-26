<template>
  <q-card class="q-px-md q-py-lg q-mt-xl q-mb-sm license-card white-a">
    <p>
      {{ $t('license.licenseInfo1') }}
      <a
        rel="license"
        target="_blank"
        href="http://creativecommons.org/licenses/by-nc-sa/4.0/"
      >
        {{ $t('license.licenseInfo2') }}
      </a>
    </p>
    <p class="no_mb_p">
      <a
        rel="license"
        target="_blank"
        href="http://creativecommons.org/licenses/by-nc-sa/4.0/"
      >
        <img
          alt="Creative Commons License"
          style="border-width:0"
          src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png"
        />
      </a>
    </p>
  </q-card>
</template>

<style lang="sass">
  .no_mb_p
    margin-bottom: 0
  .license-card
    background-color: #a70e16
    color: white
    a
      color: inherit
      text-decoration: underline
</style>
