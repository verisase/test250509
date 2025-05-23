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


class Supplies(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    category = models.CharField(
        max_length=100,
        choices = CATEGORY
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    supplies = models.ForeignKey(Supplies,on_delete=models.CASCADE)

    def __str__(self):
        return self.title