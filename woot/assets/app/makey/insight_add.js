var upload_attempts = 0;

var uploadImage = function(event){
	var s3upload = new S3Upload({
		file_dom_selector: 'upload_image_input',
		s3_sign_put_url: GLOBALS.S3_SIGN_URL,
		onProgress: function(file, percent, message) {
			return;
		},
		onFinishS3Put: function(file, url) {
			upload_attempts = 0;
			$('.add-insight-upload-image-preview').attr("src", url);
			$('.add-insight-upload-image-preview').show();

			$('.upload-image-button').removeClass('loading');
			$('.upload-image-button').html('<i class="upload icon"></i>Change image');

			$('.add-insight-image-url').val(url);

			$('.tag-image-select').removeClass("selected");
			$('.add-insight-image-id').val('');
		},
		onError: function(file, status) {
			upload_attempts++;
			if(upload_attempts <= 3) {
				uploadImage(event);
			} else {
				$('.upload-image-button').removeClass('loading');
				upload_attempts = 0;
			}
		}
	});
};

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


	$('.add-insight-button').click(function(){
		$('.ui.form.add-insight').form('validate form');
	});

	$('.ui.form.add-insight').form({
		title: {
			identifier  : 'title',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please enter a title for this Insight'
			},
			{
				type   : 'maxLength[200]',
				prompt : 'Crossed character limit of 200. Please provide a shorter title.'
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
			addTagsToForm();
			$('.add-insight-form').form('submit');
		}
	});

	$('.tag-image-select').on('click', function(event){
		if($(this).hasClass('selected')) {
			$(this).removeClass('selected');
			$('.add-insight-image-id').val('');
		} else {
			$('.tag-image-select').removeClass('selected');
			$(this).addClass('selected');
			$('.add-insight-image-id').val($(this).data('id'));

			$('.add-insight-upload-image-preview').hide();
			$('.add-insight-image-url').val('');
			$('.upload-image-button').removeClass('loading');
			$('.upload-image-button').html('<i class="upload icon"></i> Upload an image');
		}
	});

	$('.add-insight-upload-image-preview').hide();

	$('.upload-image-button').on('click', function(){
		$('.image-upload-selector').click();
	});

	$('.image-upload-selector').on('change', function(){
		$('.add-insight-upload-image-preview').hide();
		$('.upload-image-button').addClass('loading');
		uploadImage(event);
	});

	$('.add-insight-button-sticky').sticky({
		context: '.add-insight-column',
		offset: 10
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
		$('.ui.form.add-insight input[name="tag_name"]').remove();
		$tags.each(function(){
			var tagName = $(this).data('tag-name');
			$('.ui.form.add-insight').append(tagInputTemplate({name: tagName}));
		});
	};

});
