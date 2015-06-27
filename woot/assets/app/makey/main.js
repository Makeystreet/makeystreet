//Updates Section

var setMakeyUpdates = function(makeyId){
    //The URL for the API
    var apiUrl = "/api/v1/makey/activities/?q=" + makeyId;
    var updatesItemTemplate = Handlebars.compile($("#update-activity-item-template").html());
    var showLoading = function() {
    	$('.ui.segment.updates-feed-container').addClass("loading");
    };

    var hideLoading = function() {
    	$('.ui.segment.updates-feed-container').removeClass("loading");
    };

    showLoading();
    showLoading();
    $.getJSON( apiUrl, function( data ) {
    	showUpdates(data)
    	hideLoading();
    });


    var showUpdates = function(data){
    	var $containerEl = $(".ui.item.updates-preview-items");
    	for(var i =0;i<data.length;i++){
    		var updateItem = updatesItemTemplate(data[i]);
    		$containerEl.append(updateItem);
    	};
    }
}

// Preview Section

var setMakeyPreview = function(makeyId) {
	var apiUrl = "/api/v1/makey/preview/?q=" + makeyId;

	var insightItemTemplate = Handlebars.compile($("#insight-activity-item-template").html());
	var discussionItemTemplate = Handlebars.compile($("#discussion-activity-item-template").html());
	var insightItemEmptyTemplate = Handlebars.compile($("#insight-activity-item-empty-template").html());
	var discussionItemEmptyTemplate = Handlebars.compile($("#discussion-activity-item-empty-template").html());
	var assemblyLinkTemplate = Handlebars.compile($("#assembly-link-template").html());

	var showLoading = function() {
		$('.ui.segment.insights-preview-segment').addClass("loading");
		$('.ui.segment.discussions-preview-segment').addClass("loading");
	};

	var hideLoading = function() {
		$('.ui.segment.insights-preview-segment').removeClass("loading");
		$('.ui.segment.discussions-preview-segment').removeClass("loading");
	};

	showLoading();
	$.getJSON( apiUrl, function( data ) {
		showPreview(data)
	});

	var showPreview = function(data) {
		showPreviewInsights(data);
		showPreviewDiscussions(data);
		showMakeyLink(data);
		hideLoading();
	};

	var showMakeyLink = function(data) {
		var $containerEl = $('.assembly-link-container');
		$containerEl.html(assemblyLinkTemplate(data));
	};

	var showPreviewInsights = function(data) {
		var $containerEl = $(".ui.items.insights-preview-items");

		$containerEl.empty();
		for (var i = 0; i < data.insights.recent.length; i++) {
			var insightItem = insightItemTemplate(data.insights.recent[i]);
			$containerEl.append(insightItem);
		};

		if (data.insights.recent.length == 0)
			$containerEl.append(insightItemEmptyTemplate(data));
	}

	var showPreviewDiscussions = function(data) {
		var $containerEl = $(".ui.items.discussions-preview-items");

		$containerEl.empty();
		for (var i = 0; i < data.discussions.recent.length; i++) {
			var discussionItem = discussionItemTemplate(data.discussions.recent[i]);
			$containerEl.append(discussionItem);
		};

		if (data.discussions.recent.length == 0)
			$containerEl.append(discussionItemEmptyTemplate(data));
	}
};

// ROUTER
app.Router = Backbone.Router.extend({
	routes: {
		"(/)" : "defaultRoute",
		"overview(/)" : "overview",
		"insights(/)" : "insights",
		"issues(/)" : "issues",
		"files(/)" : "files",
		"bom(/)" : "bom",
		"docs(/)" : "docs"
	},

	initialize: function() {
		var that = this;
		$('.page-tabs a.item').click(function() {
			if($(this).data('tab')) {
				that.navigate($(this).data('tab'), {trigger: true});
			}
		});
	},

	defaultRoute: function() {
		this.navigate('overview', {trigger: true, replace: true});
	},

	overview: function() {
		this.toggleTab('overview');
	},

	docs: function() {
		this.toggleTab('docs');
	},

	files: function() {
		this.toggleTab('files');
	},

	gallery: function() {
		this.toggleTab('gallery');
	},

	insights: function() {
		this.toggleTab('insights');
	},

	issues: function() {
		// redirected with href tag in a.item
	},

	bom: function() {
		// redirected with href tag in a.item
	},

	hideAllTabs: function() {
		$('.page-tabs-content > .ui.tab').removeClass('active');
	},

	showTab: function(tab) {
		$('.page-tabs-content .ui.tab[data-tab="'+tab+'"]').addClass('active');
	},

	highlightTabPill: function(tab) {
		$('.page-tabs a.item').removeClass('active');
		$('.page-tabs a.item[data-tab="'+tab+'"]').addClass('active');
	},

	toggleTab: function(tab) {
		this.hideAllTabs();
		this.highlightTabPill(tab);
		this.showTab(tab);
	}
});

var saveImage = function(url){
	var inputItemTemplate = Handlebars.compile($('#file-progress-input-item-template').html());
	var $formEl = $('.add-image-form');
	for (var key in imageFileUploadDone) {
		if (imageFileUploadDone.hasOwnProperty(key)) {
			$formEl.append(inputItemTemplate({'url' : imageFileUploadDone[key]}));
		}
	}
	$('.add-image-form').submit();
};

var saveImageLink = function(url){
	var inputItemTemplate = Handlebars.compile($('#file-progress-input-item-template').html());
	var $formEl = $('.add-image-form');
	$formEl.append(inputItemTemplate({'url' : url}));
	$('.add-image-form').submit();
};

var saveVideo = function(url, site){
	$('.add-video-form-url-input').val(url);
	$('.add-video-form-site-input').val(site);
	$('.add-video-form').submit();
};

var saveFile = function(url, name, type){
	var files = $('.upload-file-input').prop('files')
	var file = files[0]
	$('.add-file-form-url-input').val(url);
	$('.add-file-form-name-input').val(file.name);
	$('.add-file-form-type-input').val(file.type);
	$('.add-file-form-desc-input').val(
		$('.upload-file-annotation-input').val()
		);
	$('.add-file-form').submit();
};

// ADD GALLERY STUFF
$('body').on('click', '.link-image-button',function() {
	var imageUrl = $('.link-image-input').val()
	if(!imageUrl)
		return;

	var urlRegex = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/;

	if(!urlRegex.test(imageUrl))
		return;

	if(imageUrl.substring(4,0) != "http") {
		imageUrl = "http://" + imageUrl;
	}

	$('.link-image-button').addClass('loading');
	saveImageLink(imageUrl);
});
$('body').on('click', '.link-video-button',function() {
	var videoUrl = $('.link-video-input').val()
	if(!videoUrl)
		return;

	var youtube_url_regex = /^(http|https):\/\/(?:www\.)?youtube.com\/watch\?(?=[^?]*v=[-\w+])(?:[^\s?]+)?$/;
	var vimeo_url_regex = /^(http\:\/\/|https\:\/\/)?(www\.)?(vimeo\.com\/)([0-9]+)$/;

	var currentSite = 0;
	if(youtube_url_regex.test(videoUrl)) {
		currentSite = 6;
	} else if(vimeo_url_regex.test(videoUrl)) {
		currentSite = 4;
	} else {
		return;
	}

	if(videoUrl.substring(4,0) != "http") {
		videoUrl = "http://" + videoUrl;
	}

	$('.link-video-button').addClass('loading');
	saveVideo(videoUrl, currentSite);
});

$('body').on('click', '.upload-image-button', function(){
	$('.upload-image-input').click();
});

$('body').on('click', '.upload-file-button', function(){
	$('.upload-file-input').click();
});

var upload_attempts = 0;
var upload_file_attempts = 0;

var uploadImage = function(event){
	var s3upload = new S3Upload({
		file_dom_selector: 'upload_image_input',
		s3_sign_put_url: GLOBALS.S3_SIGN_URL,
		onProgress: function(file, percent, message) {
			// console.log('progress: ' + file.name + ": "+ percent + " - " + message);
			imageFileIndex[file.name].progress({
				percent: percent,
				showActivity: false
			});
		},
		onFinishS3Put: function(file, url) {
			imageFileUploadDone[file.name] = url;
			imageFileDeferreds[file.name].resolve(url);
		},
		onError: function(file, status) {
			// upload_attempts++;
			// if(upload_attempts <= 3) {
			// 	uploadImage(event);
			// } else {
			// 	$('.upload-image-button').removeClass('loading');
			// 	upload_attempts = 0;
			// }
		}
	});
};

var uploadFile = function(){
	var s3upload = new S3Upload({
		file_dom_selector: 'upload_file_input',
		s3_sign_put_url: GLOBALS.S3_SIGN_FILE_URL,
		s3_extra_parameters: "makey_id="+GLOBALS.MAKEY_ID,
		onProgress: function(file, percent, message) {
			$('.file-upload-progress-bar').progress({
				percent: percent,
				showActivity: false
			});
		},
		onFinishS3Put: function(file, url) {
			upload_file_attempts = 0;
			saveFile(url);
		},
		onError: function(file, status) {
			upload_file_attempts++;
			if(upload_file_attempts <= 3) {
				uploadFile();
			} else {
				$('.add-file-submit').removeClass('loading');
				upload_file_attempts = 0;
			}
		}
	});
};

var imageFileIndex = {};
var imageFileUploadDone = {};
var uploadDeferredsArray = [];
var imageFileDeferreds = {};

var prepImageUpload = function(){
	var inputEl = document.getElementById('upload_image_input');
	var progressItemTemplate = Handlebars.compile($("#file-progress-template").html());
	var files = inputEl.files;
	imageFileIndex = {};
	imageFileUploadDone = {};
	uploadDeferredsArray = [];
	imageFileDeferreds = {};
	$('.file-upload-progress').empty();
	$('.file-upload-progress').show();
	for (var i = 0; i < files.length; i++) {
		$('.file-upload-progress').append(progressItemTemplate({'name': files[i].name, 'index': i}));
		$('.ui.progress.file-'+i).progress({
			showActivity: false
		});
		imageFileIndex[files[i].name] = $('.ui.progress.file-'+i);
		imageFileUploadDone[files[i].name] = false;
		var def = new $.Deferred();
		imageFileDeferreds[files[i].name] = def;
		uploadDeferredsArray.push(def);
	};

	$.when
	.apply(this, uploadDeferredsArray)
	.done(function(){
		saveImage();
	});

};

$('body').on('change', '.upload-image-input', function(event){
	$('.upload-image-button').addClass('loading');
	prepImageUpload(event);
	uploadImage(event);
});

$('body').on('change', '.upload-file-input', function(event){
	var files = event.target.files;
	if(files){
		var filename = files[0].name;
		$('.upload-file-button').html(filename);
		$('.add-file-submit').removeClass('disabled');
	}
});

$('body').on('click', '.add-file-submit', function(event){
	$('.add-file-submit').addClass('loading');
	$('.file-upload-progress-bar').show();
	$('.file-upload-progress-bar').progress();
	uploadFile();
});

$(document).ready(function(){

	// Nar Bar
	$('.right.menu.open').on("click",function(e){
		e.preventDefault();
		$('.ui.vertical.menu').toggle();
	});

	$('.ui.dropdown').dropdown();

	$('.file-upload-progress').hide();
	$('.file-upload-progress-bar').hide();

	// Insights Tab
	$('.login.modal').modal('attach events', '.item.login', 'show');
	$('.login.modal').modal('attach events', '.login-button', 'show');
	$('.login-form').form();

	$('.activity-tabs .item').tab();
	$('.add-gallery-tabs .item').tab();

	//Watch
	$('.ui.form.watch-toggle-form').form();

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
				prompt : 'Please enter a title for this Insight.'
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
				prompt : 'Please describe your Insight'
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

	// Discussions
	$('.ask-question.modal')
	.modal({
		selector: {
			close: '.icon.close, .ask-question-cancel'
		}
	})
	.modal('attach events', '.ask-question.button', 'show');

	$('.ask-question-submit').click(function(){
		$('.ui.form.ask-question').form('validate form');
	});

	$('.ui.form.ask-question').form({
		title: {
			identifier  : 'title',
			rules: [
			{
				type   : 'empty',
				prompt : 'What is your question?'
			}
			]
		},
		description: {
			identifier  : 'description',
			rules: [
			{
				type   : 'empty',
				prompt : 'Please describe your question'
			}
			]
		},
	}, {
		inline : true,
		on : 'blur',
		onSuccess: function(){
			$('.ask-question-form').form('submit');
		}
	});

	// GALLERY
	$('.add-gallery.modal')
	.modal({
		selector: {
			close: '.icon.close, .add-gallery-cancel'
		}
	})
	.modal('attach events', '.add-gallery.button', 'show');

	//FILES
	$('.add-files.modal')
	.modal({
		selector: {
			close: '.icon.close, .add-file-cancel'
		}
	})
	.modal('attach events', '.add-file.button', 'show');

	// OVERVIEW STUFF
	setMakeyPreview(GLOBALS.MAKEY_ID);

	app.router = new app.Router();

	Backbone.history.start({
		root: GLOBALS.MAKEY_URL_ROOT,
		pushState: true
	});

	// GALLERY POPUPS
	$('.img-popup').magnificPopup({
		type : 'image',
		gallery : {
			enabled:true
		},
		// image : {
		// 	titleSrc: function(item) {
		// 		comments = item.el.attr('data-comments') ? item.el.attr('data-comments') : 0;
		// 		insights = item.el.attr('data-insights') ? item.el.attr('data-insights') : 0;
		// 		upvotes = item.el.attr('data-upvotes') ? item.el.attr('data-upvotes') : 0;
		// 		return '<a href="#">'+comments+' comments</a> | <a href="#">'+insights+' insights</a> | <a href="#">'+upvotes+' upvotes</a>';
		// 	}
		// }
	});
	$('.video-popup').magnificPopup({
		type: 'iframe'
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
