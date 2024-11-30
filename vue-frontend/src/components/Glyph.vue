<template>
  <div
      class="glyph"
      :style="{
          left: glyph.left +'px',
          top: glyph.top +'px',
          width: glyph.width +'px',
          height: glyph.height +'px',
          zIndex: showInfoBox ? 4 : glyph.zIndex
       }"
      @mouseover="showInfoBox = true" @mouseleave="showInfoBox = false">
    <div class="image-wrapper">
      <label v-if="labelText">{{ labelText }}</label>
      <img
          :src="require(`../assets/glyphs/${glyph.svg}`)"
          :style="{
            width: glyph.width +'px',
            height: glyph.height +'px',
            transform: rotation
          }"
          alt="">
    </div>
    <info-box
        v-if="showInfoBox"
        :style="getLeftOffset(glyph.coordinates.x)"
        :details="prepareDetails(glyph)">
    </info-box>
  </div>
</template>

<script>
import InfoBox from "@/components/InfoBox";
import {CoordinatesHandler} from "@/services/coordinates-handler";
import {EVENT_PASS} from "@/models/events";
import {GameDataService} from "@/services/game-data-service";

export default {
  name: "Glyph",
  components: {InfoBox},
  props: ["glyph", "labelText"],
  data() {
    return {
      gameDataService: GameDataService.getInstance(),
      showInfoBox: false,
    }
  },
  methods: {
    getLeftOffset(xCoordinate) {
      if (xCoordinate > 890 / 2) {
        return `left: -150px`
      }
      return `left: 0`
    },
    prepareDetails(glyph) {
      const objectType = typeof glyph.representedObject;
      const isProbablyPlayer = glyph.representedObject.type === undefined;
      if (objectType === 'Player' || isProbablyPlayer) {
        const player = glyph.representedObject;
        const selectedGameData = this.gameDataService.getCurrentlySelectedGameData();
        let distanceTraveledIntervals;
        if (player.team.toLowerCase() === 'away') {
          distanceTraveledIntervals = selectedGameData.traveledDistancesAway.get(player.name);
        } else {
          distanceTraveledIntervals = selectedGameData.traveledDistancesHome.get(player.name);
        }
        const totalDistance = Math.floor(distanceTraveledIntervals[distanceTraveledIntervals.length - 1]);
        const travelDistanceUntilFrame = Math.floor(this.distanceTraveledUntil(this.gameDataService.currentlyDisplayedAbsoluteFrame, distanceTraveledIntervals));
        return {...player, 'traveled distance [m]': travelDistanceUntilFrame, 'traveled total [m]': totalDistance};
      } else {
        return {...glyph.representedObject};
      }
    },
    distanceTraveledUntil(frame, distanceTraveledIntervals) {
      const minuteOfFrame = (frame / 25) / 60;
      const intervalIndex = Math.floor(minuteOfFrame);
      let traveledDistance = 0;
      for (let i = 0; i <= intervalIndex && i < distanceTraveledIntervals.length; i++) {
        traveledDistance += distanceTraveledIntervals[i];
      }
      return traveledDistance;
    }
  },
  computed: {
    rotation() {
      const event = this.glyph.representedObject;
      if (event.type !== undefined && event.type === EVENT_PASS) {
        const angle = CoordinatesHandler.getGlyphAngle(event.start.x, event.start.y, event.end.x, event.end.y);
        return `rotate(${angle}deg)`;
      }
      return "none";
    },
  },
}
</script>

<style lang="scss" scoped>

.glyph {
  position: absolute;
  background-size: 100% auto;
  background-repeat: no-repeat;
  width: 16px;
  height: 16px;

  .image-wrapper {
    width: 100%;
    height: 100%;

    label {
      position: absolute;
      display: flex;
      justify-content: center;
      align-items: center;
      left: 0;
      top: 0;
      z-index: 1;
      font-size: 9pt;
      color: #E5E5E5;
      width: 100%;
      height: 100%;
      text-align: center;
    }

    img {
      position: absolute;
      left: 0;
      top: 0;
    }
  }
}

</style>