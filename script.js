$(document).ready(function() {
	$("#nappi").click(function(){
		$("#sailio1").fadeOut();
		$("#sailio3").fadeIn();
	});
	
	$("#ostonappi").click(function(){
		$("#sailio3").fadeOut();
		$("#sailio2").fadeIn();
	});
});