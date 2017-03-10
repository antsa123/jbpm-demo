const apiKey = "tu705911788977665986179742030436";

$(document).ready(function() {
	// tähän prosessin aloitus POST
	
	$("#nappi").click(function(){
		$("#sailio1").fadeOut();
		$("#sailio2").fadeIn();
		// Tähän GET skyscanner APIsta

		$.ajax({
			type: "GET",
			url: "/skyscanner",
			success: function () {

				$("#sailio2").fadeOut();
				$("#sailio3").fadeIn();
            }

		});
	});
	
	$("#ostonappi").click(function(){
		$("#sailio3").fadeOut();
		$("#sailio2").fadeIn();
		// Tähän prosesin onnistunut lopetus POST

	});
});