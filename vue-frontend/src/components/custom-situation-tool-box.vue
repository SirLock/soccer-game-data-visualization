<template>
  <div class="custom-situation-tool-box">
    <div class="custom-situation-attribute">
      <label for="startPoint">Start time [seconds]</label>
      <input id="startPoint" type="number" min="1">
      <!--            <standard-button style="margin-left: 10px;" :value="'+'"-->
      <!--                             @click="setCustomSituationStartTimeByClick()"-->
      <!--            ></standard-button>-->
    </div>
    <div class="custom-situation-attribute">
      <label for="endPoint">End time [seconds]</label>
      <input id="endPoint" type="number" min="1">
      <!--            <standard-button style="margin-left: 10px;" :value="'+'"-->
      <!--                             @click="setCustomSituationEndTimeByClick()"-->
      <!--            ></standard-button>-->
    </div>
    <div class="custom-situation-attribute">
      <label for="period">Period</label>
      <input id="period" type="number">
    </div>
    <div class="custom-situation-attribute">
      <label for="team">Team</label>
      <input id="team" type="text">
    </div>
    <div class="custom-situation-button-panel">
      <standard-button class="custom-situation-button" :value="'Add custom situation'"
                       @click="emitNewCustomSituation()"></standard-button>
      <standard-button class="custom-situation-button" :value="'Remove'"
                       @click="emitRemoveCustomSituation()"></standard-button>
    </div>
  </div>
</template>

<script>
import StandardButton from "@/components/standard-button";
import {Situation} from "@/models/situation";

export default {
  name: "custom-situation-tool-box",
  props: ["displayedSituation"],
  emits: ["addCustomSituation", "customSituationToRemove"],
  components: {StandardButton},
  methods: {
    emitNewCustomSituation() {
      let startSecond = document.getElementById('startPoint').value;
      let endSecond = document.getElementById('endPoint').value;
      let period = document.getElementById('period').value;
      const team = document.getElementById('team').value;
      if (startSecond === "" || endSecond === "" || period === "" || team === "") {
        return;
      }
      const startFrame = Math.floor(Number(startSecond)) * 25;
      const endFrame = Math.floor(Number(endSecond)) * 25;
      period = Number(period);
      this.$emit(
          'addCustomSituation',
          Situation.fromCustomInput({
            startFrame,
            endFrame,
            period,
            team
          }));
    },
    emitRemoveCustomSituation() {
      if (this.displayedSituation.kind === 'custom') {
        this.$emit('customSituationToRemove', this.displayedSituation);
      }
    },
    setDisplayedInfo(situation) {
      document.getElementById('startPoint').value = situation.startFrame / 25;
      document.getElementById('endPoint').value = situation.endFrame / 25;
      document.getElementById('period').value = situation.period;
      document.getElementById('team').value = situation.team;
    },
    clearDisplayedInfo() {
      document.getElementById('startPoint').value = '';
      document.getElementById('endPoint').value = '';
      document.getElementById('period').value = '';
      document.getElementById('team').value = '';
    }
  },
  watch: {
    displayedSituation() {
      if (this.displayedSituation) {
        this.setDisplayedInfo(this.displayedSituation);
      } else {
        this.clearDisplayedInfo();
      }
    }
  },
}
</script>

<style lang="scss" scoped>

.custom-situation-tool-box {
  display: flex;
  flex-direction: column;
  width: 320px;
  margin-top: 10px;
  color: #E5E5E5;
  background: #333333;
  padding: 10px;
  font-size: 11pt;

  .custom-situation-attribute {
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
  }

  .custom-situation-button-panel {
    display: flex;
    margin-top: 5px;

    .custom-situation-button {
      margin-right: 15px;
    }
  }
}
</style>