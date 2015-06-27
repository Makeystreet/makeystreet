$(function(){
	$('.login.modal').modal('attach events', '.item.login', 'show');
	$('.login.modal').modal('attach events', '.login-button', 'show');
	$('.login-form').form();

	// Nar Bar
	$('.right.menu.open').on("click",function(e){
		e.preventDefault();
		$('.ui.vertical.menu').toggle();
	});

	$('.ui.dropdown').dropdown();
});
$(function(){
	$('.notifications-popup-button').popup({
		popup: '.notifications-popup',
		on: 'click',
		position: 'top center'
	});
});