from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField (User, on_delete=models.CASCADE, related_name='userprofile')
    rank = models.IntegerField (default=-1)
    noShares = models.IntegerField (default=0)
    cash = models.IntegerField (default=380000)
    netWorth = models.IntegerField (default=0)
    isSU = models.BooleanField (default=False)
    noOfCompanies = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Company (models.Model):
    name = models.CharField (max_length=30)
    NumberOfshares = models.IntegerField (default=10)
    sharePrice = models.IntegerField (default=0)
    remainingShares = models.IntegerField(default=10)
    PEratio = models.FloatField (default=0.0)
    sixtyFlag = models.BooleanField (default=False)

    def __str__(self):
        return self.name


class UserTable (models.Model):
    profile = models.ForeignKey (Profile, on_delete=models.CASCADE )
    company = models.ForeignKey (Company, on_delete=models.CASCADE)
    noShares = models.IntegerField (default=0)
    pricesShare = models.IntegerField (default=0)
    total = models.IntegerField(default=0)
    #def __str__(self):
     #   return self.profile.user


class UserHistory (models.Model):
    profile = models.ForeignKey (Profile, on_delete=models.CASCADE)
    company = models.ForeignKey (Company, on_delete=models.CASCADE)
    noShares = models.IntegerField (default=0)
    pricesShare = models.IntegerField (default=0)
    buysell = models.IntegerField (default=0)
    total = models.IntegerField(default=0)



class BuyTable (models.Model):
    company = models.ForeignKey (Company, on_delete=models.CASCADE)
    profile = models.ForeignKey (Profile, on_delete=models.CASCADE)
    bidPrice = models.IntegerField (default=0)
    bidShares = models.IntegerField (default=0)
    buytime = models.DateTimeField(default=datetime.now,blank=True)
    #def __str__(self):
     #   return self.company.name

class SellTable (models.Model):
    company = models.ForeignKey (Company, on_delete=models.CASCADE)
    profile = models.ForeignKey (Profile, on_delete=models.CASCADE)
    sellPrice = models.IntegerField (default=0)
    sellShares = models.IntegerField (default=0)
    selltime = models.DateTimeField(default=datetime.now, blank=True)
    tenflag = models.BooleanField(default=False)
   # def __str__(self):
    #    return self.company.name


class News (models.Model):
    title = models.CharField (max_length=100)
    content = models.CharField (max_length=500)

class SU (models.Model):
    spread = models.IntegerField(default=0)
    sensex = models.FloatField(default=0)
    LiveText = models.CharField(max_length=100)
