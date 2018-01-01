(function ($) {
   "use strict";

/*--------------------------
	 preloader
---------------------------- */	
	$(window).on('load',function(){
		var pre_loader = $('#preloader')
		pre_loader.fadeOut('slow',function(){$(this).remove();});
	});	

/*----------------------------
 Header Images
------------------------------*/
	var header_img = $(".header-img");
	   header_img.height($(window).height());
		$(window).on('resize',function(){
		$(".header-img").height($(window).height());
	});	

/*---------------------
 TOP Menu Stick
--------------------- */
	var s = $("#sticker");
	var pos = s.position();					   
	$(window).scroll(function() {
		var windowpos = $(window).scrollTop();
		if (windowpos > pos.top) {
		s.addClass("stick");
		} else {
			s.removeClass("stick");	
		}
	});
	

/*----------------------------
 Navbar nav
------------------------------ */
	var main_menu = $(".main-menu ul.navbar-nav li ");
	  main_menu .on('click', function(){
		 main_menu .removeClass("active");
		$(this).addClass("active");
	});	

/*----------------------------
 Scrollspy js
------------------------------ */
	var Body = $('body');
	Body.scrollspy({
		target: '.navbar-collapse',
		offset: 80
	});

/*---------------------
	 venobox
--------------------- */
	var veno_box = $('.venobox');
	veno_box.venobox();

/*---------------------
 Testimonial carousel
---------------------*/
	var test_carousel = $('.testimonial-carousel');
	test_carousel.owlCarousel({
		loop:true,
		nav:false,
		dots:true,
		autoplay:false,
		smartSpeed:3000,
		responsive:{
			0:{
				items:1
			},
			768:{
				items:1
			},
			1000:{
				items:1
			}
		}
	});
/*----------------------------
Page Scroll
------------------------------ */
    var page_scroll = $('a.page-scroll');
	page_scroll.on('click', function(event) {
		var $anchor = $(this);
		  $('html, body').stop().animate({
			  scrollTop: $($anchor.attr('href')).offset().top - 55
			}, 1500, 'easeInOutExpo');
		event.preventDefault();
	}); 

/*--------------------------
 scrollUp
---------------------------- */
	$.scrollUp({
		scrollText: '<i class="fa fa-angle-up"></i>',
		easingType: 'linear',
		scrollSpeed: 900,
		animation: 'fade'
	});
/*----------------------------
 isotope active
------------------------------ */
	// portfolio start
	$(window).on("load",function() {
		var $container = $('.awesome-project-content');
		$container.isotope({
			filter: '*',
			animationOptions: {
				duration: 750,
				easing: 'linear',
				queue: false
			}
		});
		var pro_menu = $('.project-menu li a');
		var pro_menu_active = $('.project-menu li a.active');
		    pro_menu.on("click", function() {
			pro_menu_active.removeClass('active');
			$(this).addClass('active');
			var selector = $(this).attr('data-filter');
			$container.isotope({
				filter: selector,
				animationOptions: {
					duration: 750,
					easing: 'linear',
					queue: false
				}
			});
			return false;
		});

	});
	//portfolio end

})(jQuery); 
