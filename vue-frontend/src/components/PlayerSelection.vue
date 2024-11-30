<template>
  <div class="player-selection-main-wrapper">
    <div class="top-left" @click="selectAllPlayersOfTeam(awayTeam)">select all</div>
    <div class="top-right" @click="selectAllPlayersOfTeam(homeTeam)">select all</div>
    <div class="player-options-wrapper-away">
      <div :class="getPlayerOptionsClass(player, awayTeam)" @click="selectPlayer(player, awayTeam)"
           v-for="(player, index) in teamsOptions.away"
           :key="index">
        <label>
          {{ player }}
        </label>
        <input
            type="checkbox"
            name="playersCheckboxGroup"
            :value="player"
            v-model="selectedPlayers.away"
        >
      </div>
    </div>
    <div class="player-options-wrapper-home">
      <div :class="getPlayerOptionsClass(player, homeTeam)" @click="selectPlayer(player, homeTeam)"
           v-for="(player, index) in teamsOptions.home"
           :key="index">
        <label>
          {{ player }}
        </label>
        <input
            type="checkbox"
            name="playersCheckboxGroup"
            :value="player"
            v-model="selectedPlayers.home"
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PlayerSelection",
  props: ["teamsOptions", "selectedPlayers"],
  data() {
    return {
      awayTeam: 'away',
      homeTeam: 'home'
    };
  },
  watch: {},
  methods: {
    selectAllPlayersOfTeam(team) {
      if (this.allPlayerSelectedOf(team)) {
        this.selectedPlayers[team] = [];
      } else {
        this.selectedPlayers[team] = this.teamsOptions[team];
      }
    },
    selectPlayer(player, team) {
      const team_ = this.selectedPlayers[team];
      if (team_.indexOf(player) > -1) {
        this.selectedPlayers[team] = team_.filter(p => p !== player)
      } else {
        team_.push(player)
      }
    },
    getPlayerOptionsClass(player, team) {
      if (this.selectedPlayers[team].find(p => p === player)) {
        return 'player-options-selected';
      } else {
        return 'player-options';
      }
    },
    allPlayerSelectedOf(team) {
      return this.selectedPlayers[team].length === this.teamsOptions[team].length;
    }
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.player-selection-main-wrapper {
  display: grid;
  grid-template:
    "top_left top_right"
    "away_team home_team"
    "bottom_panel bottom_panel";
  column-gap: 10px;

  .option-tile {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: auto;
    margin-bottom: 10px;
    height: 40px;
    background: #333333;
    user-select: none; /* supported by Chrome and Opera */
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    color: #E5E5E5;

    &:hover {
      box-shadow: #333333 0 0 2px 1px;
    }
  }

  .top-left {
    grid-area: top_left;
    @extend .option-tile;
    background: #FCA311;
    color: #333333;
  }

  .top-right {
    grid-area: top_right;
    @extend .option-tile;
    background: #14203E;
  }

  .player-options-wrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    width: 100%;

    //border-radius: 3px;
    user-select: none; /* supported by Chrome and Opera */
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */

    .player-options {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 100%;
      height: 40px;
      //border-radius: 1px;

      &:hover {
        box-shadow: #333333 0 0 2px 1px;
        z-index: 1;
      }

      input {
        display: none;
      }
    }

    .player-options-selected {
      @extend .player-options;
      color: #E5E5E5;
    }

    .player-options-not-selected {
      @extend .player-options;
      background: #FCA311;
    }

  }

  .player-options-wrapper-away {
    @extend .player-options-wrapper;
    grid-area: away_team;

    .player-options-selected {
      background: #FCA311;
      color: #333333;

      &:hover {
        box-shadow: #333333 0 0 2px 1px;
        z-index: 1;
      }
    }
  }

  .player-options-wrapper-home {
    @extend .player-options-wrapper;
    grid-area: home_team;

    .player-options-selected {
      background: #14203E;

      &:hover {
        box-shadow: #333333 0 0 2px 1px;
        z-index: 1;
      }
    }
  }
}
</style>