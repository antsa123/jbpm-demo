
var ProcessID = 0;
var Destination = "Nowhere";

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
	}
	
	// Prosessin aloitus
	$.ajax({
		type: "GET",
		url: "/start",
		success: tallennaID
		
	});
	
	// Suoritetaan, kun saadaan vastaus skyscannerilta
	function matkavastaus(data) {
		obj = JSON.parse(data);
		if (obj.stop == "None") {
			$("#maaranpaa").text("Hitsi!");
			$("#hintajalahtoaika").html("Äkkilähtöjä ei löytynyt tänään <br> :(");
		}
		else {
			var start = obj.start;
			var stop = obj.stop;
			Destination = obj.stop;
			var aika = obj.aika;
			var hinta = obj.hinta;
			$("#maaranpaa").text(start + " - " + stop);
			$("#hintajalahtoaika").html("Hinta: " + hinta +" €" + "<br>Lähtö huomenna kello " + aika);
		}
		$("#sailio2").fadeOut();
		$("#sailio3").fadeIn();
    }
	
	// Suoritetaan, kun saadaan prosessin lopetuksen vastaus
	function ostovastaus() {
			$("#sailio2").fadeOut();
			$("#sailio4").fadeIn();


	}
	
	$("#nappi").click(function(){
		$("#sailio1").fadeOut();
		$("#sailio2").fadeIn();
		// GET skyscanner APIsta
		$.ajax({
			type: "GET",
			data: {
				"ID": ProcessID,// Tässä lähetetään prosessin ID parametrina
				"Result" : true
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
				"ID": ProcessID,// Tässä lähetetään prosessin ID parametrina
				"Result" : true,
				"Destination" : Destination
			},
			url: "/finish",
			success: ostovastaus
		})
	});
	
	$("#tarjousnappi").click(function(){
		$("#sailio3").fadeOut();
		$("#sailio2").fadeIn();
		$.ajax({
			type: "GET",
			data: {
				"ID": ProcessID ,// Tässä lähetetään prosessin ID parametrina
				"Result" : false,
				"Destination" : Destination
			},
			url: "/finish"
		});
		$.ajax({
			type: "GET",
			url: "/start", //mikä approute
			success: function(data) {
				tallennaID(data);
				$("#sailio2").fadeOut();

				$("#sailio1").delay(100).fadeIn();

			}
		});
	});

});
