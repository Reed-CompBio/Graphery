<template>
  <div class="q-mx-sm q-my-lg">
    <q-intersection once transition="scale" class="expandable-helper">
      <q-card class="article-card-wrapper">
        <section>
          <h6>
            {{ title }}
          </h6>
        </section>
        <section>
          <q-breadcrumbs>
            <q-breadcrumbs-el v-if="authors">
              <q-chip
                clickable
                v-for="author in authors"
                :key="author"
                icon="mdi-card-account-details"
                @click="$emit('author-filter', author)"
              >
                {{ author }}
              </q-chip>
            </q-breadcrumbs-el>
            <q-breadcrumbs-el v-if="categories">
              <q-chip
                clickable
                v-for="category in categories"
                :key="category"
                icon="category"
                @click="$emit('category-filter', category)"
              >
                {{ category }}
              </q-chip>
            </q-breadcrumbs-el>
            <q-breadcrumbs-el v-if="time">
              <q-chip icon="mdi-calendar-month"> {{ time }}</q-chip>
            </q-breadcrumbs-el>
          </q-breadcrumbs>
        </section>
        <section class="article-abstract-section">
          <p>
            {{ abstract }}
          </p>
        </section>
        <q-card-actions>
          <q-btn :to="`/tutorial/${id}`"> Read More </q-btn>
        </q-card-actions>
      </q-card>
    </q-intersection>
  </div>
</template>

<script>
  export default {
    props: ['title', 'authors', 'categories', 'time', 'abstract', 'id'],
  };
</script>

<style lang="sass">
  .article-card-wrapper
    padding: 3px 20px
    h6
      margin: 10px 0px
    .article-abstract-section
      margin-top: 15px
</style>
