$(document).ready(function(){
	alert("Loaded")

	$('[data-trigger="dropdown"]').on('mouseenter', function(){

		var submenu = $(this).parent().find('.submenu');
		//submenu.fadeIn(300);
		submenu.addClass('active');

		$('.profile-menu').on('mouseleave', function(){
			$(this).find('.submenu').removeClass('active');
			//submenu.fadeOut(300);
		});

	});
})