$(document).ready(function(){
	$('#dateOfBirth').datepicker();
	$("#formRegister").click(function(e){
		if ($("#password_confirmation").val() != $("#password").val()){
			alert("Passwords don't watch");
			e.preventDefault();
		}	
	});
	$("#username").focus();
	$(".chosen-select").chosen({width: "95%"});

	$("#datetimepicker").datetimepicker({
		language: 'pt-BR'
	});
	$("#datetimepicker1").datetimepicker({
		language: 'pt-BR'
	});
});
