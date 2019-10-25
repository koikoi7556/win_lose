from django.db import models
from django.utils import timezone

class Match(models.Model):
    """
    ユーザーの勝ち負けを保存するモデル
    """

    # userが削除されても勝ち負け結果は、基本統計などに用いるため保存。
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    user_hand = models.IntegerField(verbose_name='自分の手')
    opponent_hand = models.IntegerField(verbose_name='相手の手')
    result = models.IntegerField(verbose_name='勝負結果')
    match_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}_{}'.format(self.user, self.match_time)

class Comment(models.Model):
    """
    勝ち負け時の画像とコメントを保存するモデル
    """
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    image_link = models.TextField(verbose_name='画像リンク', max_length=200)
    comment = models.TextField(verbose_name='コメント', max_length=1000)
    result = models.IntegerField(verbose_name='表示する場合の結果')
    createde_date = models.DateField(default=timezone.now)

    def __str__():
        return comment[:10]

