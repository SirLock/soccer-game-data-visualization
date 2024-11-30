<template>
  <div class="time-line-main-wrapper">
    <div @click="switchPeriod()" class="switch-periods">
      {{ selectedPeriod }}
    </div>
    <div class="time-line-wrapper">
      <div class="time-line-background-layer">
        <div v-for="(n, index) in Math.floor(numberOfTimeLineHints)" :key="index"
             class="time-hint" :style="{marginLeft: hintBoxWidth}">
          <div class="time-mark">{{ (n * 5) }}</div>
        </div>
      </div>
      <div class="time-line">
        <situation-glyph
            v-for="(situation, index) in situationsSubselection" :key="index"
            v-on:situationId="triggerGlyphClickedEvent($event)"
            :situation="situation"
            :timeline-width="this.timelineWidth"
            :game-periods-information="gamePeriodsInformation"
            :selected-period="selectedPeriod"
            :sequence-number="index"
        ></situation-glyph>
      </div>
    </div>
  </div>
</template>

<script>
import SituationGlyph from "@/components/situation-glyph";

export default {
  name: "TimeLine",
  components: {SituationGlyph},
  props: ['gameLength', 'firstPeriodEndFrame', 'secondPeriodStartFrame', 'situations'],
  emits: ['situationId'],
  data() {
    return {
      selectedPeriod: 1,
      timelineWidth: 890 - 30,
    }
  },
  methods: {
    switchPeriod() {
      if (this.selectedPeriod === 1) {
        this.selectedPeriod = 2;
      } else {
        this.selectedPeriod = 1;
      }
    },
    triggerGlyphClickedEvent(id) {
      this.$emit('situationId', id)
    },
  },
  computed: {
    gamePeriodsInformation() {
      return {
        gameLength: this.gameLength,
        firstPeriodEndFrame: this.firstPeriodEndFrame,
        secondPeriodStartFrame: this.secondPeriodStartFrame
      }
    },
    secondPeriodLength() {
      return this.gameLength - this.secondPeriodStartFrame;
    },
    hintBoxWidth() {
      return ((890 - 30) / this.numberOfTimeLineHints) + 'px';
    },
    numberOfTimeLineHints() {
      let periodLength = 0;
      if (this.selectedPeriod === 1) {
        periodLength = this.firstPeriodEndFrame;
      } else {
        periodLength = this.secondPeriodLength;
      }
      return (periodLength / 7500);
    },
    situationsSubselection() {
      let filteredSituations = [];
      if (!this.situations) {
        return filteredSituations;
      }
      if (this.selectedPeriod === 1) {
        filteredSituations = this.situations.filter(situation => {
          return situation.period === 1
        });
      } else {
        filteredSituations = this.situations.filter(situation => {
          return situation.period === 2
        });
      }
      filteredSituations.sort((situation1, situation2) => situation1.compare(situation2));
      return filteredSituations;
    }
  }
}
</script>

<style lang="scss" scoped>
.time-line-main-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  height: max-content;

  .switch-periods {
    display: flex;
    box-shadow: inset rgba(0, 0, 0, 0.35) 0 0 2px 1px;
    width: 30px;
    height: 75px;
    justify-content: center;
    align-items: center;
    user-select: none; /* supported by Chrome and Opera */
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
  }

  .time-line-wrapper {
    position: relative;

    .time-line-background-layer {
      position: absolute;
      display: flex;
      flex-direction: row;
      top: 0;
      left: 0;
      width: 100%;
      height: 15px;

      .time-hint {
        position: relative;
        width: 1px;
        background: #333333;

        .time-mark {
          position: relative;
          top: 15px;
          left: 0;
        }
      }
    }

    .time-line {
      position: relative;
      top: 0;
      left: 0;
      width: 890px - 30px;
      height: 5px;
      background: #333333;
      border-radius: 10px;

      .time-span-bundle {
        position: absolute;
        top: 0;
        left: 0;
        display: flex;
        flex-direction: column;

        .time-span {
          background-color: #FCA311;
          height: 10px;
        }
      }
    }
  }
}
</style>