
var ProcessID = 0;

// Kutsutaan, kun ikkuna suljetaan tai sivulta poistutaan
$(window).bind("beforeunload", function() {
	
	$.ajax({
		type: "GET",
		data: {
			"ID": ProcessID // Tässä lähetetään prosessin ID parametrina
			},
		url: "/abort"
	
	});
	return "Leaving page";
});

$(document).ready(function() {
	
	function tallennaID(data) {
		obj = JSON.parse(data);
		ProcessID = obj.ProcessID;
		console.log(ProcessID)
	}
	
	// Prosessin aloitus TÄSSÄ VOISI VASTAUKSENA TALLENTAA PROSESSI IDN
	$.ajax({
		type: "GET",
		url: "/start", //mikä approute
		success: tallennaID
		
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
			$("#ostonappi").hide();
	}
	
	$("#nappi").click(function(){
		$("#sailio1").fadeOut();
		$("#sailio2").fadeIn();
		// GET skyscanner APIsta
		$.ajax({
			type: "GET",
			data: {
				"ID": ProcessID // Tässä lähetetään prosessin ID parametrina
			},
			url: "/skyscanner",
			success: matkavastaus
		});
	});
	
	$("#ostonappi").click(function(){
		$("#sailio3").fadeOut();
		$("#sailio2").fadeIn();
		// Prosessin lopetus
		$.ajax({
			type: "GET",
			data: {
				"ID": ProcessID // Tässä lähetetään prosessin ID parametrina
			},
			url: "/finish",
			success: ostovastaus
		})
	});
	
});
