
class JSONResponse(HttpResponse):
    """
    Return a JSON serialized HTTP resonse
    """
    def __init__(self, request, data, status = 200):
        serialized = json.dumps(data)
        super(JSONResponse, self).__init__(
            content = serialized, 
            content_type = 'application/json', 
            status = status
        )

class JSONViewMixin(object):
    """
    Add this mixin to a Django CBV subclass to easily return JSON data.
    """
    def json_response(self, data, status = 200):
        return JSONResponse(self.request, data, status = 200)

def generate_profile_sidebar(request):
    args = {'static_blob':static_blob, }
    args.update(csrf(request))
    args.update({
        'my_lists' : List.objects.filter(owner__id = request.user.id)
    })
    return args

def list_edit(request, primkey = None):
    """
        This view gives a form to the template and saves it
        It can also give a blank form in primkey = None
        Args : primkey - key of list to edit. if None : create new List
        
    """
    list_instance = None
    list_edit_form = ListEditForm()
    if primkey:
        list_instance = List.objects.get(pk = primkey)
        list_edit_form = ListEditForm(instance = list_instance)
        
    if request.method == "POST":
        if list_instance:
            list_edit_form = ListEditForm(request.POST, instance = list_instance)
        else:
            list_edit_form = ListEditForm(request.POST)

        if list_edit_form.is_valid():
            my_list = list_edit_form.save()
            messages.success(request, 'The list : <b>%s</b> was saved successfully !' % my_list.name)
            return HttpResponseRedirect("/me")
        else:
            #Render the form along with all its errors.
            return render_to_response ('catalog/list/edit.html', locals(), context_instance = RequestContext(request))
    context = generate_profile_sidebar(request)
    context.update( {
        'list_instance' : list_instance, 
        'list_edit_form' : list_edit_form, 
    } )
    return render_to_response('catalog/lists/edit.html', context, context_instance = RequestContext(request))

def list_new(request):
    return list_edit(request, None)

def list_view(request, primkey = None):
    """
        This view gives a list to the template to show the products in that list
        Args : primkey of list to show
    """
    context = generate_profile_sidebar(request)
    if primkey:
        list_instance = List.objects.get(pk = primkey)
        context.update( {
            'list_instance' : list_instance, 
            'list_items' : list_instance.items.all()
        } )
    return render_to_response('catalog/lists/view.html', context, context_instance = RequestContext(request))

def ajax(request):
    response = "initial"
    if request.user.is_authenticated():
        # response = "initial2"
        if 'like' in request.POST:
            if request.POST['type'] == 'image':
                i = ProductImage.objects.get(pk = request.POST['image_id'])
                p = Product.objects.get(pk = request.POST['product_id'])
                check = LikeProductImage.objects.filter(image = i, user = request.user)
                if request.POST['like'] == "like":
                    if not check:
                        l = LikeProductImage(image = i, user = request.user, product = p, time = datetime.now())
                        l.save()
                        response = "okay"
                    else:
                        response = "data redundant"
                if request.POST['like'] == "unlike":
                    if check:
                        l = LikeProductImage.objects.get(image = i, user = request.user)
                        l.delete()
                        response = "okay"
                    else:
                        response = "data redundant"
            elif request.POST['type'] == 'tutorial':
                t = Tutorial.objects.get(pk = request.POST['tutorial_id'])
                p = Product.objects.get(pk = request.POST['product_id'])
                check = LikeTutorial.objects.filter(tutorial = t, user = request.user)
                if request.POST['like'] == "like":
                    if not check:
                        l = LikeTutorial(tutorial = t, user = request.user, product = p, time = datetime.now())
                        l.save()
                        response = "okay"
                    else:
                        response = "data redundant"
                if request.POST['like'] == "unlike":
                    if check:
                        l = LikeTutorial.objects.get(tutorial = t, user = request.user)
                        l.delete()
                        response = "okay"
                    else:
                        response = "data redundant"
            elif request.POST['type'] == 'makey':
                m = Makey.objects.get(pk = request.POST['makey_id'])
                p = Product.objects.get(pk = request.POST['product_id'])
                check = LikeMakey.objects.filter(makey = m, user = request.user)
                if request.POST['like'] == "like":
                    if not check:
                        l = LikeMakey(makey = m, user = request.user, product = p, time = datetime.now())
                        l.save()
                        response = "okay"
                    else:
                        response = "data redundant"
                if request.POST['like'] == "unlike":
                    if check:
                        l = LikeMakey.objects.get(makey = m, user = request.user)
                        l.delete()
                        response = "okay"
                    else:
                        response = "data redundant"
            elif request.POST['type'] == 'product':
                p = Product.objects.get(pk = request.POST['product_id'])
                check = LikeProduct.objects.filter(product = p, user = request.user)
                if request.POST['like'] == "like":
                    if not check:
                        l = LikeProduct(user = request.user, product = p, time = datetime.now())
                        l.save()
                        response = "okay"
                    else:
                        response = "data redundant"
                if request.POST['like'] == "unlike":
                    if check:
                        l = LikeProduct.objects.get(product = p, user = request.user)
                        l.delete()
                        response = "okay"
                    else:
                        response = "data redundant"
            elif request.POST['type'] == 'shop':
                s = Shop.objects.get(pk = request.POST['shop_id'])
                check = LikeShop.objects.filter(shop = s, user = request.user)
                if request.POST['like'] == "like":
                    if not check:
                        l = LikeShop(user = request.user, shop = s, time = datetime.now())
                        l.save()
                        response = "okay"
                    else:
                        response = "data redundant"
                if request.POST['like'] == "unlike":
                    if check:
                        l = LikeShop.objects.get(shop = s, user = request.user)
                        l.delete()
                        response = "okay"
                    else:
                        response = "data redundant"
        
        if 'adddata' in request.POST:
            # response = "initial3"
            if request.POST['adddata'] == 'tutorial':
                form = TutorialForm({'url':request.POST['url'], })
                if form.is_valid():
                    cd = form.cleaned_data
                    q = Tutorial.objects.filter(url = cd['url'])
                    if q:
                        q2 = Product.objects.filter(tutorials__url = cd['url'])
                        if q2:
                            response = "Thank you for adding the url but the tutorial is already linked to this maker part"
                        else:
                            tut = Tutorial.objects.get(url = cd['url'])
                            p = Product.objects.get(pk = request.POST['product_id'])
                            p.tutorials.add(tut)
                            p.save()
                            response = "okay"
                    else:
                        p = Product.objects.get(pk = request.POST['product_id'])
                        p.tutorials.create(user = request.user, url = cd['url'], added_time = datetime.now())
                        p.save()
                        response = "okay"
                else:
                    response = "Please enter a valid url"
            elif request.POST['adddata'] == 'makey':
                form = MakeyForm({'url':request.POST['url'], 'name':request.POST['name']})
                if form.is_valid():
                    cd = form.cleaned_data
                    q = Makey.objects.filter(url = cd['url'])
                    if q:
                        q2 = Product.objects.filter(makeys__url = cd['url'])
                        if q2:
                            response = "This makey is already linked to this maker part"
                        else:
                            makey = Makey.objects.get(url = cd['url'])
                            p = Product.objects.get(pk = request.POST['product_id'])
                            p.makeys.add(makey)
                            p.save()
                            response = "okay"
                    else:
                        p = Product.objects.get(pk = request.POST['product_id'])
                        p.makeys.create(user = request.user, name = cd['name'], url = cd['url'], added_time = datetime.now())
                        p.save()
                        response = "okay"
                else:
                    response = "Please enter a valid url"
    else:
        response = "login required"

    return HttpResponse(response)

def ajaxemail(request):
    if request.method == 'POST':
        email = request.POST['email']
        e = EmailCollect(email = email)
        e.save()
        response = "okay"

    return HttpResponse(response)

def me(request):
    if request.user.is_authenticated() == False:
        return HttpResponse('You need to login to see this page')
    
    args = generate_profile_sidebar(request)
    
    return render_to_response('catalog/me.html', args, context_instance = RequestContext(request))

def email_collect(request):
    args = {'static_blob':static_blob, }
    args.update(csrf(request))
    return render_to_response('catalog/email_collect.html', args, context_instance = RequestContext(request))


@login_required
def cfi_store_old(request):
    login = request.user.is_authenticated()

    login_alex=False
    if request.user.username=="alex":
        login_alex=True

    store=Shop.objects.get(name=store)
    productshopurls=ProductShopUrl.objects.filter(shop__name=store)
    products = Product.objects.filter(productshopurls__shop__name=store).order_by('-score')
    for product in products:
        if CfiStoreItem.objects.filter(item=product):
            product.incfistore=True

    context = {
        'static_blob':static_blob,
        'products':products_page,
        'list_pages' : list_pages,
        'total_products' : 0,
        'login':login,
        'login_alex':login_alex,
        'store':store,
    }

    return render(request, 'catalog/store_page_old.html')


def makey_page(request, makey_id):
    user_details = get_user_details_json(request)
    makey = Makey.objects.get(pk = makey_id)
    if makey:
        if user_details:
            can_edit = False
            if(request.user in makey.collaborators.all() or request.user.id == 1):
                can_edit = True

            # userflags=UserFlags.objects.get(user=)
            return render(request, 'catalog/makey_page.html', {
                'makey_id':makey_id,
                'makey_name' : makey.name,
                'user_details' : user_details, 
                'can_edit' : can_edit})
        else:
            return render(request, 'catalog/makey_page_wo_login.html', {
                'makey':makey,
                'makey_id' : makey.id,
                # 'creator':creator,
                
                })

    else:
        return HttpResponse('404 Error - this makey does not exist')

# Makey page is the one with the actual data.
def project_page(request, project_id):
    login = request.user.is_authenticated()

    return render(request, 'catalog/project_page.html', {'static_blob':static_blob, 'login':login})


def product_page_old(request, sku):
    if_email_add(request)

    # if request.user.is_authenticated() == False:
        # return HttpResponseRedirect("/launching_soon")
    # products = Product.objects.all()[5599:]
    # for p in products:
    #   p.sku = str(1+(int(p.id)-1)/10)
    #   p.save()

    # Product.objects.latest('pub_date') # this is to get the latest row in a table

    # product_id = str(1+(int(product_id)-1)*10)
    # product_id = product_id+'1'
    product = Product.objects.get(id = sku)
    if product.identicalto:
        return HttpResponseRedirect("/product/"+str(product.identicalto.id)+"/")
    product.descriptions = ProductDescription.objects.filter(product = product.id)
    product.shopurls = ProductShopUrl.objects.filter(product = product.id)
    # product.images = ProductImage.objects.filter(product = product.id)
    product.images = ProductImage.objects.filter(product = product.id) # , url__icontains = "small"
    # product.tutorials = Tutorial.objects.filter(product = product.id)
    login = request.user.is_authenticated()
    if login == True:
        for image in product.images:
            image.all_likes = LikeProductImage.objects.filter(image = image)
            q = LikeProductImage.objects.filter(image = image.id, user = request.user)
            if q:
                image.like = True
            else:
                image.like = False
        # get all the product likes
        product.all_likes = LikeProduct.objects.filter(product = product)
        q = LikeProduct.objects.filter(product = product, user = request.user)
        if q:
            product.like = True
        else:
            product.like = False
        # get all the product likes
        for shopurl in product.shopurls:
            # shop = Shop.objects.get(id = shopurl.shop)
            shopurl.all_likes = LikeShop.objects.filter(shop = shopurl.shop)
            q = LikeShop.objects.filter(shop = shopurl.shop, user = request.user)
            if q:
                shopurl.like = True
            else:
                shopurl.like = False
        # get all tutorial likes
    product.tutorials_detail = []
    for tutorial in product.tutorials.all():
        tutorial.all_likes = LikeTutorial.objects.filter(tutorial = tutorial)
        if login == True:
            q = LikeTutorial.objects.filter(tutorial = tutorial, user = request.user)
            if q:
                tutorial.like = True
            else:
                tutorial.like = False
        product.tutorials_detail.append(tutorial)
            # del product.tutorials
    # get all tutorial likes
    product.makeys_detail = []
    for makey in product.makeys.all():
        makey.all_likes = LikeMakey.objects.filter(makey = makey)
        if login == True:
            q = LikeMakey.objects.filter(makey = makey, user = request.user)
            if q:
                makey.like = True
            else:
                makey.like = False
        product.makeys_detail.append(makey)
            # del product.tutorials


    return render(request, 'catalog/product_page_original.html', {'static_blob':static_blob, 'login':login, 'product':product, })
    
def vendor_signup_page(request):
    if_email_add(request)
    return render(request, 'catalog/vendor_signup_page.html', {})
    

def landing_page2(request):
    if_email_add(request)
    # if request.user.is_authenticated() == False:
        # return HttpResponseRedirect("/launching_soon")
    login = request.user.is_authenticated()
    errors = []
    if 'q' in request.GET:
        form = SearchForm({'q':request.GET['q'], })
        cd = ''
        if form.is_valid():
            cd = form.cleaned_data
        if cd:
            q = cd['q']
        else:
            q = ''
            
        if not q:
            errors.append("Enter a search term.")
        elif len(q) < 1:
            errors.append("Enter atleast 1 characters.")
        elif len(q) > 50:
            errors.append("Enter atmost 50 characters.")
        else:
            if request.user.is_authenticated() == True:
                log = SearchLog(term = q, user = request.user, time = datetime.now())
            else:
                log = SearchLog(term = q, time = datetime.now())
            log.save()
            q_clean = unicodedata.normalize('NFKD', q).encode('ascii', 'ignore').translate(string.maketrans("", ""), string.punctuation).strip().split(" ")
            qs = reduce(operator.and_, (Q(name__icontains = n) for n in q_clean))
            # print "search query\n\n"
            # print qs
            products = Product.objects.filter(qs).filter(identicalto = None).order_by('-score')
            # for product in products:
            #   product.url = ProductShopUrl

            paginator = Paginator(products, 30)
            # Show 25 contacts per page
            
            page = request.GET.get('page')
            if not page:
                page = 1
            try:
                products_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                products_page = paginator.page(1)
                page = 1
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                products_page = paginator.page(paginator.num_pages)
                page = paginator.num_pages
            

            if int(paginator.num_pages) == 1:
                list_pages = [1]
            elif int(paginator.num_pages) <= 8:
                list_pages = range(1, int(paginator.num_pages)+1)
            elif int(page) <= 2:
                list_pages = range(1, 5) + ['. . .'] + [paginator.num_pages]
            elif int(page) >= int(paginator.num_pages) - 2:
                list_pages = [1, '. . .'] + range(paginator.num_pages-3, paginator.num_pages+1)
            else:
                list_pages = ['. . .'] + range(int(page)-2, int(page)+3) + ['. . .'] 
            
            for product in products_page:
                img = ProductImage.objects.filter(product = product.id, is_enabled=True)
                # print(img)
                if img:
                    product.image_p = img[0]

            context = {
                'static_blob':static_blob, 
                'products':products_page, 
                'list_pages' : list_pages, 
                'total_products' : 0, 
                'query':q, 
                'login':login, 
            }

            return render(request, 'catalog/search_result.html', context)
    stores = Shop.objects.count()
    products = Product.objects.count()
    return render(request, 'catalog/search_form.html', {'static_blob':static_blob, 'login':login, 'errors': errors, "stores":stores, "products":products})
