var users = {};
$(document).ready(function(){
		var paper_width = 700;
		var paper_height = 700;
		var paper = Raphael("holder", paper_width, paper_height);
		var circles = paper.set();
		var labels = paper.set();
		var arrows = paper.set();
		
		var get = function(cb){
			$.get('/gamestatus/' + gameName, cb);
		}
		
		var init = function(){
			var circle_radius = 70;
			get(function(data){
					var dataed = JSON.parse(data);
					users = dataed.aliveUsers;
					deadusers = dataed.deadUsers;
					for(var i = 0; i < users.length; i++){
						var user = users[i];
						var circle = paper.circle(Math.random() * paper_width,
												  Math.random() * paper_height,
												  circle_radius);
						var label = paper.text(Math.random() * paper_width,
											   Math.random() * paper_height,
											   user.name);
						circles.push(circle);
						labels.push(label);
						user.circle = circle;
						user.label = label;
						circle.click(
									 (function(usr){
										 return function(){
											 for(var i = 0; i < users.length; i++){
												 if (users[i] == usr){
													 users.splice(i, 1);
														  destory_user(usr)
															  break;
												 }
											 }
										 }
									 })(user));
					}
					
					
					var destory_user = function(usr){
						usr.label.animate({opacity:0}, 4 * 1000, function(){
								usr.label.remove();
								 });
						usr.circle.animate({opacity:0}, 4 * 1000, function(){
								usr.circle.remove();
							});
						update();
					}
					
					
					circles.attr({fill: "#000", stroke: "#fff", "stroke-dasharray": "- ", opacity: .2});
					labels.attr({font: "12px Fontin-Sans, Arial", fill: "#fff", "text-anchor": "start"});
					update();

					setInterval(function(){
							get(function(data){
									new_users = JSON.parse(data).aliveUsers;
									if (new_users.length < users.length && users.length > 2){

										// look at old users and delete the ones
										// that are not in new_users
										for(var i = 0; i < users.length; i++){
											var user = users[i];
											var alive = false;
											for(var j = 0; j < new_users.length; j++){
												var new_user = new_users[j];
												if (user.number == new_user.number){
													alive = true;
												}
											}
											if (!alive){
												var dead_user = users.splice(i, 1)[0];
												destory_user(dead_user);
												break;
											}
										}
									}
								});
						}, 10 * 1000)
						});
		};

		var update = function(){
			// user is assumed to be just updated with ordered list of kill
			// all died users are destoryed before this function
			destory_arrows();
			var x_origin = paper_width / 2;
			var y_origin = paper_height / 2;
			var length = users.length;
			var radius = 250;
			for(var i = 0; i < length; i++){
				var user = users[i];
				var x_offset = radius * Math.cos(i * 2 * Math.PI / length);
				var y_offset = radius * Math.sin(i * 2 * Math.PI / length);
				var x_user_center = x_origin + x_offset;
				var y_user_center = y_origin + y_offset;
				var label_params = {x: x_user_center-20, y: y_user_center-20};
				var circle_params = {cx: x_user_center, cy: y_user_center};
				user.circle.animate(circle_params, 2 * 1000);
				user.label.animate(label_params, 2 * 1000);
				(function(){
					for(var i = 0; i < length; i++){
						var x_arrow_offset = radius * Math.cos((i+.5) * 2 * Math.PI / length) * .95;
						var y_arrow_offset = radius * Math.sin((i+.5) * 2 * Math.PI / length) * .95;
						var x_arrow_center = x_origin + x_arrow_offset;
						var y_arrow_center = y_origin + y_arrow_offset;
						var x_arrow_vect = radius * Math.cos((i+1) * 2 * Math.PI / length) * .9 - radius * Math.cos((i) * 2 * Math.PI / length) * .9;
						var y_arrow_vect = radius * Math.sin((i+1) * 2 * Math.PI / length) * .9 - radius * Math.sin((i) * 2 * Math.PI / length) * .9;
						var arrow = paper.arrow(x_arrow_center, y_arrow_center, x_arrow_vect, y_arrow_vect);
						arrows.push(arrow);
						var arrow_params = {opacity: 1};
						setTimeout((function(arrw){
									return function(){
										arrw.animate(arrow_params, 3 * 1000);
									}
								})(arrow), 3 * 1000);
					}
					arrows.attr({fill: "red", stroke: "#fff", "stroke-dasharray": "- ", opacity: .0});
				})();
			}
		};
			 
		var destory_arrows = function(){
			for(var i = 0; i < arrows.length; i++){
				var arrow = arrows[i];
				arrow.remove();
			}
			arrows = paper.set();
		};


		// vector that the arrow the towards
		Raphael.fn.arrow = function (x, y, x_vect, y_vect){
			var width = 30;
			var length = 70;
			var arrow_dist = 20;
			var commands = [ "M" + x + " " + (y + length/2),
							 "L" + (x + width/2) + " " + (y + length/2),
							 "L" + (x + width/2) + " " + (y - arrow_dist),
							 "L" + ((x + width/2) + 10) + " " + (y - arrow_dist),
							 "L" + x + " " + (y - length),
							 "L" + ((x - width/2) - 10) + " " + (y - arrow_dist),
							 "L" + (x - width/2) + " " + (y - arrow_dist),
							 "L" + (x - width/2) + " " + (y + length/2),
							 "L" + x + " " + (y + length/2)
							 ]
			var command = "";
			for(var i = 0; i < commands.length; i++){
				command += commands[i];
			}
			var path = this.path(command);
			var rotation = (180 / Math.PI) * Math.acos(x_vect / Math.sqrt(x_vect * x_vect + y_vect * y_vect));
			if( y_vect > 0 ){
					 
			} else {
				rotation = 360 - rotation;
			}
			rotation += 90;
			path.rotate(rotation);
			return path;
		}

		init();
			 
	});
