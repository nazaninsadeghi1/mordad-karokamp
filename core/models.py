from django.db import models
from datetime import datetime

class CityChoices(models.TextChoices):
    TEHRAN = ('tehran', 'تهران')
    ISFAHAN = ('isfahan', 'اصفهان')


class ShowToChoices(models.TextChoices):
    NOBODY = ('nobody','هیجکس')
    CLOSEFRIENDS = ('closefriends','دوستان صمیمی')
    ALL = ('all','همه')

# class GenderChoices(models.TextChoices):
    # MALE = ('male','مرد')
    # FEMALE = ('femail','زن')

class CategoryChoices(models.TextChoices):
    SOCIAL = ('social','اجتماعی')
    SPORT = ('sport','ورزشی')
        

class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name='نام کاربری')
    password = models.CharField(max_length=20, verbose_name='گذرواژه')
    birthdate = models.DateField(null=True, verbose_name='تاریخ تولد')
    bio = models.TextField(null=True,verbose_name='بیوگرافی')
    city = models.CharField(max_length=20, choices=CityChoices.choices, default=CityChoices.ISFAHAN, verbose_name='شهر')
    email = models.EmailField(verbose_name='ایمیل')
    close_friend = models.ManyToManyField(to='self',null=True,blank=True, verbose_name='دوستان صمیمی')
    # gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    
    def __str__(self):
        return f'{self.username}'
    
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'



admin_user = User.objects.filter(username='admin').first()


class Post(models.Model):
    title = models.CharField('عنوان',max_length=50)
    content = models.TextField('توضیحات')
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True,blank=True ,verbose_name='کاربر')
    created_at = models.DateTimeField('تاریخ ایجاد ',auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ آخرین بروزرسانی',auto_now=True)
    visible = models.BooleanField('قابل مشاهده',default=False)
    show_to = models.CharField('نمایش برای',
        max_length=20 , choices=ShowToChoices.choices, default=ShowToChoices.NOBODY
        )
    is_deleted = models.BooleanField('حذف شده',default=False)
    category = models.CharField(max_length=20, choices= CategoryChoices,verbose_name='دسته بندی')
    image = models.ImageField(upload_to=f"post_pictures/{datetime.now().strftime('%Y%m%d')}", null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name= 'پست'
        verbose_name_plural= 'پست'
