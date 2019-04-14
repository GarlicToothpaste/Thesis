$(document).ready(function(){
	var isShown = false;

	alert("Loaded")
	//toEdit: edit '[data-trigger="dropdown"]' to specific
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


	$('[data-trigger="clickable-dropdown').on('click' , function(){
		
		// alert("Clicked")
		var dropdown = $(this).parent().find('.dropdown');

		console.log(isShown);
		//dropdown.addClass('active');
		if( isShown === false){
			$('.body-dropdown-menu').on('click' , function(){
				//console.log("isShown === false");
				//console.log($(this).find('.dropdown'));

				$(this).find('.dropdown').addClass('active');
				isShown = true;
			})
		}

		else {
			$('.body-dropdown-menu').on('click' , function(){
				
				//console.log("isShown === true");
				//console.log($(this).find('.dropdown'));

				$(this).find('.dropdown').removeClass('active');
				isShown = false;	
			})
		}

	})
})