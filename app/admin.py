from django.contrib import admin
from .models import MCQ, Import,UserQuestions

# admin.site.register(MCQ)
class questions(admin.ModelAdmin):
    list_display = ['question', 'options', 'answer',]
# Register your models here.
admin.site.register(MCQ, questions)
admin.site.register(Import)
admin.site.register(UserQuestions)