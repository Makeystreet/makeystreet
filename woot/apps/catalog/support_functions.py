# contains support functions that are used in multiple views.
import urllib

from forms import EmailForm
from models.misc import EmailCollect


def if_email_add(request):
    email = request.COOKIES.get('email', 'noemailset')
    if email != 'noemailset':
        # print email
        email = urllib.unquote(email)
        # print email
        form = EmailForm({'email': email, })
        cd = ''
        if form.is_valid():
            cd = form.cleaned_data
            # print "cleaned data"
            # print cd["email"]
            if not EmailCollect.objects.filter(email=cd["email"]):
                e = EmailCollect(email=cd["email"])
                e.save()

        # else:
        #     print "form not valid"
