<template>
  <div class="heatmap-main-wrapper">
    <div class="left-panel-wrapper">
      <div class="team-label">
        <span class="label-away">Away</span>
        <span class="label-home">Home</span>
      </div>
      <player-selection
        :teams-options="teamsPlayerOptions"
        :selected-players="teamsSelectedPlayers"
      ></player-selection>
    </div>
    <div class="top-panel">
      <select
        name="DataSet"
        @click="selectedEvent = null"
        @change="changeDataSet(dataSetId)"
        v-model="dataSetId"
        class="button-custom"
      >
        <option value="null" selected disabled>Select sample data</option>
        <option
          v-for="item in dataSetOptions"
          v-bind:key="item.value"
          v-bind:value="item.value"
        >
          {{ item.text }}
        </option>
      </select>
      <select
        name="EventType"
        v-show="dataSetIdNotNull"
        @change="changeEventType(selectedEvent)"
        class="button-custom"
        v-model="selectedEvent"
      >
        <option value="null" selected disabled>Select an event type</option>
        <option
          v-for="item in eventOptions"
          v-bind:key="item.value"
          v-bind:value="item.value"
        >
          {{ item.text }}
        </option>
      </select>
      <select
        name="Team"
        v-show="eventNotNull"
        @change="changeTeam(selectedTeam)"
        class="button-custom"
        v-model="selectedTeam"
      >
        <option value="null" selected disabled>Select a team</option>
        <option
          v-for="item in teamOptions"
          v-bind:key="item.value"
          v-bind:value="item.value"
        >
          {{ item.text }}
        </option>
      </select>
      <input
        v-show="eventAndTeamNotNull"
        @click="requestEventAttributes(this.selectedEvent, this.selectedTeam)"
        type="button"
        value="Request data"
        class="button-custom"
      />
      <input
        v-show="eventAttributesReceived"
        @click="
          $refs.parallelCoordinatesChildComponent.displayParallelCoordinates()
        "
        type="button"
        value="Parallele Koordinaten"
        class="button-custom"
      />
      <input
        v-show="showRenderButton"
        @click="displayHeatmap()"
        type="button"
        value="Render Heatmap"
        class="button-custom"
      />
    </div>
    <div class="heatmap-control-sliders">
      <heatmap-sliders :labelName="this.weightName"    :value="this.hmWeight"     :min="0" :max="100" @sliderChanged="this.weightChanged"     v-show="showRenderButton" ></heatmap-sliders>
      <heatmap-sliders :labelName="this.bandwidthName" :value="this.hmBandwidth"  :min="0" :max="100" @sliderChanged="this.bandwidthChanged"  v-show="showRenderButton" ></heatmap-sliders>
      <heatmap-sliders :labelName="this.thresholdName" :value="this.hmThreshold"  :min="0" :max="100" @sliderChanged="this.thresholdChanged"  v-show="showRenderButton" ></heatmap-sliders>
    </div>
    <div class="soccer-field-heatmap-wrapper">
      <div class="soccer-field-container"></div>
      <div id="heatmap" class="heatmap-d3-container"></div>
    </div>
    <div class="parallel-coordinate-wrapper">
      <parallel-coordinates
        @selectionConfirmed="getDataForSelectedEvents"
        ref="parallelCoordinatesChildComponent"
        :eventAttributes="this.eventAttributes"
      />
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import PlayerSelection from "./PlayerSelection.vue";
import ParallelCoordinates from "./ParallelCoordinates.vue";
import HeatmapSliders from "./HeatmapSliders.vue";


export default {
  components: { PlayerSelection, ParallelCoordinates, HeatmapSliders },
  name: "Heatmap",
  props: [],
  data() {
    return {
      weightName: "Weight",
      bandwidthName: "Bandwidth",
      thresholdName: "Threshold",
      hmWeight: 0,
      hmBandwidth: 0,
      hmThreshold: 0,
      gameData: null,
      shotsOnTarget: null,
      showRenderButton: false,
      dataSetId: null,
      dataSetIdNotNull: false,
      dataSetOptions: [
        { text: "Sample Game 1", value: "sample_game_1" },
        { text: "Sample Game 2", value: "sample_game_2" },
      ],
      eventAttributes: [],
      eventAttributesReceived: false,
      positionData: [],
      positionDataHome: [],
      positionDataAway: [],
      positionDataReceived: false,
      selectedEvents: [],
      selectedEvent: "",
      selectedTeam: "",
      eventNotNull: false,
      eventAndTeamNotNull: false,
      teamOptions: [
        { text: "Home", value: "Home" },
        { text: "Away", value: "Away" },
      ],
      eventOptions: [{ text: "Shots", value: "shot" }, { text: "Free kicks", value: "freekick" },{ text: "Corners", value: "corner" },{ text: "Throw ins", value: "throwin" },{ text: "Kick offs", value: "kickoff" }],
      heatMapExists: false, // Has a Heatmap been generated
      teamsSelectedPlayers: {
        away: [],
        home: [],
      },
      teamsPlayerOptions: {
        away: [
          "Player25",
          "Player15",
          "Player16",
          "Player17",
          "Player18",
          "Player19",
          "Player20",
          "Player21",
          "Player22",
          "Player23",
          "Player24",
          "Player26",
          "Player27",
          "Player28",
        ],
        home: [
          "Player11",
          "Player1",
          "Player2",
          "Player3",
          "Player4",
          "Player5",
          "Player6",
          "Player7",
          "Player8",
          "Player9",
          "Player10",
          "Player12",
          "Player13",
          "Player14",
        ],
      },
    };
  },
  watch: {},
  methods: {
    weightChanged(weight) {
      this.hmWeight = weight;
      this.displayHeatmap();
    },
    bandwidthChanged(bandwidth) {
      this.hmBandwidth = bandwidth;
      this.displayHeatmap();
    },
    thresholdChanged(threshold) {
      this.hmThreshold = threshold;
      this.displayHeatmap();
    },

    async changeDataSet(dataSet) {
      this.dataSetIdNotNull = false;
      this.showRenderButton = false;
      this.eventAttributesReceived = false;
      this.dataSetId = dataSet;
      if (this.dataSetId != null) {
        this.dataSetIdNotNull = true;
      }
    },

    async changeEventType(eventType) {
      this.showRenderButton = false;
      this.eventAttributesReceived = false;
      this.selectedEvent = eventType;
      if (this.selectedEvent != null) {
        this.eventNotNull = true;
      }
    },

    async changeTeam(team) {
      this.showRenderButton = false;
      this.eventAttributesReceived = false;
      this.selectedTeam = team;
      if (this.selectedTeam != null && this.selectedEvent != null) {
        this.eventAndTeamNotNull = true;
      }
    },

    async requestEventAttributes(selectedEvents, selectedTeam) {
      this.eventAttributesReceived = false;
      var eventType = selectedEvents;
      var dataSetId = this.dataSetId;
      this.selectedTeam = selectedTeam;
      const gResponse = await fetch(
        `http://localhost:5000/get-event-attributes/${dataSetId}$${eventType}$${selectedTeam}`
      );
      this.eventAttributes = await gResponse.json();
      this.eventAttributesReceived = true;
    },

    async getDataForSelectedEvents(selectedEvents) {
      this.positionDataReceived = false;
      const eventCount = selectedEvents.length;
      if (eventCount != 0) {
        var selectedFrames = [];
        for (var i of Array(eventCount).keys()) {
          selectedFrames.push(selectedEvents[i].frame);
        }
        this.positionData = await this.requestPositionData(
          this.dataSetId,
          selectedFrames
        );
        this.positionDataReceived = true;
        this.showRenderButton = true;
      }
    },

    async requestPositionData(dataSetId, frames) {
      const gResponse = await fetch(
        `http://localhost:5000/get-position-data/${dataSetId}$${frames}`
      );
      return gResponse.json();
    },

    async requestBasicData(dataSetId) {
      const gResponse = await fetch(
        `http://localhost:5000/get-basic-game-data/${dataSetId}`
      );
      this.gameData = await gResponse.json();
    },

    async requestShotsOnTarget(dataSetId) {
      const gResponse = await fetch(
        `http://localhost:5000//get-shots-on-target/${dataSetId}`
      );
      this.shotsOnTarget = await gResponse.json();
    },

    async displayHeatmap() {
      var filteredDataHome = [];
      var filteredDataAway = [];
      if (this.positionDataReceived) {
        this.positionDataHome = this.positionData[0];
        this.positionDataAway = this.positionData[1];
        filteredDataHome = this.filterPlayersHome();
        filteredDataAway = this.filterPlayersAway();
      } else {
        console.error("Position Data not available!");
      }

      // Generate new Heatmap if it does not exist
      if (!this.heatMapExists) {
        this.generateHeatMap(filteredDataHome, filteredDataAway);
        this.heatMapExists = true;
      }
      // Delete and replace Heatmap if it already exists
      else {
        d3.select("#heatmap").selectAll("svg").remove();
        this.generateHeatMap(filteredDataHome, filteredDataAway);
      }
    },

    filterPlayersHome() {
      var homeData = this.positionData[0];
      var data = [];
      for (var i of Array(homeData.length).keys()) {
        Object.entries(homeData[i]).forEach(([key, value]) => {
          if (this.teamsSelectedPlayers.home.includes(key) && key != "Ball") {
            data.push({
              playerId: `${key}`,
              team: "Home",
              x: `${value.x}`,
              y: `${value.y}`,
            });
          }
        });
      }
      return data;
    },

    filterPlayersAway() {
      var awayData = this.positionData[1];
      var data = [];
      for (var j of Array(awayData.length).keys()) {
        Object.entries(awayData[j]).forEach(([key, value]) => {
          if (this.teamsSelectedPlayers.away.includes(key) && key != "Ball") {
            data.push({
              playerId: `${key}`,
              team: "Away",
              x: `${value.x}`,
              y: `${value.y}`,
            });
          }
        });
      }
      return data;
    },

    generateHeatMap(pDataHome, pDataAway) {
      // set the dimensions and margins of the graph
      var margin = { top: 10, right: 30, bottom: 30, left: 40 },
        width = 105 * 8,
        height = 68 * 8;
  
      var chosenDataHome = pDataHome;
      var chosenDataAway = pDataAway;

      // append the svg object to the body of the page
      var svg = d3
        .select("#heatmap")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      // Add X axis
      var x = d3.scaleLinear().domain([0, 1]).range([0, width]);
      svg
        .append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

      // Add Y axis
      var y = d3.scaleLinear().domain([0, 1]).range([height, 0]);
      svg.append("g").call(d3.axisLeft(y));

      // Prepare a color palette
      var color = d3
        .scaleSequential()
        .domain([0, 0.1]) // Points per square pixel.
        .range(["#0073cf", "#0073cf"]);
      
      var colorAway = d3
        .scaleSequential()
        .domain([0, 0.1]) // Points per square pixel.
        .range(["red", "red" ]);

      var densityData = d3
        .contourDensity()
        .x(function (d) {
          return x(d.x);
        })
        .y(function (d) {
          return y(d.y);
        })
        .size([width, height])
        .weight(this.hmWeight) //40
        .bandwidth(this.hmBandwidth) //30
        .thresholds(this.hmThreshold)(
        chosenDataHome
      );

      var densityDataAway = d3
        .contourDensity()
        .x(function (d) {
          return x(d.x);
        })
        .y(function (d) {
          return y(d.y);
        })
        .size([width, height])
        .weight(this.hmWeight)
        .bandwidth(this.hmBandwidth) 
        .thresholds(this.hmThreshold)(
        chosenDataAway
      );

      // show the shape!
      svg
        .selectAll("pathHome")
        .data(densityData)
        .enter()
        .append("path")
        .attr("d", d3.geoPath())
        .style("opacity", ".03")
        .attr("fill", function (d) {
          return color(d.value);
        })
        .attr("stroke", "#69b3a2")
        .attr("stroke-linejoin", "round");
      
      svg
        .selectAll("pathAway")
        .data(densityDataAway)
        .enter()
        .append("path")
        .attr("d", d3.geoPath())
        .style("opacity", ".03")
        .attr("fill", function (d) {
          return colorAway(d.value);
        })
        .attr("stroke", "#69b3a2")
        .attr("stroke-linejoin", "round");

      // Add player locations
      svg
        .append("g")
        .selectAll("circle")
        .data(chosenDataHome)
        .join("circle")
        .attr("cx", (d) => x(d.x))
        .attr("cy", (d) => y(d.y))
        .attr("r", 2)
        .attr("stroke", "white")
        .attr("fill", function (d) {
          return d.team == "Home" ? "#14203E" : "#FCA311";
        })
        .on("mouseover", handleMouseOver)
        .on("mousemove", handleMouseMove)
        .on("mouseout", handleMouseOut);
      
      svg
        .append("g")
        .selectAll("circle")
        .data(chosenDataAway)
        .join("circle")
        .attr("cx", (d) => x(d.x))
        .attr("cy", (d) => y(d.y))
        .attr("r", 2)
        .attr("stroke", "white")
        .attr("fill", function (d) {
          return d.team == "Home" ? "#14203E" : "#FCA311";
        })
        .on("mouseover", handleMouseOver)
        .on("mousemove", handleMouseMove)
        .on("mouseout", handleMouseOut);

      // Add tooltip to div element
      var tooltip = d3
        .select("#heatmap")
        .append("div")
        .style("position", "absolute")
        .style("visibility", "hidden")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "0px")
        .style("border-radius", "5px")
        .style("padding", "20px")
        .style("box-shadow", "2px 2px 20px")
        .style("opacity", "0.9")
        .attr("id", "tooltip");

      function handleMouseOver(event, d) {
        d3.select(this).attr("stroke", "grey");
        tooltip.style("visibility", "visible");
      }

      function handleMouseMove(event, d) {
        tooltip
          .style("top", event.pageY - 300 + "px")
          .style("left", event.pageX - 290 + "px")
          .html(
            "Id: " +
              d.playerId +
              "<br> Team: " +
              d.team +
              "<br> Pos: " +
              d.x +
              " , " +
              d.y
          ); 
      }

      function handleMouseOut(event, d) {
        d3.select(this).attr("stroke", "white");
        tooltip.style("visibility", "hidden");
      }
    },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.heatmap-main-wrapper {
  display: grid;
  grid-template:
    "top_panel top_panel "
    "player_select soccer_field"
    ". parallel_coords";
  flex-direction: column;
  margin: 15px;
  
  .top-panel {
    grid-area: top_panel;
    display: flex;
    flex-direction: row;
    margin: 15px;

    .button-custom {
      position: relative;
      background-color: #153b44;
      border: none;
      margin: 9px;
      font-size: 14px;
      font-family: "Montserrat";
      color: #ffffff;
      padding: 10px 13px;
      text-align: center;
      -webkit-transition-duration: 0.4s; /* Safari */
      transition-duration: 0.4s;
      text-decoration: none;
      overflow: hidden;
      cursor: pointer;
      border-radius: 20px;

    }

    .button-custom:hover {
      background-color: #2d6e7e;
      box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24),
        0 17px 50px 0 rgba(0, 0, 0, 0.19);
    }
  }

  .left-panel-wrapper {
    grid-area: player_select;
    display: flex;
    flex-direction: column;
    background-color: #313131;
    margin: 2px 4px 4px 2px;
    padding: 4px 4px;
    border-radius: 20px;

    .team-label {
      display: flex;
      flex-direction: row;
      justify-content: space-around;

      .label-away {
        margin: 9px;
        padding: 4px 4px;
        font-size: 16px;
        font-family: "Montserrat";
        text-align: center;
        background-color:  #FCA311;
        border-radius: 7px;
      }

      .label-home {
        margin: 9px;
        padding: 4px 4px;
        font-size: 16px;
        font-family: "Montserrat";
        color: #E5E5E5;
        text-align: center;
        background-color: #14203E;
        border-radius: 7px;
      }
    }
  }

  .soccer-field-heatmap-wrapper {
    grid-area: soccer_field;
    position: relative;
    background-color: #313131;
    padding: 8px 8px;
    margin: 2px 4px 4px 4px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50 + 105 * 8px;
    height: 50 + 68 * 8px;
    border-radius: 20px;

    .soccer-field-container {
      position: absolute;
      /*       left: 100px;
      top: 100px; */
      z-index: 0;
      width: 105 * 8px;
      height: 68 * 8px;
      background-image: url("../assets/soccer_field.svg");
      background-size: 100% auto;
    }

    .heatmap-d3-container {
      position: absolute;
      /*       left: 100px;
      top: 100px; */
      z-index: 1;
      width: 105 * 8px;
      height: 68 * 8px;
    }
  }

  .parallel-coordinate-wrapper {
    grid-area: parallel_coords;
    display: flex;
    flex-direction: column;
    background-color: #313131;
    padding: 8px;
    margin: 4px 4px 2px 4px;
    border-radius: 20px;
    width: 50 + 105 * 8px;
    height: 50 + 68 * 8px;
    align-items: center;
  }
}
</style>