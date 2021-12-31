from django.db import models

# Create your models here.
#Userをインポートする必要があるので、以下Userを追加しましょう。
from django.contrib.auth.models import User
from django.utils import timezone
from multiselectfield import MultiSelectField

SCORE_CHOICES =(
    ('スーパーマーケット','スーパーマーケット'),
    ('小学校', '小学校'),
    ('中学校','中学校'),
    ('公園','公園'),
    ('神社','神社'),
    ('スターバックスコーヒー', 'スターバックス'),
    ('ブルーボトルコーヒー','ブルーボトルコーヒー'),
    ('成城石井', '成城石井'),
    ('無印良品','無印良品'),
    ('マクドナルド', 'マクドナルド'),
    ('KFC', 'ケンタッキー'),
)

class Score(models.Model):
    name = models.CharField(max_length=200, verbose_name="駅名①")
    name_sub = models.CharField(max_length=200, blank=True, null=True, verbose_name="駅名②")
    choice = MultiSelectField(
        choices = SCORE_CHOICES,
        )

    def __str__(self): 
        return self.name