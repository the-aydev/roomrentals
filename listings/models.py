from django.db import models
from datetime import datetime
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Listing(models.Model):
    class Kitchen(models.TextChoices):
        YES = 'Yes'
        NO = 'No'

    class Price(models.TextChoices):
        TENK = '#10,000'
        TWENTYK = '#20,000'
        THIRTYK = '#30,000'
        FORTYK = '#40,000'
        FIFTYK = '#50,000'
        SIXTYK = '#60,000'
        SEVENTYK = '#70,000'
        EIGHTYK = '#80,000'
        NINETYK = '#90,000'
        HUNDREDK = '#100,000'
        ONETWENTYK = '#120,000'
        ONEFIFTYK = '#150,000'
        TWOHUNDREDK = '#200,000'
        TWOFIFTYK = '#250,000'
        THREEHUNDREDK = '#300,000'
        THREEFIFTYK = '#350,000'
        FOURHUNDREDK = '#400,000'
        FOURFIFTYK = '#450,000'
        FIVEHUNDREDK = '#500,000'
        FIVEFIFTYK = '#550,000'
        SIXHUNDREDK = '#600,000'
        SIXFIFTYK = '#650,000'
        SEVENHUNDREDK = '#700,000'
        SEVENFIFTYK = '#750,000'
        EIGHTHUNDREDK = '#800,000'
        NINEHUNDREDK = '#900,000'
        ONEMILLI = '1M+'

    class State(models.TextChoices):
        ABIA = 'Abia'
        ADAMAWA = 'Adamawa'
        AKWAIBOM = 'Akwa Ibom'
        ANAMBRA = 'Anambra'
        BAUCHI = 'Bauchi'
        BAYELSA = 'Bayelsa'
        BENUE = 'Benue'
        BORNO = 'Borno'
        CROSSRIVER = 'Cross River'
        DELTA = 'Delta'
        EBONYI = 'Ebonyi'
        EDO = 'Edo'
        EKITI = 'Ekiti'
        ENUGU = 'Enugu'
        GOMBE = 'Gombe'
        IMO = 'Imo'
        JIGAWA = 'Jigawa'
        KADUNA = 'Kaduna'
        KANO = 'Kano'
        KATSINA = 'Katsina'
        KEBBI = 'Kebbi'
        KOGI = 'Kogi'
        KWARA = 'Kwara'
        LAGOS = 'Lagos'
        NASARAWA = 'Nasarawa'
        NIGER = 'Niger'
        OGUN = 'Ogun'
        ONDO = 'Ondo'
        OSUN = 'Osun'
        OYO = 'Oyo'
        PLATEAU = 'Plateau'
        RIVERS = 'Rivers'
        SOKOTO = 'Sokoto'
        TARABA = 'Taraba'
        YOBE = 'Yobe'
        ZAMFARA = 'Zamfara'
        ABUJA = 'F.C.T'

    class Garage(models.TextChoices):
        YES = 'Yes'
        NO = 'No'

    class Garden(models.TextChoices):
        YES = 'Yes'
        NO = 'No'

    class AirCondition(models.TextChoices):
        YES = 'Yes'
        NO = 'No'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedroom = models.IntegerField(default=1)
    kitchen = models.CharField(
        max_length=4, choices=Kitchen.choices, default=Kitchen.NO)
    garage = models.CharField(
        max_length=4, choices=Garage.choices, default=Garage.NO)
    garden = models.CharField(
        max_length=4, choices=Garden.choices, default=Garden.NO)
    air_condition = models.CharField(
        max_length=4, choices=AirCondition.choices, default=AirCondition.NO)
    extras = models.CharField(max_length=200)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    verified = models.BooleanField(default=False)

    def delete(self):
        self.main_photo.storage.delete(self.main_photo.name)
        self.photo_1.storage.delete(self.photo_1.name)
        self.photo_2.storage.delete(self.photo_2.name)
        self.photo_3.storage.delete(self.photo_3.name)

        # This allows us to perform the standard delete except we do this part as well
        super().delete()

    def __str__(self):
        return self.title
