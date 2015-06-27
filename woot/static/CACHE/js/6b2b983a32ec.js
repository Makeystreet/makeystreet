$(function(){
	$('.notifications-popup-button').popup({
		popup: '.notifications-popup',
		on: 'click',
		position: 'top center'
	});
});
$(function(){
	$('.login.modal').modal('attach events', '.item.login', 'show');
	$('.login.modal').modal('attach events', '.login-button', 'show');
	$('.login-form').form();
});