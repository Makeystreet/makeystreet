from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from woot.apps.catalog.models.forum import Question, Answer
from woot.apps.catalog.models.core import Makey, Comment

from woot.apps.catalog.forms import QuestionForm, AnswerForm, CommentForm


def question(request, question_id, **kwargs):
    q = get_object_or_404(Question, id=question_id)

    if request.method == "GET":
        q.increase_views()
        context = {
            'question': q,
        }
    elif request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            u = request.user
            a = Answer()
            a.save_from_form(form, creator=u, question=q)

            context = {
                'question': q,
            }
        else:
            context = {
                'question': q,
                'form': form,
            }

    if 'form' in kwargs.keys():
        context['form'] = kwargs['form']

    return render(request, 'catalog/question_page.html', context)


def ask_question(request, makey_id):
    m = get_object_or_404(Makey, id=makey_id)

    if request.method == "GET":
        context = {
            'makey': m,
        }
        return render(request, 'catalog/ask_question.html', context)

    elif request.method == "POST":
        u = get_object_or_404(User, id=request.user.id)
        form = QuestionForm(request.POST)

        if form.is_valid():
            q = Question()
            q.save_from_form(form, creator=u, makey=m)

            return HttpResponseRedirect(reverse('catalog:question', kwargs={
                'question_id': q.id
            }))
        else:
            context = {
                'makey': m,
                'form': form
            }
            return render(request, 'catalog/ask_question.html', context)


def add_comment(request):
    if request.method == "POST":
        question_id = request.POST.get('question', '')
        form = CommentForm(request.POST)
        if form.is_valid():
            owner = form.cleaned_data['owner'].split('-')
            if owner[0] == "q":
                q = get_object_or_404(Question, id=int(owner[1]))

                c = Comment()
                c.user = request.user
                c.body = form.cleaned_data['body']
                c.save()

                q.comments.add(c)
            elif owner[0] == "a":
                a = get_object_or_404(Answer, id=int(owner[1]))

                c = Comment()
                c.user = request.user
                c.body = form.cleaned_data['body']
                c.save()

                a.comments.add(c)
            kwargs = {
                'question_id': question_id,
            }
        else:
            q = get_object_or_404(Question, id=question_id)
            kwargs = {
                'question_id': question_id,
                'form': form
            }
    return HttpResponseRedirect(reverse('catalog:question', kwargs=kwargs))
