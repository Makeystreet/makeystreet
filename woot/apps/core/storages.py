from __future__ import absolute_import

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class AwsS3Storage(S3BotoStorage):
    """
    Custom S3 storage class

    Needed for using two different buckets for storing static
    and media files on Amazon S3
    """
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = getattr(settings, 'AWS_MEDIA_STORAGE_BUCKET_NAME')
        super(AwsS3Storage, self).__init__(*args, **kwargs)

    def isfile(self, name):
        return self.exists(name)

    def isdir(self, name):
        # That's some inefficient implementation...
        # If there are some files having 'name' as their prefix, then
        # the name is considered to be a directory
        if not name:  # Empty name is a directory
            return True

        if self.isfile(name):
            return False

        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.list(self._encode_name(name))

        # Check whether the iterator is empty
        for item in dirlist:
            return True
        return False

    def move(self, old_file_name, new_file_name, allow_overwrite=False):

        if self.exists(new_file_name):
            if allow_overwrite:
                self.delete(new_file_name)
            else:
                raise "The destination file '%s' exists and allow_overwrite is \
                        False" % new_file_name

        old_key_name = self._encode_name(self._normalize_name(
            self._clean_name(old_file_name)))
        new_key_name = self._encode_name(self._normalize_name(
            self._clean_name(new_file_name)))

        k = self.bucket.copy_key(new_key_name, self.bucket.name, old_key_name)

        if not k:
            raise "Couldn't copy '%s' to '%s'" % (old_file_name, new_file_name)

        self.delete(old_file_name)

    def makedirs(self, name):
        pass

    def rmtree(self, name):
        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.list(self._encode_name(name))
        for item in dirlist:
            item.delete()
