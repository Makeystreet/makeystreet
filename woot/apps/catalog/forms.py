from chosen import widgets as chosenwidgets
from django import forms

from models.core import Product
from models.misc import List, ListItem  # ,Email_collect


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


# class emailform(forms.ModelForm):
#     class Meta:
#         model = Email_collect
#         fields = ('email', 'full_name')
class TutorialForm(forms.Form):
    url = forms.URLField()


class MakeyForm(forms.Form):
    url = forms.URLField()
    name = forms.CharField()


class ListEditForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.none(),
                                              required=False)

    def __init__(self, *args, **kwargs):
        super(ListEditForm, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = Product.objects.all()

        instance = kwargs.pop('instance', None)
        # Need to convert the list_items from instance to product items
        if instance:
            for i in instance.items.all():
                print i.product
                if self.fields['products'].initial is None:
                    self.fields['products'].initial = [i.product]
                else:
                    self.fields['products'].initial.append(i.product)

    class Meta:
        model = List
        #fields = ('unique_id', 'phone_number', 'hostel', 'room_no')
        exclude = ('items',)
        widgets = {
            'products': chosenwidgets.ChosenSelectMultiple(),
            'access': chosenwidgets.ChosenSelectMultiple(),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        my_list = List()

        # Handle other data
        my_list.name = self.cleaned_data['name']
        my_list.owner = self.cleaned_data['owner']
        my_list.is_private = self.cleaned_data['is_private']

        my_list.save()  # Save so that M2M can be saved
        # Get products and make list items
        for p in self.cleaned_data['products']:
            l_i = ListItem()
            l_i.product = p
            l_i.save()
            my_list.items.add(l_i)
        my_list.access = self.cleaned_data['access']

        if commit:
            my_list.save()
        return my_list


class SearchForm(forms.Form):
    q = forms.CharField()

class EmailForm(forms.Form):
    email = forms.EmailField()

class CreateMakeyForm(forms.Form):
    val_name = forms.CharField(required=False)  # Name
    val_about = forms.CharField(required=False)  # What
    val_privacy = forms.CharField(required=False)
    status_chosen = forms.CharField(required=False)  # Status

class DeleteMakeyForm(forms.Form):
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)

class UserOnboardForm(forms.Form):
    spaces = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    users = forms.CharField(required=False)


class CreateProductReviewForm(forms.Form):
    val_part = forms.CharField()
    val_title = forms.CharField()
    val_review = forms.CharField()
    val_rating = forms.IntegerField()


class CreateShopReviewForm(forms.Form):
    val_shop = forms.CharField()
    val_title = forms.CharField()
    val_review = forms.CharField()
    val_rating = forms.IntegerField()


class CreateSpaceReviewForm(forms.Form):
    val_space = forms.CharField()
    val_title = forms.CharField()
    val_review = forms.CharField()
    val_rating = forms.IntegerField()


class CreateListingForm(forms.Form):
    val_title = forms.CharField()
    val_company = forms.CharField()
    val_listing = forms.CharField()


class UpdateImageForm(forms.Form):
    image_id = forms.CharField()
    small_url = forms.URLField()
    large_url = forms.URLField()
    full_url = forms.URLField()


class CreateArticleForm(forms.Form):
    title = forms.CharField()
    desc = forms.CharField(required=False)
    reco = forms.CharField()
    image_url = forms.URLField(required=False)
    url = forms.URLField()
    tags = forms.CharField(required=False)
    user = forms.CharField(required=False)


class CreateMakerForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    image_url = forms.URLField(required=False)


class ReplaceMakerForm(forms.Form):
    user_source = forms.CharField()
    user_target = forms.CharField()


class EditArticleForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(required=False)
    recommendation = forms.CharField()
    image_url = forms.URLField(required=False)
    tags = forms.CharField(required=False)


class ArticleEmailForm(forms.Form):
    email_id = forms.EmailField()
    tags = forms.CharField(required=False)
    users = forms.CharField(required=False)
    temp_id = forms.CharField()
    step = forms.CharField()
    redirect = forms.URLField(required=False)


class QuestionForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()


class AnswerForm(forms.Form):
    title = forms.CharField(required=False)
    description = forms.CharField()


class CommentForm(forms.Form):
    owner = forms.CharField()
    body = forms.CharField()
    question = forms.IntegerField()


class AddInsightForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)

class AskQuestionForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)

class AddInsightCommentForm(forms.Form):
    body = forms.CharField(required=True)
    action = forms.CharField(required=True)
    insight_id = forms.IntegerField(required=True)
    makey_id = forms.IntegerField(required=True)

class AddAnswerCommentForm(forms.Form):
    body = forms.CharField(required=True)
    action = forms.CharField(required=True)
    answer_id = forms.IntegerField(required=True)
    makey_id = forms.IntegerField(required=True)

class AddQuestionCommentForm(forms.Form):
    body = forms.CharField(required=True)
    action = forms.CharField(required=True)
    question_id = forms.IntegerField(required=True)
    makey_id = forms.IntegerField(required=True)

class AddImageCommentForm(forms.Form):
    body = forms.CharField(required=True)
    action = forms.CharField(required=True)
    image_id = forms.IntegerField(required=True)
    makey_id = forms.IntegerField(required=True)

class UpvoteInsight(forms.Form):
    insight_id = forms.IntegerField(required=True)
    makey_id = forms.IntegerField(required=True)
    action = forms.CharField(required=True)

class WatchMakey(forms.Form):
    makey_id = forms.IntegerField(required=True)
    action = forms.CharField(required=True)

class AddImageForm(forms.Form):
    makey_id = forms.IntegerField(required=True)
    action = forms.CharField(required=True)

class AddVideoForm(forms.Form):
    makey_id = forms.IntegerField(required=True)
    action = forms.CharField(required=True)
    url = forms.URLField(required=True)
    site = forms.IntegerField(required=True)

class AddFileForm(forms.Form):
    makey_id = forms.IntegerField(required=True)
    action = forms.CharField(required=True)
    file_url = forms.URLField(required=True)
    file_name = forms.CharField(required=True)
    file_type = forms.CharField(required=False)
    file_desc = forms.CharField(required=False)

class AddCollaboratorForm(forms.Form):
    makey_id = forms.IntegerField(required=True)
    action = forms.CharField(required=True)
    user_id = forms.IntegerField(required=True)

class RemoveCollaboratorForm(forms.Form):
    makey_id = forms.IntegerField(required=True)
    action = forms.CharField(required=True)
    user_id = forms.IntegerField(required=True)

class AddInsightImageForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)
    image_id = forms.IntegerField(required=False)
    image_url = forms.URLField(required=False)

class EditInsightImageForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)
    insight_id = forms.IntegerField(required=True)
    image_id = forms.IntegerField(required=False)
    image_url = forms.URLField(required=False)

class DeleteInsightForm(forms.Form):
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)
    insight_id = forms.IntegerField(required=True)

class EditMakeyNameDescForm(forms.Form):
    action = forms.CharField(required=True)
    makey_name = forms.CharField(required=True)
    makey_desc = forms.CharField(required=True)
    makey_id = forms.CharField(required=True)
    makey_github = forms.CharField(required=False)

class AddAnswerForm(forms.Form):
    description = forms.CharField(required=True)
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)
    question_id = forms.IntegerField(required=True)

class AddDocForm(forms.Form):
    title = forms.CharField(required=True)
    body = forms.CharField(required=True)
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)


class AddBOMForm(forms.Form):
    name = forms.CharField(required=True)
    quantity = forms.IntegerField(required=True)
    comments = forms.CharField(required=False)
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)

class EditBOMForm(forms.Form):
    bom_id = forms.IntegerField(required=True)
    name = forms.CharField(required=True)
    quantity = forms.IntegerField(required=True)
    comments = forms.CharField(required=False)
    action = forms.CharField(required=True)
    makey_id = forms.IntegerField(required=True)

class DeleteBOMForm(forms.Form):
    bom_id = forms.IntegerField(required=True)
    action = forms.CharField(required=True)

class AddIssueForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(required=False)

class AddIssueCommentForm(forms.Form):
    body = forms.CharField(required=True)
    action = forms.CharField(required=True)

class AddIssueAssigneeForm(forms.Form):
    user_id = forms.IntegerField(required=False)
    action = forms.CharField(required=True)

class AddMilestoneForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    date_of_completion = forms.CharField(required=True)

class AddIssueMilestoneForm(forms.Form):
    issue_id = forms.IntegerField(required=True)
    milestone_id = forms.IntegerField(required=True)
