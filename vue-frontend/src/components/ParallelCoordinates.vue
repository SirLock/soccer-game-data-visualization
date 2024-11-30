<template>
  <div class="parallel-coordinate-wrapper-inner">
    <div class="top-panel-wrapper">
      <input @click="returnSelectedEvents" type="button" value="Confirm Selection" v-show="this.parallelCoordinatesExist"/>
    </div>
    <div id="parallel_coords" class="parallel-coordinate-container">
    </div>
  </div>
</template>


<script>
import * as d3 from "d3";
export default {
  name: "ParallelCoordinates",
  props: ["eventAttributes"],
  data() {
    return {
      parallelCoordinatesExist: false, //Have parallel coordinates been generated
    };
  },
  watch: {},
  methods: {
    async displayParallelCoordinates() {
      if (!this.parallelCoordinatesExist) {
        this.generateParallelCoordinates();
        this.parallelCoordinatesExist = true;
      } else {
        d3.select("#parallel_coords").select("svg").remove();
        this.generateParallelCoordinates();
      }
    },

    returnSelectedEvents() {
      var svg = d3
        .select("#parallel_coords")
        .select("svg");
      this.$emit("selectionConfirmed", svg.property("value"));
    },

    generateParallelCoordinates() {
      var data = this.eventAttributes;
      var colors = d3.interpolateRdYlGn;
      var selectedKey = "time";

      var margin = { top: 30, right: 10, bottom: 30, left: 10 },
        width = 105 * 8,
        height = 68 * 8;

      var brushHeight = 50;

      var deselectedColor = "#ddd";

      var selectedLineColor = "steelblue";

      //extract keys from data object
      function d3keys(map) {
        var keys = [];
        for (var key in map) keys.push(key);
        return keys;
      }

      var keys = d3keys(data[0]).filter(function (d) {
        return d != "frame";
      });

      var x = new Map(
        Array.from(keys, (key) => [
          key,
          d3.scaleLinear(
            d3.extent(data, (d) => d[key]),
            [margin.left, width - margin.right]
          ),
        ])
      );

      var y = d3.scalePoint(keys, [margin.top, height - margin.bottom]);

      var z = d3.scaleSequential(x.get(selectedKey).domain().reverse(), colors);

      var line = d3
        .line()
        .defined(([, value]) => value != null)
        .x(([key, value]) => x.get(key)(value))
        .y(([key]) => y(key));

      const svg = d3
        .select("#parallel_coords")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      const brush = d3
        .brushX()
        .extent([
          [margin.left, -(brushHeight / 2)],
          [width - margin.right, brushHeight / 2],
        ])
        .on("start brush end", brushed);

      const path = svg
        .append("g")
        .attr("fill", "none")
        .attr("stroke-width", 2.5)
        .attr("stroke-opacity", 0.4)
        .selectAll("path")
        .data(
          data
            .slice()
            .sort((a, b) => d3.ascending(a[selectedKey], b[selectedKey]))
        )
        .join("path")
        .attr("stroke", (d) => z(d[selectedKey]))
        .attr("d", (d) => line(d3.cross(keys, [d], (key, d) => [key, d[key]])));

      path.append("title").text((d) => d.frame);

      svg
        .append("g")
        .selectAll("g")
        .data(keys)
        .join("g")
        .attr("transform", (d) => `translate(0, ${y(d)})`)
        .each(function (d) {
          d3.select(this).call(d3.axisBottom(x.get(d)));
        })
        .call((g) =>
          g
            .append("text")
            .attr("x", margin.left)
            .attr("y", -6)
            .attr("text-anchor", "start")
            .attr("fill", "currentColor")
            .text((d) => d)
        )
        .call((g) =>
          g
            .selectAll("text")
            .clone(true)
            .lower()
            .attr("fill", "none")
            .attr("stroke-width", 5)
            .attr("stroke-linejoin", "round")
            .attr("stroke", "white")
        )
        .call(brush);

      const selections = new Map();
      
      function brushed({ selection }, key) {
        if (selection === null) selections.delete(key);
        else selections.set(key, selection.map(x.get(key).invert));
        const selected = [];
        path.each(function (d) {
          const active = Array.from(selections).every(
            ([key, [min, max]]) => d[key] >= min && d[key] <= max
          );
          d3.select(this).style(
            "stroke",
            active ? z(d[selectedKey]) : deselectedColor
          );
          if (active) {
            d3.select(this).raise();
            selected.push(d);
          }
        });
        svg.property("value", selected).dispatch("input");
      }


      return svg.property("value", data).node();
    },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.parallel-coordinate-wrapper-inner {
  //grid-area: parallel_coords;
  grid-template: 
  "top_panel"
  "parallel_coordinates";
  display: flex;
  flex-direction: column;
  padding: 8px;
  

  .top-panel-wrapper {
    grid-area: top_panel;
    display: flex;
    flex-direction: row;
  }

  .parallel-coordinate-container {
    grid-area: parallel_coordinates;
    display: flex;
    flex-direction: row;
  }

}
</style>