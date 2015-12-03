document.getElementById("addInputField").onclick=function() {
				var div = document.getElementById("UserRssInput");
				var input = document.createElement("input");
				input.type = "text";
                input.name = "userRSS[]";
                input.id = "userRSS";
				div.appendChild(document.createElement("p"));
				div.appendChild(input);
			}


document.getElementById("deleteInputField").onclick=function() {
				var div = document.getElementById("UserRssInput");
    var lastInput=div.lastElementChild;
				div.removeChild(lastInput);
}