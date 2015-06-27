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

	$('.post-answer').click(function(){
		$('.ui.form.add-answer').form('validate form');
	});

	$('.ui.form.add-answer').form({
		description: {
			identifier  : 'description',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please provide an answer'
			}
			]
		},
	}, {
		inline : true,
		on : 'blur',
		onSuccess: function(){
			$('.add-answer-form').form('submit');
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

	// $(".comments-toggle").on('click', function(){
	// 	$(this).hide();
	// 	$(this).siblings('.comments').show();
	// });

	$('.question.show-comments').on('click', function(){
		var questionId = $(this).data('question-id');
		var commentsSelector = ".comments-segment[data-question-id='" + questionId + "'";
		$(commentsSelector).show();
		$(this).siblings('.hide-comments').show();
		$(this).hide();
	});

	$('.question.hide-comments').on('click', function(){
		var questionId = $(this).data('question-id');
		var commentsSelector = ".comments-segment[data-question-id='" + questionId + "'";
		$(commentsSelector).hide();
		$(this).siblings('.show-comments').show();
		$(this).hide();
	});

	$('.answer.show-comments').on('click', function(){
		var answerId = $(this).data('answer-id');
		var commentsSelector = ".comments-segment[data-answer-id='" + answerId + "'";
		$(commentsSelector).show();
		$(this).siblings('.hide-comments').show();
		$(this).hide();
	});

	$('.answer.hide-comments').on('click', function(){
		var answerId = $(this).data('answer-id');
		var commentsSelector = ".comments-segment[data-answer-id='" + answerId + "'";
		$(commentsSelector).hide();
		$(this).siblings('.show-comments').show();
		$(this).hide();
	});
});
