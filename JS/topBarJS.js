$(document).ready(function(){
	alert("Loaded")

	$('[data-trigger="dropdown"]').on('mouseenter', function(){
		var submenu = $(this).parent().find('.submenu');
		submenu.addClass('active');
		
		//submenu.fadeIn(300);
		

		$('.profile-menu').on('mouseleave', function(){

			$(this).find('.submenu').removeClass('active');
			//submenu.fadeOut(300);
		});

		$('.algorithm-menu').on('mouseleave', function(){
			$(this).find('.submenu').removeClass('active');
		});
	});
})