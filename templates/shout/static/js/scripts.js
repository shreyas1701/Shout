$(document).ready(function(){
	$('#dateOfBirth').datepicker();
	
	$("#username").focus();
	$(".chosen-select").chosen({width: "99%"});

	$(".date").datepicker({
	});

	$(".time").timepicker();
	notify();
	
	
	setInterval(function(){
		notify();
	},10*1000);
	
	
	$(".dropdown").click(function(){
		updateSeen();
		$(".badge").hide();
	});

});

function notify(frmwh){
	$.ajax({
		url: '/notify/',
		type: 'get', 
		datatype: 'json',
		success: function(data) {
			var obj = JSON.parse(data.replace(/'/g, '"'));
			console.log(obj);
			$(".notif").html("");
			$(".notif").html('<li style="margin-left: 10px"><p><strong>Upcoming Events</strong></p></li>');
			var seenFlag = false;
			for(var i=0; i<obj.length;i++){

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
			//alert('Got an error dude');
		}
	});
}