#This is a standalone script for django application to upload data to database

import sys, os
import unicodedata
import settings
#-----
#Libraries for blob storage
from azure.storage import *
import urllib2
from StringIO import StringIO
import PIL
from PIL import Image
#-----
django_install_folder = "E:\\repos\\makey2\\makeystreet\\DjangoApplication\\DjangoApplication"
#Change working directory to django install folder
os.chdir(django_install_folder)

print os.getcwd()


#Setup environment there
from django.core.management import setup_environ

print "HIN"
setup_environ(settings)



#Check if its working
from django.db.models.loading import get_models
loaded_models = get_models()
print loaded_models

from catalog.models import User, UsedForMaking, Tutorial, Product, Shop, ProductImage
from catalog.models import ProductShopUrl, ProductDescription
from catalog.models import LikeProduct, LikeImage, LikeUsedForMaking, LikeTutorial, LikeShop, LikeProductDescription

#Instaed of datetim python library the django timezone is used which will take care of the time zone set up in the settings.
from django.utils import timezone

choice = raw_input("Enter 1 for mongo db, 2 for mysql")

width = 320

if int(choice) == 1:
	#This is the mongoway
	#To read from mongodb and upload the content to mysql database.
	from pymongo import Connection

	#Create the mongo connection
	conn = Connection('localhost', 27017)
	dbconn = conn.TechieData.Product_Full_Data
	dbconn_name = conn.TechieData.Product_Name

	#Promt to enter the shop name
	shop_name = raw_input("Please enter the shop name : ")

	full_data = list(dbconn.find({"shop_name": shop_name}))

	#First get the shop id from the name provided
	#its assumed that the shop is added before the product is added.
	#This can be automated too. For the timebeing its left manual.
	print "Number of data points = %d" %len(full_data)

	try:
		shop_object = Shop.objects.get(name = shop_name)
		none_shop_object = Shop.objects.get(name = "NoneShop")
		none_user_object = User.objects.get(name = "NoneUser")
		print "got them"
	except:
		print "The shop doesnt exist. Either check your spelling or add the shop in the database."
		raw_input("Exiting program ..")
		sys.exit()
	#shop_object = Shop.objects.get(name = shop_name)

	#Create the blob service connection
	blob_service = BlobService(account_name = 'makeyimages', account_key = 'ujQIUkh/yYC8kuNumgMUNQmcv0yLCn+cg4C+eEFykx3ymm0hVNWxGyyriiZxFkPNM5k2rtYlL3enrU1Xh2TeFQ == ')

	print shop_object.name
	for data in full_data:
		time_created = timezone.now()
		product_id = data["product_id"]
		#Get product name from the o ther collection in mongo
		product_details = dbconn_name.find_one({"product_id":product_id}, {"product_link":1, "product_title":1})
		product_object = Product(name = product_details["product_title"], added_time = time_created)
		product_object.save()
		#Now get the created ID
		product_object_id = product_object.id
		product_shop_url_object = ProductShopUrl.objects.create(url = product_details["product_link"], added_time = time_created, shop = shop_object, product = product_object)
		product_description_object = ProductDescription.objects.create(description = data["product_description"], product = product_object, shop = shop_object, user_or_shop = True, user = none_user_object, added_time = time_created)
		#list of image urls to download from
		img_url_list = data["image_url_list"]
		img_ctr = 0
		if len(img_url_list) > 0:
			#Download the image first in the comp and then make multiple copies of it and upload to blob storage
			for image_urls in img_url_list:
				#try:
				print "Got to %d image url" %img_ctr
				img = PIL.Image.open(StringIO(urllib2.urlopen(image_urls).read()))
				img_name = image_urls.split("/")[-1]
				img.save(img_name)
				#Resizing
				wpercent = width/float(img.size[0])
				hsize = int(float(img.size[1]) * float(wpercent))
				img2 = img.resize((width, hsize), PIL.Image.ANTIALIAS)
				#Save both version of image locally
				new_image_name_big = str(product_object_id) + "_" + str(img_ctr) + "_big.jpg"
				new_image_name_small = str(product_object_id) + "_" + str(img_ctr) + "_small.jpg"
				#If its a gif file then care has to be taken before converting
				if img_name.split(".")[1] == 'gif' or img_name.split(".")[1] == 'GIF':
					img.convert('RGB').save(new_image_name_big, "JPEG")
					img2.convert('RGB').save(new_image_name_small, "JPEG")
				else:
					img.save(new_image_name_big, "JPEG")
					img2.save(new_image_name_small, "JPEG")
				#Now the images are saved in the database, these will be uploaded in azure now.
				img = open(new_image_name_big, 'rb').read()
				img2 = open(new_image_name_small, 'rb').read()
				blob_service.put_blob('images', new_image_name_big, img, x_ms_blob_type = 'BlockBlob', x_ms_blob_content_type = 'image/jpg')
				blob_service.put_blob('images', new_image_name_small, img2, x_ms_blob_type = 'BlockBlob', x_ms_blob_content_type = 'image/jpg')
				#Now as they are uploaded . Create custom urls for them
				url1 = "http://makeyimages.blob.core.windows.net/images/" + new_image_name_big
				url12 = "http://makeyimages.blob.core.windows.net/images/" + new_image_name_small
				img_object = ProductImage(url = url1, added_time = time_created, user = none_user_object, product = product_object)
				img_object.save()
				img2_object = ProductImage(url = url2, added_time = time_created, user = none_user_object, product = product_object)
				img2_object.save()
				img_ctr += img_ctr
				"""except:
					print "Sorry something went wrong" """


		print "Data added for " + product_id

elif int(choice) == 2:
	#This is the mysql way
	import MySQLdb
	try:
		db = MySQLdb.connect(host = "localhost", user = "root", passwd = "19890101", db = "techiest_catalog")
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit()
	cur = db.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("SELECT * FROM techiest_catalog.ps_product_supplier;")
	all_supplier = cur.fetchall()
	try:
		spark_shop_object = Shop.objects.get(name = "Sparkfun")
		rhydo_shop_object = Shop.objects.get(name = "Rhydolabz")
		aero_shop_object = Shop.objects.get(name = "Aeroworks")
		none_shop_object = Shop.objects.get(name = "NoneShop")
		none_user_object = User.objects.get(name = "NoneUser")
	except:
		print "The shop doesnt exist. Either check your spelling or add the shop in the database."
		raw_input("Exiting program ..")
		sys.exit()
	for rows in all_supplier:
		shop_id = rows["id_supplier"]
		if int(shop_id) == 1:
			shop_object = spark_shop_object
		elif int(shop_id) == 2:
			shop_object = rhydo_shop_object
		elif int(shop_id) == 3:
			shop_object = aero_shop_object
		time_created = timezone.now()
		product_id = rows["id_product"]
		if product_id > 0:
			#Get product name from the other table in mysql
			cur.execute("SELECT * FROM techiest_catalog.ps_product_lang WHERE id_product = "+str(product_id)+";")
			product_details = cur.fetchall()
			if len(product_details) > 0:
				product_object = Product.objects.create(name = product_details[0]["name"], added_time = time_created)
				product_shop_url_object = ProductShopUrl.objects.create(url = rows["product_supplier_link"], added_time = time_created, shop = shop_object, product = product_object)
				#Get rid of unicode data
				try:
					long_desc = unicodedata.normalize('NFKC', unicode(product_details[0]["description"])).encode('ascii', 'ignore')
				except:
					try:
						long_desc = unicodedata.normalize('NFKC', unicode(product_details[0]["description_short"])).encode('ascii', 'ignore')
					except:
						long_desc = u"NA"
				try:
					product_description_object = ProductDescription.objects.create(description = long_desc, product = product_object, shop = shop_object, user_or_shop = True, user = none_user_object, added_time = time_created)
				except:
					try:
						long_desc = unicodedata.normalize('NFKC', unicode(product_details[0]["description_short"])).encode('ascii', 'ignore')
						product_description_object = ProductDescription.objects.create(description = long_desc, product = product_object, shop = shop_object, user_or_shop = True, user = none_user_object, added_time = time_created)
					except:
						long_desc = u"NA"
						product_description_object = ProductDescription.objects.create(description = long_desc, product = product_object, shop = shop_object, user_or_shop = True, user = none_user_object, added_time = time_created)
				print "Data added for " + str(product_id)
