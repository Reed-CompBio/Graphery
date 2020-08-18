<template>
  <InfoCard>
    <template v-slot:title>
      Rank
    </template>
    <div>
      <NumberSelection
        class="level-number-selection"
        :end="4"
        label="Difficulty Level"
        v-model="difficultyLevelNumber"
      />
      <NumberSelection
        class="level-number-selection"
        :end="99"
        label="Serial Number"
        v-model="serialNumber"
        :formatter="(obj) => (obj < 10 ? '0' + obj : obj)"
      />
      <NumberSelection
        class="section-number-selection"
        label="Section Number"
        v-model="sectionNumber"
      />
      <div class="rank-display-section text-bold text-h5">
        <span>{{ currentRank.level }}-{{ currentRank.section }}</span>
      </div>
    </div>
  </InfoCard>
</template>

<script>
  export default {
    components: {
      InfoCard: () =>
        import('@/components/ControlPanel/parts/cards/InfoCard.vue'),
      NumberSelection: () =>
        import('@/components/ControlPanel/parts/selectors/NumberSelection'),
    },
    props: {
      currentRank: {
        type: Object,
        default: () => ({
          level: 0,
          section: 0,
        }),
      },
    },
    model: {
      prop: 'currentRank',
      event: 'updateRank',
    },
    computed: {
      difficultyLevelNumber: {
        set(d) {
          this.$emit('updateRank', {
            level: (this.currentRank.level % 100) + d * 100,
            section: this.currentRank.section,
          });
        },
        get() {
          return Math.round(this.currentRank.level / 100);
        },
      },
      serialNumber: {
        set(d) {
          this.$emit('updateRank', {
            level: Math.round(this.currentRank.leading / 100) * 100 + d,
            section: this.currentRank.section,
          });
        },
        get() {
          return this.currentRank.level % 100;
        },
      },
      sectionNumber: {
        set(d) {
          this.$emit('updateRank', {
            level: this.currentRank.level,
            section: d,
          });
        },
        get() {
          return this.currentRank.section;
        },
      },
    },
  };
</script>

<style lang="sass">
  .level-number-selection
    width: 15%
    display: inline-block
    margin: 0 5px

  .section-number-selection
    width: 20%
    display: inline-block
    margin-left: 3%

  .rank-display-section
    margin-left: 5%
    display: inline-block
</style>
