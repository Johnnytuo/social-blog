from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):

    user = models.ForeignKey(User, default= None,on_delete=models.PROTECT)
    username = models.CharField(max_length=200)
    email = models.EmailField()
    sex = models.CharField(max_length=50)
    bio_text = models.CharField(max_length=200,editable= True)
    profile_pic = models.FileField(blank=False)
    content_type = models.CharField(max_length=50)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    zip = models.IntegerField(max_length=5)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    fav_cuisine = models.CharField(max_length=200)

    def _str_(self):
        return 'id= '+self.id+'text=" ' +self.bio+'"'


class HostPost(models.Model):

    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    content = models.CharField(max_length=200)
    samp_image = models.FileField(blank=True)
    image_type = models.CharField(max_length=50)
    cuisine_type = ArrayField(models.CharField(max_length=200), blank=True)
    create_datetime = models.DateTimeField()
    event_datetime = models.DateTimeField()
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    zip = models.IntegerField(max_length=5)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    num_guests = models.IntegerField()
    guest_list = ArrayField(models.IntegerField(), blank=True)


class Review(models.Model):

    user = models.ForeignKey(User, default= None,on_delete=models.PROTECT)
    username = models.CharField(max_length=200)
    event_id = models.ForeignKey(HostPost, default= None,on_delete=models.PROTECT)
    datetime = models.DateTimeField()
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(max_length=1)
    image = models.FileField(blank=True)
    image_type = models.CharField(max_length=50)
    tipping = models.IntegerField(max_length=5)

    def _str_(self):
        return 'id= '+self.id+'text=" ' +self.bio+'"'


class GuestPost(models.Model):

    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    content = models.CharField(max_length=200)
    cuisine_type = ArrayField(models.CharField(max_length=200), blank=True)
    create_datetime = models.DateTimeField()
    event_datetime = models.DateTimeField()
    status = models.BooleanField(default=True)
    host_id = models.ForeignKey(User, default= None,on_delete=models.PROTECT)
    event_id = models.ForeignKey(HostPost, default= None,on_delete=models.PROTECT)

class Transaction:
    event_id = models.ForeignKey(HostPost, default= None,on_delete=models.PROTECT)
    host_id = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    guests_list = ArrayField(models.IntegerField(), blank=True)