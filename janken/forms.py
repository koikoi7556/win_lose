from django import forms
from .models import Response, Match
from django.contrib.auth.forms import UsernameField  


JANKEN = (
    (-1, '負けのとき'),
    (0, 'あいこのとき'),
    (1, '勝ちのとき')
)


class ResponseForm(forms.ModelForm):
    class Meta:       
        model = Response
        fields = ['result', 'image_link', 'text']
        widgets = {
            'result': forms.Select(choices=JANKEN),
        }

    def clean_text(self):
        text = self.cleaned_data['text']  
        if len(text) < 5:
            raise forms.ValidationError('%(min_length)s 文字以上で入力してください', params={'min_length': 5})
        return text

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs = {'placeholder': '5文字以上', 'rows': '5'}
        self.fields['image_link'].widget.attrs = {'placeholder': 'プレビューで画像が表示されるか確認してください', 'rows': '4'}