const apiKey = "tu705911788977665986179742030436";

$(document).ready(function() {
	
	// tähän prosessin aloitus POST
	$.ajax({
		type: "POST",
		url: "" //mikä approute
		
	});
	
	function matkavastaus(data) {
		obj = JSON.parse(data);
		var start = obj.start;
		var stop = obj.stop;
		var aika = obj.aika;
		var hinta = obj.hinta;
		$("#maaranpaa").text(start + " - " + stop);
		$("#hintajalahtoaika").html("Hinta: " + hinta + "<br>Lähtö huomenna kello " + aika);
		$("#sailio2").fadeOut();
		$("#sailio3").fadeIn();
    }
	
	function ostovastaus() {
		
	}
	
	$("#nappi").click(function(){
		$("#sailio1").fadeOut();
		$("#sailio2").fadeIn();
		// Tähän GET skyscanner APIsta

		$.ajax({
			type: "GET",
			url: "/skyscanner",
			success: matkavastaus
		});
	});
	
	$("#ostonappi").click(function(){
		$("#sailio3").fadeOut();
		$("#sailio2").fadeIn();
		
		$.ajax({
			type: "POST",
			url: "", //mikä approute
			success: ostovastaus
		})
		// Tähän prosesin onnistunut lopetus POST
	});
});