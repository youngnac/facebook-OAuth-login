from django import forms


class PostLikeForm(forms.Form):
    post_number = forms.IntegerField(min_value=1, max_value=50)
