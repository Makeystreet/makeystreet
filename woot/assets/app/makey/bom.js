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

	$('.ui.form.add-bom').form({
		name: {
			identifier  : 'name',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please provide the part name'
			}
			]
		},
	}, {
		inline : true
	});

	$('.delete-bom-button').on('click', function(){
		var that = this;
		$('.delete-bom-modal').modal({
			closable  : false,
			onDeny    : function(){
			},
			onApprove : function() {
				$(that).parent('.delete-bom-form').submit();
			}
		}).modal('show');
	});

	$('.edit-bom-button').on('click', function(){
		var bomID = $(this).data('bom-id');
		var $modalEl = $('.edit-bom-modal[data-bom-id="'+bomID+'"]');
		$modalEl.modal({
			selector: {
				close: '.icon.close, .edit-cancel-button'
			}
		}).modal('show');
	});

	$('.ui.form.edit-bom').form({
		name: {
			identifier  : 'name',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please provide the part name'
			}
			]
		},
	}, {
		inline : true
	});
});
