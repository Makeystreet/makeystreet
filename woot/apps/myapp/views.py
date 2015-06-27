# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
def land(request):
    response="We just migrated our production servers. The site will be up soon."
    return HttpResponse(response)