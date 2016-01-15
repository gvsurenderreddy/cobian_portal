$(document).ready(function() {
    $("#slider").anythingSlider({
        autoPlay: true,
        delay: 5000,
        buildArrows: true,
        buildNavigation: false,
        buildStartStop: false,
        backText: "",
        appendBackTo: $(".media-player-control.left"),
        appendForwardTo: $(".media-player-control.right")
    });
   
   $(".media-player-control.right").click(function(){
       $('#slider1').data('AnythingSlider').goForward(); 
   });
});