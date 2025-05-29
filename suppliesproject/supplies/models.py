from django.db import models
# Create your models here.
CATEGORY = (
    ('tool', '道具'),
    ('consumable', '消耗品'),
    ('other', 'その他')
)

RATE_CHOICES = (
    (1,'★☆☆☆☆'),
    (2,'★★☆☆☆'),
    (3,'★★★☆☆'),
    (4,'★★★★☆'),
    (5,'★★★★★'),
)

LEND = ((i, str(i)) for i in range(1,100))

class Supplies(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    category = models.CharField(
        max_length=100,
        choices = CATEGORY
    )
    tag = models.CharField(max_length=100,null=True, blank=True)
    lend = models.IntegerField(null=True, blank=True, default=0)
    allsupplies = models.IntegerField(null=True, blank=True)
    stamp = models.IntegerField(null=True, blank=True, default=0)
    borrowed = models.IntegerField(null=True, blank=True,default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.title

class Lendingsupplies(models.Model):
    lend = models.IntegerField(choices=LEND)
    date = models.DateField()
    destruction = models.IntegerField(default=0, choices=LEND)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lendid = models.ForeignKey(Supplies, on_delete=models.CASCADE)

    def __str__(self):
        return self.lendid.title

class Review(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    supplies = models.ForeignKey(Supplies,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

