
# Get the payload into payload variable
import json
import sys
payload_file = None
payload = None
for i in range(len(sys.argv)):
    if sys.argv[i] == '-payload' and (i + 1) < len(sys.argv):
        payload_file = sys.argv[i+1]
        with open(payload_file, 'r') as f:
            payload = json.loads(f.read())
        break

# Open S3 connection
from boto.s3.connection import S3Connection
AWS_ACCESS_KEY_ID = "AKIAJIYSSDR3ONQIJYBA"
AWS_SECRET_ACCESS_KEY = "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"
conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket('makeymedia')

# Create file names
import uuid
from datetime import datetime
year = datetime.now().year
month = datetime.now().month
random_file_name = str(uuid.uuid4())
folder_location = "/" + str(year) + "/" + str(month) + "/"
small_file_location = folder_location + random_file_name + "_small.png"
large_file_location = folder_location + random_file_name + "_large.png"
full_file_location = folder_location + random_file_name + "_full.png"

# Open image from the given url
import cStringIO
import urllib
from PIL import Image as Im
img_url = payload['image_url']
# img_url = "http://www.adafruit.com/images/1200x900/998-00.jpg"
img_string = cStringIO.StringIO(urllib.urlopen(img_url).read())
img = Im.open(img_string)
print('Image opened - %s' % img_url)

# Save full image to S3
key = bucket.new_key(full_file_location)
key.set_contents_from_string(img_string.getvalue())
print('Full image saved - %s' % full_file_location)

# Resize and Save large image to S3
img.thumbnail((640, 428), Im.ANTIALIAS)
out_img_large = cStringIO.StringIO()
img.save(out_img_large, 'PNG')
key = bucket.new_key(large_file_location)
key.set_contents_from_string(out_img_large.getvalue())
print('Large image saved - %s' % large_file_location)

# Resize and Save small image to S3
img.thumbnail((240, 240), Im.ANTIALIAS)
out_img_small = cStringIO.StringIO()
img.save(out_img_small, 'PNG')
key = bucket.new_key(small_file_location)
key.set_contents_from_string(out_img_small.getvalue())
print('Small image saved - %s' % small_file_location)

# Send updated data to makeystreet
import urllib2
s3_prefix = "http://makeymedia.s3.amazonaws.com"
values = {
    'image_id': payload['image_id'],
    'small_url': s3_prefix + small_file_location,
    'large_url': s3_prefix + large_file_location,
    'full_url': s3_prefix + full_file_location,
}
get_data = urllib.urlencode(values)
url = "http://makeystreet-prod.elasticbeanstalk.com/image/update/?%s" % get_data
print('Request Payload: %s' % get_data)
print('Request URL: %s' % url)
response = urllib2.urlopen(url)
print('Response Code: %d' % response.code)
print('Response Text: %s' % response.read())
