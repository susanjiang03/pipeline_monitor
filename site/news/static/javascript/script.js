document.getElementById("addInputField").onclick=function() {
				var div = document.getElementById("UserRssInput");
				var input = document.createElement("input");
				input.type = "text";
                input.name = "userRSS[]";
                input.id = "userRSS";
				div.appendChild(document.createElement("p"));
				div.appendChild(input);
			}