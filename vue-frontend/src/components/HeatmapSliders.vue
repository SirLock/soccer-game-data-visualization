<template>
  <div class="slider-main-wrapper">
    <label class="slider-label">{{this.labelName}}</label>
    <input class="slider" type="range" min=min max=max step="1" v-model="value" @change="changed"/>
    <span class="slider-value" v-text="value"></span>
  </div>
</template>

<script>
export default {
  name: "HeatmapSliders",
  props: ["labelName", "value", "min", "max"],
  data() {
    return {
    }
  },
  watch: {},
  methods: {
      changed() {
          this.$emit("sliderChanged", this.value)
      },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.slider-main-wrapper {
    display: grid;
    grid-template: 
    "slider_label slider slider_value";
    gap: 10px;
    margin: 10px;
    width: 300px;

    .slider-label {
        grid-area: slider_label;
        width: 75px;
    }

    .slider {
        grid-area: slider;
    }

    .slider-value {
        grid-area: slider_value;
        width: 25px;
    }
}
</style>