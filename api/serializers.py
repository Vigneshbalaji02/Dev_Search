from rest_framework import serializers
from web.models import Project, Tag
from users.models import Profile



class Profileserializers(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"


class Tagserializers(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields="__all__"


class Projectserializers(serializers.ModelSerializer):
    owner = Profileserializers(many=False)
    tags = Tagserializers(many=True)

    class Meta:
        model=Project
        fields="__all__"

