import json
from datetime import datetime
from django.http import Http404

from django.contrib.auth.models import User
from django.utils import timesince

from woot.apps.catalog.models.core import Note, Makey
from woot.apps.catalog.models.interactions import Interaction, UserInteraction, UserNotification
from woot.apps.catalog.models.forum import Question, Answer


def get_user_details_json(request):
    login = request.user.is_authenticated()

    user_details = {}
    if login:
        cur_user = User.objects.get(username=request.user.username)
        user_details["id"] = cur_user.id
        user_details["facebook_name"] = cur_user.first_name + " " +\
            cur_user.last_name
        user_details = json.dumps(user_details)
    else:
        user_details = {}

    return user_details


def is_admin(request):
    if request.user in [User.objects.get(id=1), User.objects.get(id=76),
                        User.objects.get(id=276), User.objects.get(id=16),
                        User.objects.get(id=302)]:
        return True
    return False

def check_private_access(request, makey):
    if makey.is_private:
        if request.user not in makey.collaborators.all() and not is_admin(request):
            raise Http404

def time_elapsed(datetimeobj):
    datetimeobj = datetimeobj.replace(tzinfo=None)
    return timesince.timesince(datetimeobj)



def get_makey_activities(makey, include_submodules=False):

    # Create time sorted list of activities
    activities = []

    if not makey:
        return activities

    # Get insight activities
    insight_creation_interactions = UserInteraction.objects.\
        filter(event=Interaction.activity_insight_created,
               event_id__in=makey.notes.all().values_list('id', flat=True))

    for insight_interaction in insight_creation_interactions:
        insight_interaction.insight = Note.objects.get(pk=insight_interaction.event_id)


    activities += insight_creation_interactions

    # Get insight activities
    questions = Question.objects.filter(makey=makey)
    question_creation_interactions = UserInteraction.objects.\
        filter(event=Interaction.activity_question_created,
               event_id__in=questions.values_list('id', flat=True))

    for question_interaction in question_creation_interactions:
        question_interaction.question = Question.objects.get(pk=question_interaction.event_id)


    activities += question_creation_interactions

    # Get insight activities
    answer_creation_interactions = UserInteraction.objects.\
        filter(event=Interaction.activity_answer_created,
               event_id__in=Answer.objects.filter(question__in=questions).
               values_list('id', flat=True))

    for answer_interaction in answer_creation_interactions:
        answer_interaction.answer = Answer.objects.get(pk=answer_interaction.event_id)

    activities += answer_creation_interactions

    if include_submodules:
        for submodule in makey.modules_used.all():
            activities += get_makey_activities(submodule, True)

    #sorting according to date of interaction
    activities = sorted(activities, key=lambda x: x.added_time,
                        reverse=True)

    return activities

def get_user_notifications(user):
    if not user:
        return []

    notifs = UserNotification.objects.filter(user=user, read=False).order_by('-added_time')

    return notifs


def get_makey_insights(makey, include_submodules=False):
    insights = []

    if not makey:
        return insights

    insights += makey.notes.exclude(is_pending_approval=True)

    if include_submodules:
        for submodule in makey.modules_used.all():
            insights += get_makey_insights(submodule, True)

    # insights = sorted(insights, key=lambda x: x.added_time,
    #                     reverse=True)

    return insights
class GitlabIntegeration:
  
  def __init__(self,token,host):
    self.auth_token = token
    self.host = host
    self.git = gitlab.Gitlab(host=self.host,token=self.auth_token)
  
  
  def getFiles(self,projectID,params):
    return self.git.getrepositorytree(projectID,**params)
 
  
  def getAllcommits(self,projectID,refName):
    preurl = "http://git.makeystreet.com/api/v3/projects/"
    posturl = "/repository/commits"
    url = preurl+str(projectID)+posturl
    params = {}
    params['private_token'] = self.auth_token
    params['ref_name'] = refName
    r = requests.get(url,data= params)
    return r.text
  
   
  def getProjects(self):
    return self.git.getprojects()
  
  #gets the commits for a particular file. Don't know why Gitlab gives the latest commit , even though the file under consideration was not
  #changed in it.
  def getCommitData(self,Name,projectID,tree):
    if tree != None:
     Name = tree+'/'+Name
    data = self.git.getfile(projectID,Name,'master')
    commit = self.git.getrepositorycommit(projectID,data['commit_id'])
    return commit
