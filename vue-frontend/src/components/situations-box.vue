<template>
  <div class="situation-box">
    <div class="team-options">
      <div
          :class="selectedTeams.includes('away') ? 'away-selected' : 'options'"
          @click="updateSelectedTeams('away')"
      >away
      </div>
      <div
          :class="selectedTeams.includes('home') ? 'home-selected' : 'options'"
          @click="updateSelectedTeams('home')"
      >home
      </div>
    </div>
    <div class="button-tiles">
      <div :class="this.selectedSituations.includes(attacksThroughTop) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(attacksThroughTop)"
      >attacks through top
      </div>
      <div :class="this.selectedSituations.includes(attacksThroughCenter) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(attacksThroughCenter)"
      >attacks through center
      </div>
      <div :class="this.selectedSituations.includes(attacksThroughBottom) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(attacksThroughBottom)"
      >attacks through bottom
      </div>
      <div :class="this.selectedSituations.includes(counters) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(counters)"
      >Counter attacks
      </div>
      <div :class="this.selectedSituations.includes(goal) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(goal)"
      >Goals
      </div>
      <div :class="this.selectedSituations.includes(freeKick) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(freeKick)"
      >Free Kick
      </div>
      <div :class="this.selectedSituations.includes(corner) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(corner)"
      >Corner Kick
      </div>
      <div :class="this.selectedSituations.includes(shot) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(shot)"
      >Shots
      </div>
      <div :class="this.selectedSituations.includes(fault) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(fault)"
      >Faults
      </div>
      <div :class="this.selectedSituations.includes(custom) ? 'tile-button-selected' : 'tile-button'"
           @click="updateSelectedSituations(custom)"
      >Custom
      </div>
    </div>
  </div>
</template>

<script>


import {RestService} from "@/services/rest-service.ts";
import {
  ATTACKS_THROUGH_FIELD_PART,
  ATTACKS_THROUGH_TOP,
  ATTACKS_THROUGH_CENTER,
  ATTACKS_THROUGH_BOTTOM,
  CHALLENGE_LEADING_TO_SHOT,
  COUNTERS, FREE_KICK, GOAL,
  KINDS_OF_SITUATIONS, CORNER, SHOT, FAULT, CUSTOM
} from "@/models/situation";

export default {
  name: "situations-box",
  props: [],
  emit: ['situationFilter'],
  data() {
    return {
      restService: RestService.getInstance(),
      selectedSituations: [],
      selectedTeams: ['away', 'home'],
      challengesLeadingToShots: CHALLENGE_LEADING_TO_SHOT,
      attacksThroughTop: ATTACKS_THROUGH_TOP,
      attacksThroughCenter: ATTACKS_THROUGH_CENTER,
      attacksThroughBottom: ATTACKS_THROUGH_BOTTOM,
      counters: COUNTERS,
      goal: GOAL,
      freeKick: FREE_KICK,
      corner: CORNER,
      shot: SHOT,
      fault: FAULT,
      custom: CUSTOM,
      allFilterOptions: [
        this.challengesLeadingToShots,
        this.attacksThroughTop,
        this.attacksThroughCenter,
        this.attacksThroughBottom,
        this.counters,
        this.goal,
        this.freeKick,
        this.corner,
        this.shot,
        this.fault,
        this.custom
      ]
    }
  },
  methods: {
    updateSelectedSituations(situation) {
      this.selectedSituations = this.updateSelection(situation, this.selectedSituations);
      this.$emit('situationFilter', {selectedTeams: this.selectedTeams, selectedSituations: this.selectedSituations});
    },
    updateSelectedTeams(team) {
      this.selectedTeams = this.updateSelection(team, this.selectedTeams);
      this.$emit('situationFilter', {selectedTeams: this.selectedTeams, selectedSituations: this.selectedSituations});
    },
    updateSelection(selected, selection) {
      if (selection.includes(selected)) {
        selection = selection.filter(currentTeam => currentTeam !== selected);
      } else {
        selection.push(selected);
      }
      return selection;
    }
  }
  ,
}
</script>

<style lang="scss" scoped>
.situation-box {
  max-width: 340px;
  background: #333333;

  .team-options {
    display: flex;
    flex-direction: row;
    width: 100%;
    justify-content: center;
    align-items: center;

    .options {
      display: flex;
      width: 100%;
      height: 25px;
      box-shadow: rgba(229, 229, 229, 0.25) 1px 1px 3px 2px;

      justify-content: center;
      align-items: center;
      color: #e5e5e5;
    }

    .away-selected {
      @extend .options;
      background: #FCA311;
      color: #333333;
      box-shadow: none;
    }

    .home-selected {
      @extend .options;
      background: #14203E;
      color: #E5E5E5;
      box-shadow: none;
    }

  }

  .button-tiles {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    padding: 5px;

    .tile-button {
      display: flex;
      text-align: center;
      align-items: center;
      margin: 5px;
      min-width: 60px;
      max-width: 60px;
      min-height: 60px;
      max-height: 60px;
      word-spacing: 1pt;
      font-size: 9pt;
      padding: 5px;
      background: #333333;
      border-radius: 5px;
      border-right: 1px solid #262626;
      border-bottom: 1px solid #262626;
      color: #E5E5E5;
      box-shadow: inset rgba(229, 229, 229, 0.46) 2px 1px 0 1px;
    }

    .tile-button-selected {
      @extend .tile-button;
      background: #414141;
      border-radius: 5px;
      color: #e5e5e5;
      border-left: 1px solid #262626;
      border-top: 1px solid #262626;
      border-right: none;
      border-bottom: none;
      box-shadow: rgba(229, 229, 229, 0.25) 2px 1px 0 1px;
    }
  }
}
</style>