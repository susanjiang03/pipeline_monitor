/**
 * Created by jhohman on 12/1/2015.
 */

var ws = null;

$(document).ready(function () {
    ws = new WebSocket("ws://" + window.location.hostname + ":8081/socket");
    ws.onmessage = function(event) {
        d3_fl_chart.render(event.data);
    };
});

function populate_articles() {
    ws.send("0");
    alert("Populate articles job request sent.");
}
