from django import forms
from .models import Response, Match
from django.contrib.auth.forms import UsernameField  

class LoginForm(forms.Form):  
    """ログイン画⾯⽤のフォーム"""  
    username = UsernameField(  
        label='ユーザー名',  
        max_length=255,  
    )  
    password = forms.CharField(  
        label='パスワード',  
        strip=False,  
        widget=forms.PasswordInput(render_value=True),  
    ) 


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
            'result': forms.Select(choices=JANKEN)
        }
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['result']