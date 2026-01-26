from datetime import datetime
from unittest.loader import VALID_MODULE_NAME
from xml.dom import ValidationErr
from django import forms
from core.models import  CityChoices
from core.models import User, Post



class PostForm(forms.ModelForm):
    tag = forms.CharField(max_length=40, widget=forms.TextInput(attrs={"class":"form-control"}),help_text="اینجا تگ با # وارد شود")
    
    # category = forms.ChoiceField(
    #     widget = forms.RadioSelect(attrs={"class":"form-radio"}),
    #     initial= CategoryChoices.SOCIAL,
    #     choices= CategoryChoices.choices,
    # )
    
    class Meta:
        model = Post
        fields = ["title", "content", "user", "visible", "show_to", "category", "tag"]
        widgets = {"content":forms.Textarea(attrs={"class":"form-control"}),
                   "category":forms.Select(attrs={"class":"form-radio"}),
                   }
        
        error_messages = {
            # "title":'این عنوان مناسب نیست'
            "title":{
                "required":'این فیلد اجباری است.',
                "max-length": 'این فیلد نمی تواند بیشتر از 50 کاراکتر باشد.'
            }
        }

# class PostForm(forms.Form):
#     title = forms.CharField(
#         max_length=40, required=True,
#         label="عنوان",
#         validators=[
#             validators.MinLengthValidator(
#             3,'این فیلد نمی تواند کمتر از 3 کاراکتر باشد!'
#             )
#         ],
#     )
#     content = forms.CharField(max_length=255, label="محتوا")
#     username = forms.CharField(max_length=50,label= "کاربر")
#     user = forms.ModelChoiceField(queryset=User.objects.all())
#     visible = forms.BooleanField(label= "نمایش")
#     category = forms.ChoiceField(choices=CategoryChoices.choices, label="دسته بندی")

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content)<3:
            raise forms.ValidationError ('این فیلد نمی تواند کمتر از 3 کاراکتر باشد')
        return content
    

    def clean(self):
        data = super().clean()
        title = data.get('title')
        content = data.get('content')
        if title not in content:
            raise forms.ValidationError("حتما باید عنوان در محتوا باشد")
        return data
        

    # def clean_content(self):
    #     d = self.clean_content.get('content')
    #     absurd_words = ['hello','hi','by']
    #     for word in d:
    #         raise forms.ValidationError('این حرفها زشت است نزن')
    #     return d
    
    # def clean_title(self):
    #     title= self.cleaned_data.get('title')
    #     if len(title) == 0:
    #         raise forms.ValidationError('این فیلد نمی تواند خالی باشد')
    #     return title
    
        

class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=30, label='نام کاربری')
    password = forms.CharField(
        max_length=40,
        label='گذرواژه',
        widget=forms.PasswordInput(attrs={"class":"form-control","plaseholder":"گذرواژه"}),
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={"type":"date","class":"form-control"}),
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class":"form-control"})
    )
    city = forms.ChoiceField(choices=CityChoices.choices, initial=CityChoices.ISFAHAN)
    email = forms.EmailField()
    close_friend = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class':'form-checkbox'}))


    def clean_birthdate(self):
        bd = self.cleaned_data.get('birthdate')
        if (datetime.now().date() - bd).days < 18 * 365:
            raise forms.ValidationError('کاربر بچه سال قبول نمی کنیم')
    
        return bd
    


    def clean(self):
        data = super().clean()
        username = data.get('username')
        password = data.get('password')
        if username in password:
            raise forms.ValidationError('نام کاربری نمی تواند بخشی از گذرواژه باشد')
        return data



    