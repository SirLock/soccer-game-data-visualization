<template>
  <div :class="isSelected ? 'situation-glyph-wrapper-selected' : 'situation-glyph-wrapper'"
       :style="{
          left: (this.getXPositionOnTimeline() - 13)+'px',
          borderColor: (this.isSelected ? timespanHintColor : 'rgba(51, 51, 51, 0)')
        }"
       @click.left="toggleSelectionAndEmit()"
       @click.right="toggleSelection($event)"
       @mouseover="showInfoBox = true" @mouseleave="showInfoBox = false">
    <div class="glyph-container">
      <div class="time-line-pin"
           :style="{height: (sequenceNumber*10 + 40)+'px'}">
        <div class="time-span-hint"
             :style="{width: getTimespan()+'px', background: timespanHintColor}">
          <div class="click-lug"></div>
        </div>
      </div>
      <img class="situation-glyph"
           :src="require(`../assets/glyphs/soccerBall.svg`)"
           alt="">
    </div>
  </div>
  <info-box
      v-if="showInfoBox"
      :details="situation"
      :style="{top: -175+'px'}">
  </info-box>
</template>

<script>
import InfoBox from "@/components/InfoBox";

export default {
  name: "situation-glyph",
  components: {InfoBox},
  emits: ['situationId'],
  props: ['situation', 'timelineWidth', 'gamePeriodsInformation', 'selectedPeriod', 'sequenceNumber'],
  data() {
    return {
      awayColor: '#FCA311',
      homeColor: '#14203E',
      isSelected: false,
      showInfoBox: false,
    }
  },
  methods: {
    toggleSelection(event) {
      event.preventDefault();
      this.isSelected = !this.isSelected;
    },
    toggleSelectionAndEmit() {
      this.isSelected = true;
      this.$emit('situationId', this.situation.id);
    },
    getTimespan() {
      return Math.floor(((this.situation.endFrame - this.situation.startFrame) / this.periodLength) * this.timelineWidth);
    },
    getXPositionOnTimeline() {
      const startFrame = this.situation.startFrame;
      let relativePosition = 0;
      if (this.selectedPeriod === 1) {
        relativePosition = startFrame / this.firstPeriodLength;
      } else {
        relativePosition = (startFrame - this.secondPeriodStartFrame) / this.secondPeriodLength;
      }
      return Math.floor(this.timelineWidth * relativePosition);
    },
  },
  computed: {
    timespanHintColor() {
      return this.situation.team === 'Away' ? this.awayColor : this.homeColor;
    },
    firstPeriodLength() {
      return this.gamePeriodsInformation.firstPeriodEndFrame;
    },
    secondPeriodStartFrame() {
      return this.gamePeriodsInformation.secondPeriodStartFrame;
    },
    gameLength() {
      return this.gamePeriodsInformation.gameLength;
    },
    secondPeriodLength() {
      return this.gameLength - this.secondPeriodStartFrame;
    },
    periodLength() {
      return this.selectedPeriod === 1 ? this.firstPeriodLength : this.secondPeriodLength;
    }
  }
}
</script>

<style lang="scss" scoped>
.situation-glyph-wrapper {
  position: absolute;
  top: -27px;
  width: 27px;
  height: 27px;
  border-radius: 100%;

  &:hover {
    border-width: 2px;
    border-style: solid;
    border-color: rgba(51, 51, 51, 0);
    z-index: 2;
  }

  .glyph-container {
    display: flex;
    width: 100%;
    height: 100%;

    .time-line-pin {
      position: relative;
      top: 26px;
      left: 13px;
      width: 1px;
      background: #3333337F;
      display: flex;
      flex-direction: column-reverse;

      .time-span-hint {
        position: relative;
        height: 5px;
        background: #FCA311;

        .click-lug {
          position: relative;
          height: 10px;
          width: 10px;
          background: rgba(51, 51, 51, 0.1);
          border-bottom: 1px solid rgba(51, 51, 51, 0.4);
        }
      }
    }

    .situation-glyph {
      position: relative;
      left: -1px;
    }
  }

  .situation-glyph-info {

  }
}

.situation-glyph-wrapper-selected {
  @extend .situation-glyph-wrapper;
  border-width: 2px;
  border-style: solid;
  z-index: 1;
}
</style>