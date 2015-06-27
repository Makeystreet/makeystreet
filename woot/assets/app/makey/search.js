$(document).ready(function(){

	// Nar Bar
	$('.right.menu.open').on("click",function(e){
		e.preventDefault();
		$('.ui.vertical.menu').toggle();
	});

	$('.ui.dropdown').dropdown();

	$('.login.modal').modal('attach events', '.item.login', 'show');
	$('.login.modal').modal('attach events', '.login-button', 'show');
	$('.login-form').form();

	$('.search-button').on('click', function(){
		var query = $('.search-input').val();
		if(!query)
			return;

		var searchURL = GLOBALS.SEARCH_URL + "?q=" + encodeURIComponent(query);

		window.open(searchURL, '_self');
		$('.search-button').addClass('loading');
	});

	$('.search-input').keypress(function (e) {
		if (e.keyCode == 13) {
			$('.search-button').click();
		}
	});


	// MENU
	$('.tab-item').on('click', function(){
		$('.tab-item').removeClass('active');
		$(this).addClass('active');

		$('.ui.tab').hide();
		var currentTab = $(this).data('tab');
		$('.ui.tab[data-tab="'+currentTab+'"]').show();
	});

	if($('.vertical-makey-menu').length === 1){
		$('.ui.header.submodules').hide();
	}

	$('.ui.divided.items .item').on('click', function(){
		window.open($(this).data('href'), '_self');
	});
});
