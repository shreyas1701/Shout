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

	
});
