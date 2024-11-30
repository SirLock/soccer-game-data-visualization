<template>
  <div class="component-wrapper">
    <div v-if="isDataLoading" class="loading-hint-container">
      <div class="loading-hint"></div>
    </div>
    <div class="trajectory-main-wrapper">
      <div class="top-panel">
        <div class="select-game-data-dropdown">
          <div class="dropdown-button">{{ selectedGameDataId ? selectedGameDataId : 'Select game data' }}
          </div>
          <div class="dropdown-content">
            <div @click="selectedGameDataId='sample_game_1'" class="game-data-option">sample_game_1</div>
            <div @click="selectedGameDataId='sample_game_2'" class="game-data-option">sample_game_2</div>
          </div>
        </div>
        <standard-button class="top-buttons" :value="'Request game data'"
                         @click="triggerRequestGameData(selectedGameDataId)"
        ></standard-button>
        <standard-button class="top-buttons" :value="'Animate situation'"
                         @click="triggerRenderSituation(displayedSituationId, true)"
        ></standard-button>
      </div>
      <div class="left-panel-wrapper">
        <div class="player-filter-options">
          <div :class="selectedPlayerFilterType === 'None' ? 'selected' : 'options'"
               @click="setFilterType('None')"
          >None
          </div>
          <div :class="selectedPlayerFilterType === 'Distance' ? 'selected' : 'options'"
               @click="setFilterType('Distance')"
          >Distance
            <input style="max-width: 50px; margin-left: 10px" id="player-distance" type="number"
                   v-model="filterPlayerDistance" step="0.5" min="0.5" max="100"/>
            <label style="margin-left:5px" for="player-distance">m</label>
          </div>
        </div>
        <player-selection :teams-options="teamsPlayerOptions"
                          :selected-players="teamsSelectedPlayers"></player-selection>
      </div>
      <div class="display-wrapper">
        <div class="soccer-field-container"></div>
        <div id="canvas-prolonged" class="trajectory-canvas-container"></div>
        <div class="glyph-overlay-wrapper">
          <div class="glyph-wrapper" :id="glyph.id" v-for="(glyph, index) in eventGlyphsToDisplay" :key="index">
            <glyph v-if="glyph.frame === -1"
                   :glyph="glyph" :label-text="glyph?.labelText"></glyph>
            <glyph v-else
                   :glyph="glyph" :label-text="glyph?.labelText"
                   @click="setPlayerGlyphsToEventFrameAndRerender(glyph.frame + offsetForProperSituationDisplay)"></glyph>
          </div>
        </div>
      </div>
      <div class="right-panel">
        <custom-situation-tool-box
            v-bind:displayed-situation="situationDisplayedInCustomSituationBox"
            v-on:addCustomSituation="addCustomSituation($event)"
            v-on:customSituationToRemove="removeSituation($event)"
        ></custom-situation-tool-box>
        <situations-box
            v-on:situationFilter="updateSituationFilter($event)"
        ></situations-box>
        <div class="event-glyph-selection-container">
          <div v-for="(eventOption, index) in displayableEventsOptions" :key="index"
               :class="selectedEventGlyphs.includes(eventOption) ? 'tile-button-selected' : 'tile-button'"
               @click="updateSelectedEventGlyphs(eventOption)">
            {{ eventOption }}
            <img style="margin-left: 3px; width: 16px; height: 16px" :src="getSvgSource(eventOption)" alt=""/>
          </div>
        </div>
      </div>
      <div class="bottom-panel">
        <time-line v-if="this.gameData && this.situations"
                   :game-length="this.gameData.trackingAway.length"
                   :first-period-end-frame="this.gameData.basicInformation?.firstPeriodEnd"
                   :second-period-start-frame="this.gameData.basicInformation?.secondPeriodStart"
                   :situations="this.filteredSituations"
                   v-on:situationId="situationGlyphClicked($event)"
                   @click.right="setFrameForCustomSituation($event)"
        ></time-line>
      </div>
      <animation-tool-box
          :is-animation-paused="isAnimationPaused"
          :is-animation-running="isAnimationRunning"
          :animation-length-in-frames="animationLengthInFrames"
          :currently-displayed-relative-frame="currentlyDisplayedRelativeFrame"
          v-on:no-trails="changeNoTrails($event)"
          v-on:stopAnimation="stopAnimation()"
          v-on:startOrResumeAnimation="startOrResumeAnimation()"
          v-on:pauseAnimation="pauseAnimation()"
          v-on:seekOnRange="resumeAnimationAt($event)"
      ></animation-tool-box>
    </div>
  </div>
</template>

<script>
import * as p5 from "p5";
import PlayerSelection from "./PlayerSelection.vue";
import Glyph from "@/components/Glyph.vue";
import {RestService} from "@/services/rest-service";
import TimeLine from "@/components/TimeLine";
import {TransformDto} from "@/services/transform-dto";
import {GameData} from "@/models/game-data";
import {GlyphHandler} from "@/services/glyph-handler";
import {DrawAndRenderFunctions} from "@/services/draw-and-render-functions";
import SituationsBox from "@/components/situations-box";
import {KINDS_OF_SITUATIONS} from "@/models/situation";
import {EVENT_ALL, EVENT_SVG_MAPPINGS} from "@/models/events";
import StandardButton from "@/components/standard-button";
import {GameDataService} from "@/services/game-data-service";
import CustomSituationToolBox from "@/components/custom-situation-tool-box";
import AnimationToolBox from "@/components/animation-tool-box";


export default {
  components: {
    AnimationToolBox,
    CustomSituationToolBox,
    StandardButton,
    SituationsBox,
    TimeLine,
    PlayerSelection,
    Glyph
  },
  name: "Trajectory",
  created() {
    this.gameData = this.$store.state.gameData;
    if (!this.$store.state.trajectories) {
      return;
    }
    this.situations = this.$store.state.trajectories.situations;
    this.eventGlyphsToDisplay = this.$store.state.trajectories.eventGlyphsToDisplay;
    this.eventsToDisplay = this.$store.state.trajectories.eventsToDisplay;
    this.teamsSelectedPlayers = this.$store.state.trajectories.teamsSelectedPlayers;
    this.teamsPlayerOptions = this.$store.state.trajectories.teamsPlayerOptions;
    this.displayedSituationId = this.$store.state.trajectories.displayedSituationIndex;
    if (this.$store.state.trajectories.situationFilter) {
      this.situationFilter = this.$store.state.trajectories.situationFilter;
    } else {
      this.situationFilter = {
        selectedTeams: ['away', 'home'],
        selectedSituations: KINDS_OF_SITUATIONS,
      }
    }

    if (this.displayedSituationId > -1) {
      this.triggerRenderSituation(this.displayedSituationId, false);
    }
  },
  data() {
    return {
      animationLengthInFrames: 0,
      currentlyDisplayedRelativeFrame: 0,
      currentlyDisplayedAbsoluteFrame: 0,
      restService: RestService.getInstance(),
      gameDataService: GameDataService.getInstance(),
      isAnimationRunning: false,
      isAnimationPaused: false,
      eventSvgMappings: EVENT_SVG_MAPPINGS,
      selectedEventGlyphs: EVENT_ALL,
      displayableEventsOptions: EVENT_ALL,
      selectedGameDataId: '',
      colorAway: "#FCA311",
      colorHome: "#14203E",
      p5canvas: {
        prolonged: null
      },
      gameData: null,
      displayedSituationId: -1,
      eventsToDisplay: [],
      eventGlyphsToDisplay: [],
      teamsSelectedPlayers: {
        away: [],
        home: []
      },
      teamsPlayerOptions: {
        away: [],
        home: []
      },
      isDataLoading: false,
      filteredSituations: null,
      situations: null,
      situationFilter: {
        selectedTeams: ['away', 'home'],
        selectedSituations: KINDS_OF_SITUATIONS,
      },
      situationEventDataMap: new Map(),
      offsetForProperSituationDisplay: 2,
      selectedPlayerFilterType: "None",
      situationDisplayedInCustomSituationBox: null,
      filterPlayerDistance: 3,
      listenOnTimeLineClickForStartFrame: false,
      listenOnTimeLineClickForEndFrame: false,
      renderGameParameters: {
        trackingData: null,
        teamsPlayers: null,
        selectedEntities: this.teamsSelectedPlayers,
        eventsToDisplay: this.eventsToDisplay,
        frameOffset: 0,
        animate: false,
        noTrails: false,
        eventGlyphs: this.eventGlyphsToDisplay,
        eventGlyphsFilter: this.selectedEventGlyphs,
        lastIndexOfTrackingData: 0,
        currentFrame: 0,
      },
    };
  },
  methods: {
    changeNoTrails(noTrails) {
      this.renderGameParameters.noTrails = Boolean(noTrails);
    },
    setCustomSituationStartTimeByClick() {
      this.listenOnTimeLineClickForStartFrame = true;
      this.listenOnTimeLineClickForEndFrame = false;
    },
    setCustomSituationEndTimeByClick() {
      this.listenOnTimeLineClickForStartFrame = false;
      this.listenOnTimeLineClickForEndFrame = true;
    },
    setFrameForCustomSituation(event) {
      event.preventDefault();
      const xOnTimeLine = event.offsetX;
      const selectedFrame = xOnTimeLine * (this.gameData.basicInformation.firstPeriodEnd / 860);
      if (this.listenOnTimeLineClickForStartFrame) {
        document.getElementById('startPoint').value = Math.floor(selectedFrame / 25);
      }
      if (this.listenOnTimeLineClickForEndFrame) {
        document.getElementById('endPoint').value = Math.floor(selectedFrame / 25);
      }
    },
    stopAnimation() {
      this.isAnimationRunning = false;
      this.isAnimationPaused = false;
      this.triggerRenderSituation(this.displayedSituationId, false);
    },
    pauseAnimation() {
      this.p5canvas.prolonged.noLoop();
      this.isAnimationPaused = true;
    },
    resumeAnimationAt(currentFrame) {
      this.eventGlyphsToDisplay = [];
      this.renderGameParameters.currentFrame = Number(currentFrame);
      this.isAnimationPaused = false;
      this.isAnimationRunning = true;
      this.renderGame(this.renderGameParameters);
    },
    startOrResumeAnimation() {
      if (this.isAnimationRunning && this.isAnimationPaused) {
        this.p5canvas.prolonged.loop();
        if (this.p5canvas.prolonged.isLooping()) {
          this.isAnimationPaused = false;
        }
      } else {
        this.isAnimationRunning = true;
        this.triggerRenderSituation(this.displayedSituationId, true);
      }
    },
    getSvgSource(eventName) {
      const svgName = this.eventSvgMappings[eventName];
      return require(`../assets/glyphs/${svgName}`);
    },
    async triggerRequestGameData(dataSetId) {
      this.isDataLoading = true;
      let [trackingAway, trackingHome, traveledDistances, playersAway, playersHome, basicInformation, events,
        challengesLeadingToShots, attacksThroughTop, attacksThroughCenter, attacksThroughBottom, counters, goals, shots, faults, corners, freeKicks] = await Promise.all([
        this.restService.requestTrackingData(dataSetId, 'away'),
        this.restService.requestTrackingData(dataSetId, 'home'),
        this.restService.requestTraveledDistances(dataSetId),
        this.restService.requestPlayers(dataSetId, 'away'),
        this.restService.requestPlayers(dataSetId, 'home'),
        this.restService.requestBasicInformation(dataSetId),
        this.restService.requestEvents(dataSetId),
        this.restService.requestChallengesLeadingToShots(dataSetId),
        this.restService.requestAttackThroughFieldPart(dataSetId, "top"),
        this.restService.requestAttackThroughFieldPart(dataSetId, "center"),
        this.restService.requestAttackThroughFieldPart(dataSetId, "bottom"),
        this.restService.requestCounters(dataSetId),
        this.restService.requestGoals(dataSetId),
        this.restService.requestShots(dataSetId),
        this.restService.requestFaults(dataSetId),
        this.restService.requestCorners(dataSetId),
        this.restService.requestFreeKicks(dataSetId)
      ]);
      this.isDataLoading = false;
      const gameData = new GameData({...this.gameData, id: dataSetId});
      gameData.trackingAway = TransformDto.toFrameElements(trackingAway);
      gameData.trackingHome = TransformDto.toFrameElements(trackingHome);
      gameData.traveledDistancesAway = TransformDto.toTraveledDistancesMaps(traveledDistances.away);
      gameData.traveledDistancesHome = TransformDto.toTraveledDistancesMaps(traveledDistances.home);
      gameData.playersAway = TransformDto.toPlayersMap(playersAway);
      gameData.playersHome = TransformDto.toPlayersMap(playersHome);
      gameData.basicInformation = TransformDto.toBasicInformation(basicInformation);
      gameData.events = events;
      this.gameData = gameData;

      this.situations = TransformDto.toSituations([
        ...challengesLeadingToShots,
        ...attacksThroughTop,
        ...attacksThroughCenter,
        ...attacksThroughBottom,
        ...counters,
        ...goals,
        ...shots,
        ...faults,
        ...corners,
        ...freeKicks
      ]);
    },

    async triggerRequestEventsWithin(dataSetId, startFrame, endFrame) {
      this.eventsToDisplay = await this.restService.requestEventsWithin(dataSetId, startFrame, endFrame);
    },

    async triggerRequestRelevantPlayersByDistance(dataSetID, teamID, startFrame, endFrame, relevantDistance) {
      return await this.restService.requestRelevantPlayersByDistance(dataSetID, teamID, startFrame, endFrame, relevantDistance);
    },

    async triggerRequestRelevantPlayersByPassParticipation(dataSetID, startFrame, endFrame) {
      return await this.restService.requestRelevantPlayersByPassParticipation(dataSetID, startFrame, endFrame);
    },

    async triggerRenderSituation(situationId, animate, earlyEndFrame) {
      const gameDataId = this.selectedGameDataId;
      if (!this.gameData || !this.situations || situationId < 0) {
        console.log("Cannot render situation. No data available.");
        return;
      }
      this.displayedSituationId = situationId;
      const situation = this.getSituationById(situationId);
      const startFrame = situation.startFrame;
      const endFrame = earlyEndFrame ? earlyEndFrame : situation.endFrame + this.offsetForProperSituationDisplay;
      await this.triggerRequestEventsWithin(gameDataId, startFrame, endFrame);
      const partialGameData = {
        away: [],
        home: [],
      };
      for (let i = startFrame - 1; i < endFrame; i++) {
        partialGameData.away.push(this.gameData.trackingAway[i]);
        partialGameData.home.push(this.gameData.trackingHome[i]);
      }
      const teamsPlayers = {
        away: this.gameData.playersAway,
        home: this.gameData.playersHome
      }

      if (this.selectedPlayerFilterType === 'Distance') {
        this.teamsSelectedPlayers.home = await this.triggerRequestRelevantPlayersByDistance(gameDataId,
            "home", startFrame, endFrame, this.filterPlayerDistance);
        this.teamsSelectedPlayers.away = await this.triggerRequestRelevantPlayersByDistance(gameDataId,
            "away", startFrame, endFrame, this.filterPlayerDistance);
      } else if (this.selectedPlayerFilterType === 'Participation') {
        this.teamsSelectedPlayers.home = [];
        this.teamsSelectedPlayers.away = [];
        const filteredPlayers =
            await this.triggerRequestRelevantPlayersByPassParticipation(gameDataId, startFrame, endFrame);
        const homeTeam = this.teamsPlayerOptions.home;
        const awayTeam = this.teamsPlayerOptions.away;

        for (let i = 0; i < filteredPlayers.length; i++) {
          if (homeTeam.includes(filteredPlayers[i])) {
            this.teamsSelectedPlayers.home.push(filteredPlayers[i]);
          } else if (awayTeam.includes(filteredPlayers[i])) {
            this.teamsSelectedPlayers.away.push(filteredPlayers[i]);
          }
        }
      }

      this.eventGlyphsToDisplay = [];
      this.renderGameParameters.trackingData = partialGameData;
      this.renderGameParameters.teamsPlayers = teamsPlayers;
      this.renderGameParameters.selectedEntities = this.teamsSelectedPlayers;
      this.renderGameParameters.eventsToDisplay = this.eventsToDisplay;
      this.renderGameParameters.frameOffset = startFrame;
      this.renderGameParameters.animate = animate;
      this.renderGameParameters.eventGlyphs = this.eventGlyphsToDisplay;
      this.renderGameParameters.eventGlyphsFilter = this.selectedEventGlyphs;
      this.renderGameParameters.lastIndexOfTrackingData = partialGameData.away.length - 1;
      this.renderGameParameters.currentFrame = 0;
      this.renderGame(this.renderGameParameters);
    },
    situationGlyphClicked(situationId) {
      this.triggerRenderSituation(situationId, false);
      this.situationDisplayedInCustomSituationBox = this.getSituationById(situationId);
    },

    setFilterType(filterType) {
      this.selectedPlayerFilterType = filterType;
    },
    getSituationById(id) {
      return this.situations.find(situation => situation.id === id);
    },
    filterSituations(situations) {
      const filtered = [];
      for (let situation of situations) {
        const isInSelectedTeams = this.situationFilter.selectedTeams.includes(situation.team.toLowerCase());
        const isInSelectedSituations = this.situationFilter.selectedSituations.includes(situation.kind);
        if (isInSelectedSituations && isInSelectedTeams) {
          filtered.push(situation)
        }
      }
      return filtered;
    },
    updateSituationFilter(situationFilter) {
      this.situationFilter = situationFilter;
    },
    updateSelectedEventGlyphs(selected) {
      if (this.selectedEventGlyphs.includes(selected)) {
        this.selectedEventGlyphs = this.selectedEventGlyphs.filter(currentTeam => currentTeam !== selected);
      } else {
        this.selectedEventGlyphs = [...this.selectedEventGlyphs, selected];
      }
    },
    setPlayerGlyphsToEventFrameAndRerender(targetFrame) {
      this.triggerRenderSituation(this.displayedSituationId, false, targetFrame);
    },
    renderGame(renderParameters) {
      this.animationLengthInFrames = renderParameters.lastIndexOfTrackingData;
      this.currentlyDisplayedAbsoluteFrame = renderParameters.lastIndexOfTrackingData + renderParameters.frameOffset;

      if (renderParameters.lastIndexOfTrackingData <= 0 || renderParameters.selectedEntities.length <= 0) {
        return;
      }
      this.p5canvas.prolonged?.remove();

      const renderProlongedCanvasElements = function (p5) {
        const drawPlayerLines = (entities, currentCoordinatesAway, nextCoordinatesAway,
                                 strokeColor, strokeWeight) => {
          p5.strokeWeight(strokeWeight);
          p5.stroke(strokeColor);
          DrawAndRenderFunctions.drawPlayerLines(entities, currentCoordinatesAway, nextCoordinatesAway, p5);
        };
        const drawBallLine = (currentCoordinatesHome, nextCoordinatesHome, strokeColor, strokeWeight) => {
          p5.stroke(strokeColor);
          p5.strokeWeight(strokeWeight);
          DrawAndRenderFunctions.drawBallLine(currentCoordinatesHome, nextCoordinatesHome, p5);
        }

        p5.setup = () => {
          p5.createCanvas(840 + 50, 544 + 50);
          if (renderParameters.animate) {
            p5.loop();
          } else {
            p5.noLoop();
          }
          p5.frameRate(25);
        };

        const drawCompleteSituation = () => {
          const away = renderParameters.trackingData.away;
          const home = renderParameters.trackingData.home;
          const selectedEntities = renderParameters.selectedEntities;

          for (let currentFrame = 0; currentFrame < renderParameters.lastIndexOfTrackingData; currentFrame++) {
            const opacity = Math.max(0, Math.floor(255 * currentFrame / (renderParameters.lastIndexOfTrackingData + 1)));
            const currentCoordinatesAway = away[currentFrame].coordinates;
            const nextCoordinatesAway = away[currentFrame + 1].coordinates;
            const currentCoordinatesHome = home[currentFrame].coordinates;
            const nextCoordinatesHome = home[currentFrame + 1].coordinates;
            if (!renderParameters.noTrails) {
              drawPlayerLines(selectedEntities.away, currentCoordinatesAway, nextCoordinatesAway,
                  p5.color(253, 161, 13, opacity), 3);
              drawPlayerLines(selectedEntities.home, currentCoordinatesHome, nextCoordinatesHome,
                  p5.color(20, 32, 62, opacity), 3);
            }
            drawBallLine(currentCoordinatesHome, nextCoordinatesHome, 255, 1);
            GlyphHandler.addEventGlyphs(renderParameters.eventGlyphs, renderParameters.eventsToDisplay,
                currentFrame + renderParameters.frameOffset - 1, renderParameters.eventGlyphsFilter);
          }
          GlyphHandler.addPlayerGlyphs(renderParameters.eventGlyphs,
              away[renderParameters.lastIndexOfTrackingData].coordinates,
              home[renderParameters.lastIndexOfTrackingData].coordinates,
              renderParameters.teamsPlayers, selectedEntities);
        };


        const drawAnimatedSituation = () => {
          if (renderParameters.currentFrame > renderParameters.lastIndexOfTrackingData) {
            p5.noLoop();
            this.isAnimationRunning = false;
          }

          const currentFrame = renderParameters.currentFrame;
          const away = renderParameters.trackingData.away;
          const home = renderParameters.trackingData.home;
          const opacity = Math.max(25, Math.floor(255 * currentFrame / (renderParameters.lastIndexOfTrackingData + 1)));
          const currentCoordinatesAway = away[currentFrame].coordinates;
          const nextCoordinatesAway = away[currentFrame + 1].coordinates;
          const currentCoordinatesHome = home[currentFrame].coordinates;
          const nextCoordinatesHome = home[currentFrame + 1].coordinates;
          const selectedEntities = renderParameters.selectedEntities;

          this.eventGlyphsToDisplay = this.filterEventGlyphs(renderParameters.eventGlyphs);
          renderParameters.eventGlyphs = this.eventGlyphsToDisplay;

          if (!renderParameters.noTrails) {
            drawPlayerLines(selectedEntities.away, currentCoordinatesAway, nextCoordinatesAway,
                p5.color(253, 161, 13, opacity), 3);
            drawPlayerLines(selectedEntities.home, currentCoordinatesHome, nextCoordinatesHome,
                p5.color(20, 32, 62, opacity), 3);
          }
          drawBallLine(currentCoordinatesHome, nextCoordinatesHome, 255, 1);

          GlyphHandler.addEventGlyphs(renderParameters.eventGlyphs, renderParameters.eventsToDisplay,
              currentFrame + renderParameters.frameOffset - 1, renderParameters.eventGlyphsFilter);

          GlyphHandler.addPlayerGlyphs(renderParameters.eventGlyphs,
              nextCoordinatesAway,
              nextCoordinatesHome,
              renderParameters.teamsPlayers, selectedEntities);
          renderParameters.currentFrame++;
          this.currentlyDisplayedRelativeFrame = renderParameters.currentFrame;
        }
        if (renderParameters.animate) {
          p5.draw = drawAnimatedSituation;
          this.isAnimationRunning = true;
        } else {
          p5.draw = drawCompleteSituation;
        }
      };
      this.p5canvas.prolonged = new p5(renderProlongedCanvasElements.bind(this), "canvas-prolonged");
    },
    filterEventGlyphs(events) {
      return events.filter(event => !event.labelText || event.labelText === "");
    },
    getPlayersOf(frameElement) {
      return [...frameElement.coordinates.keys()].filter(key => key !== 'Ball');
    },
    addCustomSituation(newCustomSituation) {
      this.situations = [...this.situations, newCustomSituation];
      this.filteredSituations = this.filterSituations(this.situations);
    },
    removeSituation(situationToRemove) {
      this.situationDisplayedInCustomSituationBox = null;
      this.situations = this.situations.filter(situation => situation.id !== situationToRemove.id);
      this.filteredSituations = this.filterSituations(this.situations);
    },
  }
  ,
  computed: {},
  watch: {
    currentlyDisplayedAbsoluteFrame(newValue, oldValue) {
      this.gameDataService.currentlyDisplayedAbsoluteFrame = newValue;
    },
    gameData() {
      if (!this.gameData?.trackingAway || !this.gameData?.trackingHome) {
        return;
      }
      this.gameDataService.setCurrentlySelectedGameData(this.gameData);
      const away = this.gameData.trackingAway;
      const home = this.gameData.trackingHome;
      let awayPlayers = [];
      let homePlayers = [];
      if (away && away.length > 0) {
        awayPlayers = this.getPlayersOf(away[0]);
      }
      if (home && home.length > 0) {
        homePlayers = this.getPlayersOf(home[0]);
      }
      this.teamsPlayerOptions = {
        away: awayPlayers,
        home: homePlayers
      }
      this.$store.commit('updateSelectedGameDataSet', this.gameData.id);
      this.$store.commit('updateGameData', this.gameData);
    },
    situationFilter() {
      this.filteredSituations = this.filterSituations(this.situations);
      let trajectoriesStoreObject = this.$store.getters.trajectories;
      trajectoriesStoreObject = {
        ...trajectoriesStoreObject,
        situationFilter: this.situationFilter
      };
      this.$store.commit('updateTrajectories', trajectoriesStoreObject);
    },
    situations() {
      this.updateSituationFilter(this.situationFilter)
      let trajectoriesStoreObject = this.$store.getters.trajectories;
      trajectoriesStoreObject = {...trajectoriesStoreObject, situations: this.situations};
      this.$store.commit('updateTrajectories', trajectoriesStoreObject);
    },
    eventsToDisplay() {
      let trajectoriesStoreObject = this.$store.getters.trajectories;
      trajectoriesStoreObject = {...trajectoriesStoreObject, eventsToDisplay: this.eventsToDisplay};
      this.$store.commit('updateTrajectories', trajectoriesStoreObject);
    },
    eventGlyphsToDisplay() {
      let trajectoriesStoreObject = this.$store.getters.trajectories;
      trajectoriesStoreObject = {...trajectoriesStoreObject, eventGlyphsToDisplay: this.eventGlyphsToDisplay};
      this.$store.commit('updateTrajectories', trajectoriesStoreObject);
    },
    teamsSelectedPlayers() {
      let trajectoriesStoreObject = this.$store.getters.trajectories;
      trajectoriesStoreObject = {...trajectoriesStoreObject, teamsSelectedPlayers: this.teamsSelectedPlayers};
      this.$store.commit('updateTrajectories', trajectoriesStoreObject);
    },
    teamsPlayerOptions() {
      let trajectoriesStoreObject = this.$store.getters.trajectories;
      trajectoriesStoreObject = {...trajectoriesStoreObject, teamsPlayerOptions: this.teamsPlayerOptions};
      this.$store.commit('updateTrajectories', trajectoriesStoreObject);
    },
    displayedSituationIndex() {
      let trajectoriesStoreObject = this.$store.getters.trajectories;
      trajectoriesStoreObject = {...trajectoriesStoreObject, displayedSituationIndex: this.displayedSituationId};
      trajectoriesStoreObject = {...trajectoriesStoreObject, teamsSelectedPlayers: this.teamsSelectedPlayers};
      this.$store.commit('updateTrajectories', trajectoriesStoreObject);
    }
  },
}
;
</script>

<style lang="scss" scoped>

.component-wrapper {

  .loading-hint-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: -15px;
    margin-right: -15px;
    height: 30px;
    border-radius: 5px;
    color: #E5E5E5;

    @keyframes loading {
      0% {
        background-image: url("../assets/animations/loading_1.svg")
      }
      13% {
        background-image: url("../assets/animations/loading_2.svg")
      }
      26% {
        background-image: url("../assets/animations/loading_3.svg")
      }
      40% {
        background-image: url("../assets/animations/loading_4.svg")
      }
      55% {
        background-image: url("../assets/animations/loading_5.svg")
      }
      70% {
        background-image: url("../assets/animations/loading_6.svg")
      }
      85% {
        background-image: url("../assets/animations/loading_7.svg")
      }
      100% {
        background-image: url("../assets/animations/loading_8.svg")
      }
    }

    .loading-hint {
      width: 35px;
      height: 35px;
      background-size: 100% auto;
      animation-name: loading;
      animation-duration: 2s;
      animation-iteration-count: infinite;
    }
  }

  .trajectory-main-wrapper {
    display: grid;
    grid-template:
    "top_panel top_panel right_panel"
    "left_panel soccer_field right_panel" (68 * 8px)+50
    "left_panel bottom_panel bottom_right_panel" / auto 900px auto;
    flex-direction: column;
    margin: 15px;

    .top-panel {
      grid-area: top_panel;
      display: flex;
      flex-direction: row;
      margin: 15px;

      .select-game-data-dropdown {
        position: relative;
        display: inline-block;
        font-size: 9pt;
        margin-right: 15px;
        margin-left: -5px;

        &:hover {
          .dropdown-content {
            display: block;
          }

          .dropdown-button {
            background-color: #333333;
          }
        }

        .dropdown-button {
          background-color: #333333;
          color: #e5e5e5;
          padding: 16px;
          border: none;
          cursor: pointer;
        }

        .dropdown-content {
          display: none;
          position: absolute;
          background-color: #e5e5e5;
          box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
          z-index: 1;

          .game-data-option {
            color: #333333;
            padding: 12px 16px;
            text-decoration: none;
            display: block;

            &:hover {
              background-color: #ffffff;
            }
          }
        }
      }

      .top-buttons {
        margin-right: 10px;
      }
    }

    .left-panel-wrapper {
      grid-area: left_panel;
      display: flex;
      flex-direction: column;
      margin: 0 10px;
      row-gap: 10px;

      .player-filter-options {
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
          background: #e5e5e5;
          color: #333333;
        }

        .selected {
          @extend .options;
          background: #333333;
          color: #e5e5e5;
          box-shadow: none;
        }

      }
    }

    .right-panel {
      grid-area: right_panel;
      display: flex;
      flex-direction: column-reverse;
      user-select: none; /* supported by Chrome and Opera */
      -webkit-user-select: none; /* Safari */
      -moz-user-select: none; /* Firefox */
      -ms-user-select: none; /* Internet Explorer/Edge */

      .event-glyph-selection-container {
        display: flex;
        background: #333333;
        flex-wrap: wrap;
        max-width: 340px;
        margin-bottom: 10px;
        color: #E5E5E5;

        .tile-button {
          display: flex;
          text-align: center;
          align-items: center;
          margin: 5px;
          word-spacing: 1pt;
          font-size: 9pt;
          padding: 8px;
          background: #333333;
          border-radius: 5px;
          border-right: 1px solid #262626;
          border-bottom: 1px solid #262626;
          box-shadow: inset rgba(229, 229, 229, 0.46) 2px 1px 0 1px;
        }

        .tile-button-selected {
          @extend .tile-button;
          background: #414141;
          border-radius: 5px;
          border-left: 1px solid #262626;
          border-top: 1px solid #262626;
          border-right: none;
          border-bottom: none;
          box-shadow: rgba(229, 229, 229, 0.25) 2px 1px 0 1px;
        }

      }

    }

    .display-wrapper {
      grid-area: soccer_field;
      position: relative;
      background-color: #333333;
      display: flex;
      justify-content: center;
      align-items: center;
      width: (105 * 8px)+50;
      height: (68 * 8px)+50;

      .soccer-field-container {
        position: absolute;
        z-index: 0;
        width: 105 * 8px;
        height: 68 * 8px;
        background-image: url("../assets/soccer_field.svg");
        background-size: 100% auto;
      }

      .trajectory-canvas-container {
        position: absolute;
        width: (105 * 8px)+50;
        height: (68 * 8px)+50;
      }

      .glyph-overlay-wrapper {
        position: absolute;
        width: (105 * 8px)+50;
        height: (68 * 8px)+50;
      }
    }

    .bottom-panel {
      grid-area: bottom_panel;
      display: flex;
      justify-content: left;
    }

  }

}
</style>