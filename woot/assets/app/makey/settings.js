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

	//Add collaborator
	var usersEngine = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		remote: {
			url: '/api/v1/user/search/?q=%QUERY',
			filter: function(list) {
				return $.map(list.users, function(user) {
					return { name: user.first_name + " " + user.last_name + " (" + user.username + ")", id: user.id };
				});
			}
		},
		limit: 10
	});
	usersEngine.initialize();

	$('.add-collaborator-input').typeahead({
		hint: true,
		highlight: true,
		minLength: 3
	},
	{
		name: 'users',
		displayKey: 'name',
		source: usersEngine.ttAdapter(),
	});

	$('.add-collaborator-input').on("typeahead:selected", function(event, selected, dataset){
		$('.add-collaborator-form-user-input').val(selected.id);
	});

	$('.add-collaborator-button').on('click', function() {
		$(this).addClass('loading');
		$('.add-collaborator-form').submit();
	});

	$('.edit-makey-name-form').form({
		name: {
			identifier  : 'makey_name',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please enter a name for this makey.'
			},
			{
				type   : 'maxLength[200]',
				prompt : 'Crossed character limit of 200. Please provide a shorter name.'
			}
			]
		},
		description: {
			identifier  : 'makey_desc',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please enter a description for this makey.'
			},
			{
				type   : 'maxLength[200]',
				prompt : 'Crossed character limit of 200. Please provide a shorter description.'
			}
			]
		}
	}, {
		inline : true,
		on : 'submit'
	});

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

	$('.delete-makey-button').on('click', function(){
		$('.delete-makey-modal').modal({
			closable  : false,
			onDeny    : function(){
			},
			onApprove : function() {
				$('.delete-makey-form').submit();
			}
		}).modal('show');
	});

});
