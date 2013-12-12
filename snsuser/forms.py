# -*- coding: utf-8 -*-
"""
入力値検証用のフォームを定義するファイルです。ファイル名に規則はありませんが、慣例でforms.pyに記述します。
"""
#国際化の宣言を行うugettextを便利のために_という別名でインポートしています。
from django.utils.translation import ugettext as _
from django import forms

from django.contrib.auth.models import User
from models import SnsUser

def check_unique_email(email):
    """
    渡されたメールアドレスが有効なユーザに利用されていないかを検証する関数です。
    """
    try :
        #同一のメールアドレスを持つユーザを抽出しています。Model.Manager.getは条件に合うデータが無い場合にModel.DoesNotExist例外を送出します
        User.objects.get(email=email, is_active=True)
        #条件に合うデータがある場合にのみこのロジックを通ります。つまり、既に同一のメールアドレスを持つユーザがいた場合です。
        #検証関数は検証に問題がある場合にforms.ValidationErrorを送出する決まりになっています。
        raise forms.ValidationError, _(u"This email address is already in use.")
    except User.DoesNotExist:
        #検証関数は検証に問題が無いので、メールアドレスを返します
        return email

class SendKeyForm(forms.Form):
    """
    入力値の検証フォームです。特定のモデルと関わりがない場合には、django.forms.Formを継承したクラスとして宣言します。
    """
    #メールアドレスとしての検証を行うためのフォームフィールドをemailという名前の入力値に対して指定しています
    email = forms.EmailField()
    
    def clean_email(self):
        """
        emailという入力値に対する検証です。clean_入力名関数は、form検証時に自動で呼び出されます。ただし、フォームフィールドの検証が通った場合のみ呼び出されます。
        検証に問題がない場合には、Pythonの型に変換して返します。emailは入力もPython型も文字列型なので、文字列を返しています。
        """
        #フォームフィールドの検証が通った後に呼び出されますので、self.cleaned_dataにemailという名前で文字列として格納されています。
        value = self.cleaned_data.get('email')
        #フォームフィールドとして単純に検証できない検証をここで行います。
        return check_unique_email(value)

class CreateUserForm(forms.ModelForm):
    """
    ユーザ登録用の検証フォームです
    """
    email = forms.EmailField(widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        #SnsUserを元に検証フォームを自動生成します
        model = SnsUser
        #SnsUserのフィールドのうち、指定のもののみを検証対象にします
        fields = ('email', 'username', 'password', 'nickname', )
    
    def clean_email(self):
        value = self.cleaned_data.get('email')
        return check_unique_email(value)

    def clean_username(self):
        """
        ユーザ名が既に利用されていないかを検証します。
        """
        value = self.cleaned_data.get('username')
        try:
            User.objects.get(username__iexact=value)
            raise forms.ValidationError, _(u"This username is already taken.")
        except User.DoesNotExist:
            return value

class UploadIconForm(forms.Form):
    """
    アイコン画像アップロード用の検証フォームです
    """
    #画像ファイルのみを受け付ける設定をします
    icon = forms.ImageField()

