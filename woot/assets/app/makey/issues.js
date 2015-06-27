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
		$('.search-box').addClass('loading');
	});

	$('.search-input').keypress(function (e) {
		if (e.keyCode == 13) {
			$('.search-button').click();
		}
	});

	$('.status-buttons a.open').on('click', function(){
		$('.status-buttons').hide();
		$('.status-buttons.open-active').show();
		$('.issues-segment').hide();
		$('.issues-segment.open-issues').show();
	});

	$('.status-buttons a.closed').on('click', function(){
		$('.status-buttons').hide();
		$('.status-buttons.closed-active').show();
		$('.issues-segment').hide();
		$('.issues-segment.closed-issues').show();
	});
});
