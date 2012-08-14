$(document).ready(function(){
		$("#add_new").click(function(){
				$('#newEntries').append($('<input type="text" class="number" id="input" /> <input type="text" class="name" id="input" /><br />'));
			});
		
		$("#submit").click(function(){
				var result = "";
				var numElements = document.getElementsByClassName("number");
				var nameElements = document.getElementsByClassName("name");
				n = numElements.length;
				for (var i = 0; i < n; i++) {
					var currNum = numElements[i].value;
					var currName = nameElements[i].value
						if(!($.trim(currNum).length === 0 && $.trim(currName).length === 0))
							result += currNum + "," + currName + "\n";
				}
				$.post("/startgame", {data: result});
			});
	});
