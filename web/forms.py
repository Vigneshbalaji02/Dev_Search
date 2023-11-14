from django.forms import ModelForm, widgets
from .models import Project, Review
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields=["title","featured_images","descrition","demo_link","Source_link","tags"]
        #fields='__all__'

        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({"class":"input","placeholder":"Tiltle"})
        self.fields["descrition"].widget.attrs.update({"class":"input","placeholder":"Descrition"})
        self.fields["demo_link"].widget.attrs.update({"class":"input","placeholder":"Demo_link"})
        self.fields["Source_link"].widget.attrs.update({"class":"input","placeholder":"Source_link"})


class Reviewform(ModelForm):
    class Meta:
        model=Review
        fields=["value","body"]
        labels={
            'value':"Place your vote",
            'body': "Add a comment with your vote"
        }

    def __init__(self, *args, **kwargs):
        super(Reviewform, self).__init__(*args, **kwargs)

        self.fields["value"].widget.attrs.update({"class":"input"})
        self.fields["body"].widget.attrs.update({"class":"input","placeholder":"Add you comment"})

        #for name, filed in self.fields.items():
        #   filed.widget.attrs.update({"class":"input"})

            