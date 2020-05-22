
	
(function ($) {

    "use strict";

	// JQUERY LIGHT BOX
	
	if ( $.isFunction($.fn.fluidbox) ) {
		$('a').fluidbox();
	}

	
	$('a[href="#"]').on('click', function(event){
		return;
	});
	
	// COUNTDOWN TIME 
	
	countdownTime();
	
	
	$('[data-nav-menu]').on('click', function(event){
		
		var $this = $(this),
			visibleHeadArea = $this.data('nav-menu');
		
		$(visibleHeadArea).toggleClass('visible');
		
	});
	
	
	var winWidth = $(window).width();
	dropdownMenu(winWidth);
	
	$(window).on('resize', function(){
		dropdownMenu(winWidth);
		
	});
	
	// Circular Progress Bar
	
	var isAnimated = false;
	
	
})(jQuery);



function countdownTime(){
	
	if(isExists('#clock')){
		$('#clock').countdown('2021/06/26', function(event){
			var $this = $(this).html(event.strftime(''
				+ '<div class="time-sec"><span class="title">%D</span> days </div>'
				+ '<div class="time-sec"><span class="title">%H</span> hours </div>'));
		});
	}
}
function dropdownMenu(winWidth){
	
	if(winWidth > 767){
		
		$('.main-menu li.drop-down').on('mouseover', function(){
			var $this = $(this),
				menuAnchor = $this.children('a');
				
			menuAnchor.addClass('mouseover');
			
		}).on('mouseleave', function(){
			var $this = $(this),
				menuAnchor = $this.children('a');
				
			menuAnchor.removeClass('mouseover');
		});
		
	}else{
		
		$('.main-menu li.drop-down > a').on('click', function(){
			
			if($(this).attr('href') == '#') return false;
			if($(this).hasClass('mouseover')){ $(this).removeClass('mouseover'); }
			else{ $(this).addClass('mouseover'); }
			return false;
		});
	}
	
}

function isExists(elem){
	if ($(elem).length > 0) { 
		return true;
	}
	return false;
}
