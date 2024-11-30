<template>
  <div class="animation-tool-box">
    <div class="animation-button-wrapper">
      <div v-if="isAnimationRunning"
           style="width: 30px; height: 30px; background-color: #333333;"
           @click="stopAnimation()"
      ></div>
      <img v-if="!isAnimationRunning || isAnimationPaused" :src="require(`../assets/glyphs/play.svg`)" alt="play"
           @click="startOrResumeAnimation()"
      />
      <img v-if="isAnimationRunning && !isAnimationPaused" :src="require(`../assets/glyphs/pause.svg`)" alt="pause"
           @click="pauseAnimation()"
      />
      <div class="no-trail-input-wrapper">
        <label for="no-trails-checkbox">No trails</label>
        <input id="no-trails-checkbox" type="checkbox" onchange="" v-model="noTrails" name="No trails"/>
      </div>
    </div>
    <div class="animation-range-wrapper">
      <input id="animation-range" type="range" min="0" :max="animationLengthInFrames"
             v-model="currentlyDisplayedRelativeFrame"
             @mousedown="pauseAnimation()" @mouseup="seekOnRange()"/>
      <div class="animation-info-display">
        currently displayed second: {{ Math.floor(currentlyDisplayedRelativeFrame / 25) }}s
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "animation-tool-box",
  props: ["isAnimationRunning", "isAnimationPaused", "animationLengthInFrames",
    "currentlyDisplayedRelativeFrame", "noTrails"],
  emits: ["stopAnimation", "startOrResumeAnimation", "pauseAnimation", "seekOnRange", "noTrails"],
  methods: {
    seekOnRange() {
      this.$emit('seekOnRange', this.currentlyDisplayedRelativeFrame);
    },
    stopAnimation() {
      this.$emit('stopAnimation');
    },
    startOrResumeAnimation() {
      this.$emit('startOrResumeAnimation');
    },
    pauseAnimation() {
      this.$emit('pauseAnimation');
    }
  },
  watch: {
    noTrails() {
      this.$emit('noTrails', this.noTrails);
    }
  }
}
</script>

<style lang="scss" scoped>

.animation-tool-box {
  grid-area: bottom_right_panel;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 10px;
  margin-top: 10px;
  width: 330px;

  .animation-button-wrapper {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    margin-bottom: 10px;
    width: 100%;

    img {
      width: 30px;
    }

    .no-trail-input-wrapper {
      background: #333333;
      color: #e5e5e5;
      padding: 5px;
    }
  }

  .animation-range-wrapper {
    display: flex;
    flex-direction: column;
    width: 100%;

    input[type=range] {
      -webkit-appearance: none;
      width: 100%;
    }

    input[type=range]::-webkit-slider-runnable-track {
      height: 5px;
      background: #333333;
      border: none;
      border-radius: 3px;
    }

    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      height: 20px;
      width: 8px;
      border-radius: 5px;
      background: #333333;
      margin-top: -7px;
      border: #e5e5e5 solid 1px;
    }

    input[type=range]:focus {
      outline: none;
    }

    input[type=range]:focus::-webkit-slider-runnable-track {
      background: #333333;
    }

    .animation-info-display {
      margin-top: 15px;
    }
  }
}
</style>