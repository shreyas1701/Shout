$(document).ready(function(){
	$(".shout_text").keyup(function(){
		text = $(this).val();
		$(".charNum").text(text.length);
		if(text.length > 160){
			$(".charNum").css("color","red");
			$("#shoutBtn").prop('disabled',true);
		}else{
			$(".charNum").css("color","black");
			$("#shoutBtn").prop('disabled',false);
		}
	});

	$(".licom a").click(function(e){
		var id = $(this).attr("id");
		likeShout(id);
		e.preventDefault();
	});

});


function likeShout(id) {
	$.ajax({
		url: '/like/'+id,
		type: 'get', 
		datatype: 'json',
		success: function(data) {
			console.log(data);
		},
		error: function(data){
			console.log(data);
		}
	});
}
