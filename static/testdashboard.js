var users = {};
$(document).ready(function(){
		var get = function(cb){
			$.get('/gamestatus/' + gameName, cb);
		}

		var init = function(){
			get(function(data){
					var dataed = JSON.parse(data);
					users = dataed.aliveUsers;
					deadusers = dataed.deadUsers;
					$body = $('body');
					for(var i = 0; i < users.length; i++){
						var user = users[i];
						addUser(user, false);
					}

					for(var i = 0; i < deadusers.length; i++){
						var user = deadusers[i];
						addUser(user, true);
					}
				});
		}
		
		var addUser = function(user, isDead){
			var textBox = $('<input type="text"/>');
			var submitButton = $('<button>Send</button>');
			submitButton.click(function(){
					if (textBox.length != 0){
						var body = textBox.val();
						$.post('/kill/', {Body: body, From: user.number}, function(data){
								document.location.reload(true);
							});
						console.log(textBox.val());
						textBox.val("");
					}
				});
			if(!isDead){
				$body.append($('<h1>' + user.name + " " + user.number + '</h1>'));
			} else {
				$body.append($('<h1>' + '<s>' + user.name + "</s" + user.number + '</h1>'));
			}
			$body.append($('<textarea cols=60 rows=10>' + user.messages.join('\n') + '</textarea>'));
			$body.append($('<br/>'));
			$body.append(textBox);
			$body.append(submitButton);
		}

		init();
	});