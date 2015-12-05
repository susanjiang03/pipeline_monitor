/**
 * d3_node_chart.js
 * Script to render a d3 node chart for pipeline monitor.
 *
 * jQuery
 * d3.js
 * @author James Hohman
 * @requires jQuery 1.11.3 or later
 *
 * Copyright (c) 2015, James Hohman
 *
 */

$(document).ready(function() {
  d3_fl_chart.render();
  d3.select(window).on('resize', d3_fl_chart.render);
});


(function (d3_fl_chart, $, undefined) {
  d3_fl_chart.cached_data = {};

  d3_fl_chart.render = function(data) {
    d3_fl_chart.graph = data === undefined ? d3_fl_chart.cached_data : JSON.parse(data);
    d3_fl_chart.cached_data = d3_fl_chart.graph;

    $('#chart').empty();
    var ar = 0.5;
    var width = parseInt(d3.select('#chart').style('width'), 10);
    var height = width * ar;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-2000)
        .linkDistance(200)
        .size([width, height]);

    var svg = d3.select("#chart").append("svg")
        .attr("width", width)
        .attr("height", height);

    var colors = {
      success: {bc: "lightgreen", bdc: "darkgreen"},
      "in progress": {bc: "lightblue", bdc: "royalblue"},
      "not run": {bc: "ghostwhite", bdc: "lightblue"},
      warning: {bc: "#FFFB9F", bdc: "rgb(176, 156, 47)"},
      error: {bc: "pink", bdc: "firebrick"}
    };

    var graph = d3_fl_chart.graph;

    if ($.isEmptyObject(graph)) {
      window.svg = svg;
      svg.append("text")
        .text("Awaiting pipeline data...")
        .style("font-size", "4vw")
        .style("fill", "white")
        .attr("x", width * 0.1)
        .attr("y", height/2);
      return;
    }

    var num_nodes = d3_fl_chart.graph.nodes.length;
    var node_dims = { width: 160, height: 120 };


    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var link = svg.selectAll(".link")
        .data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke-width", function (d) {
          return Math.sqrt(d.value);
        });

    var gnode = svg.selectAll(".node")
        .data(graph.nodes)
        .enter()
        .append("g")
        .attr("class", "g-nodes");

    var node = gnode.append("rect")
        .attr("class", "node")
        .attr("width", node_dims.width)
        .attr("height", node_dims.height)
        .attr("rx", 12)
        .attr("ry", 12)
        .attr("x", -60)
        .attr("y", -40)
        .style("fill", function (d) {
          return colors[d.status]["bc"];
        })
        .style("stroke", function (d) {
          return colors[d.status]["bdc"];
        })
        .call(force.drag);

    var label = gnode.append("text")
        .attr("class", "label")
        .text(function (d) {
          return d.name;
        })
        .attr("x", -44)
        .attr("y", -10);

    var status = gnode.append("text")
        .attr("class", "status")
        .text(function (d) {
          return d.status;
        })
        .attr("x", -28)
        .attr("y", 14);

    force.on("tick", function () {
      link.attr("x1", function (d) {
            return d.source.x;
          })
          .attr("y1", function (d) {
            return d.source.y;
          })
          .attr("x2", function (d) {
            return d.target.x;
          })
          .attr("y2", function (d) {
            return d.target.y;
          });

      gnode.attr("transform", function (d) {
        return "translate(" + [d.x, d.y] + ")";
      });
    });
  };
}(window.d3_fl_chart = window.d3_fl_chart || {}, jQuery));
