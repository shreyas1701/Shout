$(document).ready(function(){
	$('#dateOfBirth').datepicker();
	
	$("#username").focus();
	$(".chosen-select").chosen({width: "99%"});

	$(".date").datepicker({
	});

	$(".time").timepicker();
	notify("fromStart");
	setInterval(function(){
		notify("normal");
	},5*1000*60);
	
	$(".dropdown").click(function(){
		$(".badge").hide();
	});

});

function notify(frmwh){
	$.ajax({
		url: '/notify/',
		type: 'get', 
		datatype: 'json',
		success: function(data) {
			var prev = $(".notif li").length;

			$(".notif").html("");
			$(".notif").html('<li style="margin-left: 10px"><p><strong>Upcoming Events</strong></p></li>');
			var dataArr = data.split("{");
			for(var i=2; i<dataArr.length;i=i+2){
				var event = dataArr[i].split(",");
				st_date = event[3].split(": ")[1];
				var datsplt = st_date.split("T");
				var eventName = event[0].split(":")[1];
				eventName = eventName.replace(/['"]+/g, '');
				notifHtml = '<li><p><a href="#">'+eventName+' - '+datsplt[0].substring(datsplt[0].indexOf("-")+1)+' @ '+datsplt[1].substring(0,5)+'</a></p></li>';
				$(".notif").append(notifHtml);
			}

			var pres = $(".notif li").length;

			if(frmwh === "normal"){
				if(pres > prev){
					$(".badge").show();
				}else{
					$(".badge").hide();
				}	
			}else{
				$(".badge").hide();
			}
			
			
		},
		failure: function(data) { 
			alert('Got an error dude');
		}
	});
}