from django.db import models
import uuid
from users.models import Profile
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True) 
    descrition = models.TextField(null=True,blank=True)
    featured_images= models.ImageField(null=True,blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    Source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField("Tag")
    vote_total=models.IntegerField(default=0, null=True,blank=True)
    vote_ratio=models.IntegerField(default=0, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio','-vote_total','title']


    @property
    def imageURL(self):
        try:
            url= self.featured_images.url
        except:
            url=''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset



    @property
    def votes(self):
        reviews=self.review_set.all()
        upvotes = reviews.filter(value='up').count()
        totalvalues = reviews.count()

        ratio=(upvotes / totalvalues) * 100
        self.vote_total = totalvalues
        self.vote_ratio = ratio
        self.save()

class Review(models.Model):
    VOTE_TYPE = (
        {"up", "upvote"},
        {"down", "downvote"}
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner','project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True) 
    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
