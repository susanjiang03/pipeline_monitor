/**
 * Created by jhohman on 12/1/2015.
 */
$(document).ready(function () {
    var ws = new WebSocket("ws://localhost:8081/socket");
    ws.onmessage = function(event) {
        d3_fl_chart.render(event.data);
    };
});