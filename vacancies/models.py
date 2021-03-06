from django.db import models
from django.db.models.indexes import Index
from ckeditor_uploader.fields import RichTextUploadingField
from mainapp.models import Category
from orgs.models import Employer
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.

class Level(models.Model):
    LEVEL_CHOICES = (
        ('I', '1 уровень'),
        ('II', '2 уровень'),
        ('III', '3 уровень'),
        ('IV', '4 уровень'),
        ('не требуется', 'без аттестации НАКС'),
    )
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    """base class for vacancy model"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(u"Название", max_length=80)
    employer = models.ForeignKey(Employer, blank=True, null=True, on_delete=models.CASCADE)
    salary_min = models.IntegerField(u'Зарплата от', blank=True)
    salary_max = models.IntegerField(u'Зарплата до', blank=True, null=True)
    naks_att_level = models.ManyToManyField(Level, verbose_name="Уровень аттестации НАКС") 
    business_trips = models.BooleanField(verbose_name="Вакансия с командировками", default=False)
    shift_work = models.BooleanField(verbose_name="Вахтовый метод работы", default=False)
    short_description = models.CharField(
        u'Краткое описание вакансии', max_length=200)
    description = RichTextUploadingField(blank=True, verbose_name='Описание вакансии') 
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(u'Дата создания', default=timezone.now)
    published = models.BooleanField(
        verbose_name='Опубликовать в ленте вакансий', default=False)

    class Meta:
        ordering = ['created_date']
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        indexes = [
            models.Index(fields=['salary_min', 'salary_max']),
        ]
    
    def __str__(self):
        return self.title