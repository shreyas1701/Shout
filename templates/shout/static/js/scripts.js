$(document).ready(function(){
	$('#dateOfBirth').datepicker();
	
	$("#username").focus();
	$(".chosen-select").chosen({width: "99%"});

	$(".date").datepicker({
	});

	$(".time").timepicker();
	$.ajaxSetup({ 
		beforeSend: function(xhr, settings) {
			function getCookie(name) {
				var cookieValue = null;
				if (document.cookie && document.cookie != '') {
				    var cookies = document.cookie.split(';');
				    for (var i = 0; i < cookies.length; i++) {
				        var cookie = jQuery.trim(cookies[i]);
				        // Does this cookie string begin with the name we want?
				        if (cookie.substring(0, name.length + 1) == (name + '=')) {
				            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				            break;
				        }
				    }
				}
				return cookieValue;
			}
			if(!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
				// Only send the token to relative URLs i.e. locally.
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		} 
	});

	notify();
	setInterval(function(){
		notify();
	},10*1000);

	

	$("#invSelct2").click(function(){
		$("#selectDiv").show();		
	});

	$("#invSelct1").click(function(){
		$("#selectDiv").hide();		
	});

	if($(".pageName").val() == "profile"){
		getshouts("profile");	
	}else if($(".pageName").val() == "home"){
		getshouts("home");
	}else{
		getshouts("hashtag");
		getEvents();
	}
	
	$(".dropdown").click(function(){
		updateSeen();
		$(".badge").hide();
	});

	$( ".shouts" ).on( "click", ".likeShout", function(e) {
		var id = $(this).attr("id")
		likeTheShout(id);
		$(this).removeClass("likeShout").addClass("likedShout");
		$(this).html('<i class="fa fa-thumbs-up" aria-hidden="true"></i>Liked');
		var text = $(this).parent().parent().find(".numLikes").html();
		if(text !== ""){
			var num = text.substring(0,text.indexOf(" "));
			var num1 = parseInt(num);
			num1++;
			text = text.replace(num,num1);
			$(this).parent().parent().find(".numLikes").html(text);
		}else{
			text = "1 person likes this!";
			$(this).parent().parent().find(".numLikes").html(text);
		}
		e.preventDefault();
	});

	$( ".shouts" ).on( "click", ".likedShout", function(e) {
		var id = $(this).attr("id")
		unLikeTheShout(id);
		$(this).removeClass("likedShout").addClass("likeShout");
		$(this).html('<i class="fa fa-thumbs-up" aria-hidden="true"></i>Like');
		var text = $(this).parent().parent().find(".numLikes").html();
		var num = text.substring(0,text.indexOf(" "));
		var num1 = parseInt(num);
		if(num1 == 1){
			text = "";
			$(this).parent().parent().find(".numLikes").html(text);
		}else{
			num1--;
			text = num1+" person likes this!";
			$(this).parent().parent().find(".numLikes").html(text);
		}
		e.preventDefault();
	});

	setTimeout(function(){
		$("#invSelct1").click();
	},500);
});

function notify(frmwh){
	$.ajax({
		url: '/notify/',
		type: 'get', 
		datatype: 'json',
		success: function(data) {
			var obj = JSON.parse(data.replace(/'/g, '"'));
			//console.log(obj);
			$(".notif").html("");
			$(".notif").html('<li style="margin-left: 10px"><p><strong>Upcoming Events</strong></p></li>');
			var seenFlag = false;
			for (var i = obj.length - 1; i >= 0; i--) {

				var bgText = "style='background:#f1f1f1'"
				if(obj[i].seen === "True"){
					notifHtml = '<li><p><a href="#">'+obj[i].notif_text+'</a></p></li>';
				}else{
					seenFlag = true;
					notifHtml = '<li><p><a href="#" '+bgText+' >'+obj[i].notif_text+'</a></p></li>';
				}
				
				$(".notif").append(notifHtml);
			}


			if(seenFlag){
				$(".badge").show();
			}else{
				$(".badge").hide();
			}
			
		},
		error: function(data) { 
			console.log("error");
			console.log(data);
		}
	});
}

function updateSeen() {
	$.ajax({
		url: '/updateSeen/',
		type: 'get', 
		datatype: 'json',
		success: function(data) {
			console.log(data);
		},
		error: function(data) { 
			console.log('Got an error dude');
			console.log(data);
		}
	});
}

function getshouts(location){
	//console.log(location);
	var dataObj = {
		location: ""+location,
	};

	if(location == "hashtag"){
		dataObj = {
			location: ""+location,
			hashText: ""+$("#hashText").val()
		};
	}else if(location == "profile"){
		dataObj = {
			location: ""+location,
			userId: ""+$("#profLId").val()
		};
	}
	

	$.ajax({
		url: '/getShouts/',
		type: 'post', 
		data: dataObj,
		datatype: 'json',
		success: function(data){
			//console.log(data);
			var arr = JSON.parse(data.replace(/'/g, '"'));

			var divText = "";
			if (location == "home"){
				divText = "homeShouts";	
			}else if (location == "profile"){
				divText = "profShouts";	
			}else if(location == "hashtag"){
				divText = "hashShouts";
			}

			$("#"+divText).html("");
			var shoutHtml = "";
			for (var i = 0; i < arr.length; i++) {
				var likesText = '<span class="numLikes"></span>';
				
				if(arr[i].likes > 0){
					likesText = '<span class="numLikes">'+arr[i].likes+' people like this</span>';
				}

				var shout_text = hashTag(arr[i].shout);
				var likeClass = "likeShout";
				var likeText = "Like";
				if(arr[i].liked === "True"){
					likeClass = "likedShout";
					likeText = "Liked";
				}
				shoutHtml += 	'<div class="shout">'+
								'<h4><a href="/profile/'+arr[i].user+'/">'+arr[i].username+'</a></h4>'+
								'<p class="shout_text">'+shout_text+'</p>'+
								'<p class="timestamp pull-right">'+arr[i].shout_at+'</p>'+
								'<div class="clear"></div>'+
								'<p class="licom">'+
								'<span><a id="'+arr[i].id+'" class="'+likeClass+'" href="#"><i class="fa fa-thumbs-up" aria-hidden="true"></i>'+likeText+'</a></span>&nbsp;'+
								likesText+
								'</p>'+
								'</div>';
							
			}
			$("#"+divText).html(shoutHtml);

		},
		error: function(data){
			console.log(data);
		}
	});
}

function hashTag(text) {
	var shout_text = text.replace("%", "'");
	var hashLink = "";
	var re = new RegExp("#",'gi');
	var textArr = [];
	while (re.exec(shout_text)){
		textArr.push(re.lastIndex);
	}

	if(textArr.length > 1){
		var hashArr = [];
		for (var j = 0; j < textArr.length; j++) {
			var newStr = shout_text.substring(textArr[j]-1,shout_text.length);
			if(newStr.indexOf(" ") > -1){
				hashLink = newStr.substring(0,newStr.indexOf(" "));
			}else{
				var re = new RegExp("#",'gi');
				var count = 0;
				while (re.exec(newStr)){
						count += 1;
				}
				if (count == 1){
					hashLink = newStr;	
				}
			}
			if(hashLink !== ""){
				hashArr.push(hashLink);	
			}
		}

		for (var i = 0; i < hashArr.length; i++) {
			var txt = hashArr[i];
			var symArr = [",", ".", "!", "?"]
			for (var j = symArr.length - 1; j >= 0; j--) {
				var rex = new RegExp("\\"+symArr[j], 'g');
				txt = txt.replace(rex, "")
			}

			var linkText = "<a href='/hashtag/"+txt.substring(1,txt.length)+"/'>"+txt+"</a>";
			shout_text = shout_text.replace(txt, linkText);
		}
	}else if (textArr.length == 1){
		var newStr = shout_text.substring(textArr[0]-1,shout_text.length);
		if(newStr.indexOf(" ") > -1){
			hashLink = newStr.substring(0,newStr.indexOf(" "));
		}else{
			var re = new RegExp("#",'gi');
			var count = 0;
			while (re.exec(newStr)){
					count += 1;
			}
			if (count == 1){
				hashLink = newStr;	
			}
		}
		if (hashLink !== ""){
			var symArr = [",", ".", "!", "?"]
			for (var j = symArr.length - 1; j >= 0; j--) {
				var rex = new RegExp("\\"+symArr[j], 'g');
				hashLink = hashLink.replace(rex, "");
			}
			var linkText = "<a href='/hashtag/"+hashLink.substring(1,hashLink.length)+"/'>"+hashLink+"</a>";
			shout_text = shout_text.replace(hashLink, linkText);	
		}
	}
	
	return shout_text
}

function likeTheShout(id) {
	var dataObj = {
		id: ""+id,
	};
	$.ajax({
		url: '/like/',
		type: 'post', 
		data: dataObj,
		datatype: 'json',
		success: function(data){
			console.log(data);
		},
		error:function(data){
			console.log(data);
		}
	});
}

function unLikeTheShout(id) {
	var dataObj = {
		id: ""+id,
	};
	$.ajax({
		url: '/unlike/',
		type: 'post', 
		data: dataObj,
		datatype: 'json',
		success: function(data){
			console.log(data);
		},
		error:function(data){
			console.log(data);
		}
	});
}

function getEvents(){

	
	var dataObj = {
		hashText: ""+$("#hashText").val()
	};


	$.ajax({
		url: '/getEvents/',
		type: 'post', 
		data: dataObj,
		datatype: 'json',
		success: function(data){
			var arr = JSON.parse(data.replace(/'/g, '"'));
			var eventHtml = "";
			for (var i = arr.length - 1; i >= 0; i--) {
				eventHtml += '<div class="col-md-4 box">'+
					'<h4>'+arr[i].event_name+'</h4>'+
					'<p>'+arr[i].description+'</p>'+
					'<a href="/event_info/'+arr[i].id+'/" class="btn btn-large btn-primary">See More!</a>'+
				'</div>'
			}

			$("#hashEvents").html(eventHtml);
			
		},
		error: function(data){

		}
	});
}