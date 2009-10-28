var delay = 1000;
var start_frame = 0;

function init() {
	var lis = $('slide-images').getElementsByTagName('li');
	
	for( i=0; i < lis.length; i++){
		if(i!=0){
			lis[i].style.display = 'none';
		}
	}
	end_frame = lis.length -1;
	
	start_slideshow(start_frame, end_frame, delay, lis);
	
	
}



function start_slideshow(start_frame, end_frame, delay, lis) {
	setTimeout(fadeInOut(start_frame,start_frame,end_frame, delay, lis), delay);
}


function fadeInOut(frame, start_frame, end_frame, delay, lis) {
	return (function() {
		lis = $('slide-images').getElementsByTagName('li');
		Effect.Fade(lis[frame]);
		if (frame == end_frame) { frame = start_frame; } else { frame++; }
		lisAppear = lis[frame];
		setTimeout("Effect.Appear(lisAppear);", 0);
		setTimeout(fadeInOut(frame, start_frame, end_frame, delay), delay + 1850);
	})
	
}


Event.observe(window, 'load', init, false);