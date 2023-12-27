from django.contrib import admin
from .models import MCQ, Import,UserQuestions,UserInfo

# admin.site.register(MCQ)
class questions(admin.ModelAdmin):
    list_display = ['question', 'options', 'answer',]
class user_questions(admin.ModelAdmin):
    list_display = ['user','encoded_id', 'used_question' ]
class user_info(admin.ModelAdmin):
    list_display = ['user','correct','incorrect','phone']
# Register your models here.
admin.site.register(MCQ, questions)
admin.site.register(Import)
admin.site.register(UserQuestions, user_questions)
admin.site.register(UserInfo, user_info)