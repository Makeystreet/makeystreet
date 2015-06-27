$(document).ready(function(){

	// Nar Bar
	$('.right.menu.open').on("click",function(e){
		e.preventDefault();
		$('.ui.vertical.menu').toggle();
	});

	$('.ui.dropdown').dropdown();

	$('.login.modal').modal('attach events', '.item.login', 'show');
	$('.login-form').form();
});
