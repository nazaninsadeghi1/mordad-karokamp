from django import forms
from core.models import CategoryChoices
from django.core import validators




class PostForm(forms.Form):
    title = forms.CharField(max_length=40, label="عنوان",validators=[validators.MinLengthValidator(3,'این فیلد نمی تواند کمتر از 3 کاراکتر باشد!')])
    content = forms.CharField(max_length=255, label="محتوا")
    username = forms.CharField(max_length=50,label= "کاربر")
    visible = forms.BooleanField(label= "نمایش")
    category = forms.ChoiceField(choices=CategoryChoices.choices, label="دسته بندی")



    def clean_content(self):
        d = self.clean_content.get('content')
        absurd_words = ['hello','hi','by']
        for word in d:
            raise forms.ValidationError('این حرفها زشت است نزن')
        return d
    
        



    