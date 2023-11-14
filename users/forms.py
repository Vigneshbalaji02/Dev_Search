from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm ,widgets
from .models import Profile, skill, message




class customusercreationform(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name", "email","username","password1","password2"]
        labels={
            'first_name':"Name"
        }
    def __init__(self, *args, **kwargs):
        super(customusercreationform, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update({"class":"input","placeholder":"First name"})
        self.fields["email"].widget.attrs.update({"class":"input","placeholder":"Email"})
        self.fields["username"].widget.attrs.update({"class":"input","placeholder":"Username"})
        self.fields["password1"].widget.attrs.update({"class":"input","placeholder":"Password"})
        self.fields["password2"].widget.attrs.update({"class":"input","placeholder":"Confirm password"})

class Profileform(ModelForm):
    class Meta:
        model=Profile
        fields=["name","email","username","location","short_intro","bio","profile_image","social_github","social_twitter","social_linkedin"]

    def __init__(self, *args, **kwargs):
        super(Profileform, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"class":"input","placeholder":"Name"})
        self.fields["email"].widget.attrs.update({"class":"input","placeholder":"Email"})
        self.fields["username"].widget.attrs.update({"class":"input","placeholder":"Username"})
        self.fields["location"].widget.attrs.update({"class":"input","placeholder":"Current location"})
        self.fields["short_intro"].widget.attrs.update({"class":"input","placeholder":"Short intro"})
        self.fields["bio"].widget.attrs.update({"class":"input","placeholder":"Bio"})
        self.fields["profile_image"].widget.attrs.update({"class":"input"})
        self.fields["social_github"].widget.attrs.update({"class":"input","placeholder":"Github link"})
        self.fields["social_twitter"].widget.attrs.update({"class":"input","placeholder":"Twitter link"})
        self.fields["social_linkedin"].widget.attrs.update({"class":"input","placeholder":"Linkedin"})


class skillform(ModelForm):
    class Meta:
        model=skill
        fields='__all__'
        exclude=["owner"]

    def __init__(self, *args, **kwargs):
        super(skillform, self).__init__(*args, **kwargs)

        for name,filed in self.fields.items():
            filed.widget.attrs.update({"class":"input"})


class messagefrom(ModelForm):
    class Meta:
        model=message
        fields=['name', 'email', 'subject', 'body']


    def __init__(self, *args, **kwargs):
        super(messagefrom, self).__init__(*args, **kwargs)

        for name,filed in self.fields.items():
            filed.widget.attrs.update({"class":"input"})

