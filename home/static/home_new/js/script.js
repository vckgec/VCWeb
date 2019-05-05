// =================================
     // 		preloader                              
// ==================================// 
$(window).on('load', function() {
	$('#status').fadeOut();
	$('#preloader').delay(1000).fadeOut();
});
// =================================
     // 		Owl-Carousel                           
// ==================================// 
$(function(){
	$("#team-members").owlCarousel({
		items:2,
		autoplay:true,
		smartspeed:700,
		loop:true,
		autoplayHoverPause:true,
		nav:true,
		dots:false,
		navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>']
	});
});
// =================================
     // 		progress-bar                          
// ==================================// 

$(function(){
	$(".progress-bar").each(function() {
		console.log("here.")
		$(this).animate({
			width: $(this).attr("aria-valuenow") +"%"
		},2000);   
	});
});
// =================================
     // 		Navigation-Bar                         
// ==================================// 
// $(function () {
// 	//show/hide nav on page load
// 	showHideNav();

// 	$(window).scroll(function(){
// 		//show/hide nav on windows scroll
// 		showHideNav();
// 	});

// 	function showHideNav(){
// 		if ($(window)scrollTop() > 50 ) {
// 			//show white nav
// 			$("nav").addClass("white-nav-top");
// 			//show dark logo
// 			$(".navbar-brand img ").attr("src","image/vc_logo.jpg");
// 		} else{
// 			//hide white nav
// 			$("nav").removeClass("white-nav-top");
// 			//show logo
// 			$("navbar-brand img").attr("src", "image/vc_logo.jpg");


// 		}
// 	}
// });