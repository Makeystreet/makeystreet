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

	// Insights Tab
	$('.add-insight.modal')
	.modal({
		selector: {
			close: '.icon.close, .add-insight-cancel'
		}
	})
	.modal('attach events', '.add-insight.button', 'show');


	$('.add-insight-submit').click(function(){
		$('.ui.form.add-insight').form('validate form');
	});

	$('.ui.form.add-insight').form({
		title: {
			identifier  : 'title',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please enter a title this Insight'
			}
			]
		},
		description: {
			identifier  : 'description',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please describe your insight'
			}
			]
		},
	}, {
		inline : true,
		on : 'blur',
		onSuccess: function(){
			$('.add-insight-form').form('submit');
		}
	});

	$('.ui.form.upvote-insight-toggle').form();

	$('.ui.reply.form').form({
		body: {
			identifier  : 'body',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please enter a comment'
			}
			]
		}
	}, {
		inline : true
	});

	$('.delete-insight-button').on('click', function(){
		$('.delete-insight-modal').modal({
			closable  : false,
			onDeny    : function(){
			},
			onApprove : function() {
				$('.delete-insight-form').submit();
			}
		}).modal('show');
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
});
