<template>
  <div class="main-wrapper">
    <div class="custom-button" @click="switchHeatmapTrajectory()">
      {{ getButtonTitle }}
    </div>
    <heatmap v-if="showHeatmap"></heatmap>
    <trajectory v-if="showTrajectory"></trajectory>
  </div>
</template>

<script>
import Heatmap from "@/components/Heatmap";
import Trajectory from "@/components/Trajectory";

export default {
  name: "App",
  data() {
    return {
      showHeatmap: false,
      showTrajectory: true,
    };
  },

  methods: {
    switchHeatmapTrajectory() {
      if (this.showHeatmap) {
        this.showHeatmap = false;
        this.showTrajectory = true;
      } else {
        this.showTrajectory = false;
        this.showHeatmap = true;
      }
    },
  },
  computed: {
    getButtonTitle() {
      if (this.showHeatmap) {
        return "switch to trajectories"
      } else {
        return "switch to heatmaps"
      }
    }
  },

  components: {
    Heatmap,
    Trajectory,
  },
};
</script>


<style lang="scss">
html {
  background: #E5E5E5;
  font-family: cairo, sans-serif;
}

.main-wrapper {
  display: flex;
  flex-direction: column;
  width: auto;
  height: 100%;
  margin: 15px;

  .custom-button {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    box-shadow: rgba(0, 0, 0, 0.35) 0 5px 15px;
    border-radius: 5px;
    width: auto;
    height: 40px;
    background: #333333;
    user-select: none; /* supported by Chrome and Opera */
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    color: #E5E5E5;

    &:hover {
      box-shadow: none;
    }
  }
}
</style>
