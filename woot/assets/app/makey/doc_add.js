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

	$('.add-doc-button').click(function(){
		$('.ui.form.add-doc').form('validate form');
	});

	$('.ui.form.add-doc').form({
		title: {
			identifier  : 'title',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please enter a title for this doc'
			},
			{
				type   : 'maxLength[200]',
				prompt : 'Crossed character limit of 200. Please provide a shorter title.'
			}
			]
		},
		body: {
			identifier  : 'body',
			rules: [
			{
				type   : 'empty',
				prompt : 'This can\'t be empty'
			}
			]
		},
	}, {
		inline : true,
		on : 'submit',
		onSuccess: function(){
			addTagsToForm();
			$('.add-doc-form').form('submit');
		}
	});

	$('.add-doc-button-sticky').sticky({
		context: '.add-doc-column',
		offset: 10
	});

	var editor = new wysihtml5.Editor( "wysihtml-textarea", {
		toolbar:      "wysihtml-toolbar",
		parserRules:  wysihtml5ParserRules
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

	var tagsEngine = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		remote: {
			url: '/api/v1/tag/search/?q=%QUERY',
			filter: function(list) {
				return $.map(list.tags, function(tag) {
					return tag
				});
			}
		},
		limit: 10
	});
	tagsEngine.initialize();

	$('.tags-search').typeahead({
		hint: false,
		highlight: true,
		minLength: 3
	},
	{
		name: 'tags',
		displayKey: 'name',
		source: tagsEngine.ttAdapter(),
	});

	var tagTemplate = Handlebars.compile($('#tag-template').html());
	var tagInputTemplate = Handlebars.compile($('#tag-item-input-template').html());
	var addTag = function(tagName) {
		var tagSelector = ".tags-container .tag-item[data-tag-name='" + tagName + "']";
		if ($(tagSelector).length == 0)
			$('.tags-container').append(tagTemplate({name: tagName}));
		$('.tags-search').typeahead('val', '');
	};

	$('.tags-search').on("typeahead:selected", function(event, selected, dataset){
		addTag(selected.name);
	});

	$('.tags-search').on('keypress', function(event){
		if (event.keyCode == 13) {
			var tagName = $('.tags-search').typeahead('val');
			if (tagName) {
				addTag(tagName)
				$('.tags-search').typeahead('close');
			}
		}
	});

	$('.add-tag-icon').on('click', function(){
		var tagName = $('.tags-search').typeahead('val');
		if (tagName) {
			addTag(tagName)
			$('.tags-search').typeahead('close');
		}
	});

	$('.tags-container').on('click', '.icon.close', function(){
		$(this).parent('.tag-item').remove();
	});

	var addTagsToForm = function(){
		var $tags = $('.tags-container .tag-item');
		$('.ui.form.add-doc input[name="tag_name"]').remove();
		$tags.each(function(){
			var tagName = $(this).data('tag-name');
			$('.ui.form.add-doc').append(tagInputTemplate({name: tagName}));
		});
	};

});
