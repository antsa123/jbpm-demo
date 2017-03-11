
$(document).ready(function() {
	
	// Prosessin aloitus
	$.ajax({
		type: "POST",
		url: "/start" //mikä approute
		
	});
	
	// Suoritetaan, kun saadaan vastaus skyscannerilta
	function matkavastaus(data) {
		obj = JSON.parse(data);
		var start = obj.start;
		var stop = obj.stop;
		var aika = obj.aika;
		var hinta = obj.hinta;
		$("#maaranpaa").text(start + " - " + stop);
		$("#hintajalahtoaika").html("Hinta: " + hinta +" €" + "<br>Lähtö huomenna kello " + aika);
		$("#sailio2").fadeOut();
		$("#sailio3").fadeIn();
    }
	
	// Suoritetaan, kun saadaan prosessin lopetuksen vastaus
	function ostovastaus() {
			$("#maaranpaa").text("Hyvää matkaa!");
			$("#hintajalahtoaika").html("Sinut ohjattaisiin lipun ostoon kokoversiossa.");
			$("#sailio2").fadeOut();
			$("#sailio3").fadeIn();
	}
	
	$("#nappi").click(function(){
		$("#sailio1").fadeOut();
		$("#sailio2").fadeIn();
		// GET skyscanner APIsta
		$.ajax({
			type: "GET",
			url: "/skyscanner",
			success: matkavastaus
		});
	});
	
	$("#ostonappi").click(function(){
		$("#sailio3").fadeOut();
		$("#sailio2").fadeIn();
		// Prosessin lopetus
		$.ajax({
			type: "POST",
			url: "/finish",
			success: ostovastaus
		})
	});
});

// Kutsutaan, kun ikkuna suljetaan tai sivulta poistutaan
$( window ).on("unload", function() {
  $.ajax({
		type: "POST",
		url: "/abort"
  });
});