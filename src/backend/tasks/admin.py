from django.contrib import admin
from tasks.models import Task, TaskCompletion


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)

class TaskCompletionAdmin(admin.ModelAdmin):
    pass

admin.site.register(TaskCompletion, TaskCompletionAdmin)
