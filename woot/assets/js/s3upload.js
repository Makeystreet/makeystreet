(function() {

    window.S3Upload = (function() {

        S3Upload.prototype.s3_object_name = 'default_name';

        S3Upload.prototype.s3_sign_put_url = '/signS3put';

        S3Upload.prototype.file_dom_selector = 'file_upload';

        S3Upload.prototype.s3_extra_parameters = null;

        S3Upload.prototype.custom_mime_type = null;

        S3Upload.prototype.onFinishS3Put = function(file, public_url) {
            return console.log('base.onFinishS3Put()', public_url);
        };

        S3Upload.prototype.onProgress = function(file, percent, status) {
            return console.log('base.onProgress()', percent, status);
        };

        S3Upload.prototype.onError = function(file, status) {
            return console.log('base.onError()', status);
        };

        function S3Upload(options) {
            if (options === null) options = {};
            for (var option in options) {
                this[option] = options[option];
            }
            this.handleFileSelect(document.getElementById(this.file_dom_selector));
        }

        S3Upload.prototype.handleFileSelect = function(file_element) {
            var f, files, _i, _len, _results;
            files = file_element.files;
            _results = [];
            for (_i = 0, _len = files.length; _i < _len; _i++) {
                f = files[_i];
                this.onProgress(f, 0, 'Upload started.');
                _results.push(this.uploadFile(f));
            }
            return _results;
        };

        S3Upload.prototype.createCORSRequest = function(method, url) {
            var xhr;
            xhr = new XMLHttpRequest();
            if (xhr.withCredentials !== null) {
                xhr.open(method, url, true);
            } else if (typeof XDomainRequest !== "undefined") {
                xhr = new XDomainRequest();
                xhr.open(method, url);
            } else {
                xhr = null;
            }
            return xhr;
        };

        S3Upload.prototype.executeOnSignedUrl = function(file, callback) {
            var this_s3upload, xhr;
            this_s3upload = this;
            xhr = new XMLHttpRequest();
            xhr_url = this.s3_sign_put_url + '?s3_object_type=' + file.type + '&s3_object_name=' + encodeURIComponent(file.name);
            if(this.s3_extra_parameters) {
                xhr_url += '&' + this.s3_extra_parameters;
            }

            xhr.open('GET', xhr_url, true);
            xhr.overrideMimeType('text/plain; charset=x-user-defined');
            xhr.onreadystatechange = function(e) {
                var result;
                if (this.readyState === 4 && this.status === 200) {
                    try {
                        result = JSON.parse(this.responseText);
                    } catch (error) {
                        this_s3upload.onError(file, 'Signing server returned some ugly/empty JSON: "' + this.responseText + '"');
                        return false;
                    }
                    if(file.type == "") {
                        this_s3upload.custom_mime_type = result.mime_type;
                    }
                    return callback(file, result.signed_request, result.url);
                } else if (this.readyState === 4 && this.status !== 200) {
                    return this_s3upload.onError(file, 'Could not contact request signing server. Status = ' + this.status);
                }
            };
            return xhr.send();
        };

        S3Upload.prototype.uploadToS3 = function(file, url, public_url) {
            var this_s3upload, xhr;
            this_s3upload = this;
            xhr = this.createCORSRequest('PUT', url);
            if (!xhr) {
                this.onError('CORS not supported');
            } else {
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        this_s3upload.onProgress(file, 100, 'Upload completed.');
                        return this_s3upload.onFinishS3Put(file, public_url);
                    } else if(xhr.status == 307) {
                        console.log(307);
                        var redirectUrl = xhr.getResponseHeader('Location');
                        console.log(redirectUrl);
                        return this_s3upload.uploadToS3(file, redirectUrl, public_url);
                    } else {
                        return this_s3upload.onError(file, 'Upload error: ' + xhr.status);
                    }
                };
                xhr.onerror = function() {
                    return this_s3upload.onError(file, 'XHR error.');
                };
                xhr.upload.onprogress = function(e) {
                    var percentLoaded;
                    if (e.lengthComputable) {
                        percentLoaded = Math.round((e.loaded / e.total) * 100);
                        return this_s3upload.onProgress(file, percentLoaded, percentLoaded === 100 ? 'Finalizing.' : 'Uploading.');
                    }
                };
            }

            if(file.type == "") {
                xhr.setRequestHeader('Content-Type', this_s3upload.custom_mime_type);
            } else {
                xhr.setRequestHeader('Content-Type', file.type);
            }
            xhr.setRequestHeader('x-amz-acl', 'public-read');
            return xhr.send(file);
        };

        S3Upload.prototype.uploadFile = function(file) {
            var this_s3upload;
            this_s3upload = this;
            return this.executeOnSignedUrl(file, function(file, signedURL, publicURL) {
                return this_s3upload.uploadToS3(file, signedURL, publicURL);
            });
        };

        return S3Upload;

    })();

}).call(this);
