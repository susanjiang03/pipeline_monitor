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
  d3_fl_chart.status_properties = [
    "task_id", "name", "status", "last_run", "message", "url"
  ];

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

    var node_dims = {
      width: 180,
      height: 84,
      l_b_factor: 0.05,
      t_b_factor: 0.2
    };

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

    var clip_path = gnode.append("clipPath")
      .attr("id", function(d, i) {
        return "clip-" + i;
      })
      .append("rect")
        .attr("width", node_dims.width)
        .attr("height", node_dims.height)
        .attr("rx", 12)
        .attr("ry", 12)
        .attr("x", -node_dims.width/2)
        .attr("y", -node_dims.height/2);

    var node = gnode.append("rect")
      .attr("class", "node")
      .attr("width", node_dims.width)
      .attr("height", node_dims.height)
      .attr("rx", 12)
      .attr("ry", 12)
      .attr("x", -node_dims.width/2)
      .attr("y", -node_dims.height/2)
      .style("fill", function (d) {
        return colors[d.status]["bc"];
      })
      .style("stroke", function (d) {
        return colors[d.status]["bdc"];
      })
      .call(force.drag);

    gnode.append("g")
      .each(function (d) {
        var glabel = d3.select(this)
        .attr("clip-path", function(d, i) {
          return "url(#clip-" + i + ")";
        });

        if (d.status === "not run") {
          var text = glabel.append("text")
            .attr("class", "status");
          $.each(["task_id", "name", "status"], function (i, sp) {
            var text = glabel.append("text")
              .attr("class", "status");
            text.append("tspan")
              .attr("class", sp + " slabel")
              .attr("x", -(node_dims.width / 2) + node_dims.width * node_dims.l_b_factor)
              .attr("y", -(node_dims.height / 2) + node_dims.height * node_dims.t_b_factor + 12 * i)
              .text(sp.replace("_", " ") + ": ");

            text.append("tspan")
              .attr("class", "stext")
              .text(d[sp]);
          });
        } else {
          $.each(d3_fl_chart.status_properties, function (i, sp) {
            var text = glabel.append("text")
              .attr("class", "status");
            text.append("tspan")
              .attr("class", sp + " slabel")
              .attr("x", -(node_dims.width / 2) + node_dims.width * node_dims.l_b_factor)
              .attr("y", -(node_dims.height / 2) + node_dims.height * node_dims.t_b_factor + 12 * i)
              .text(sp.replace("_", " ") + ": ");

            if (sp === "url") {
              text.append("a")
                .attr("class", "slink")
                .attr("xlink:href", d[sp])
                .text("Task details...");
            } else if (sp === "status") {
              var inner_text = text.append("tspan")
                .attr("class", "stext status-msg")
                .text(d[sp]);
              inner_text.attr("class", function(d) {
                return "stext status-msg " + d[sp]
              });
            } else {
              text.append("tspan")
                .attr("class", "stext")
                .text(d[sp]);
            }
          });
        }
      });

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
