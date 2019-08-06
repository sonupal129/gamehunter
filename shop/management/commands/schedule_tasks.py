from django.core.management import BaseCommand
from shop.tasks_to_schedule import task_to_schedule
from background_task.models import Task
# Code Starts Below

class Command(BaseCommand):
      help = "Schedule Custom Tasks"

      def handle(self, *args, **kwargs):
            repeater = {"daily-tasks": Task.DAILY, "weekly-tasks": Task.WEEKLY, "biweekly-tasks": Task.EVERY_2_WEEKS}
            for key, tasks in task_to_schedule.items():
                  for task in tasks:
                        obj = Task.objects.filter(task_name=task.name, queue=key)
                        if obj.count() == 0:
                              task(queue=key, repeat=repeater.get(key))
                        if obj.count() > 1:
                              obj.delete()
                              task(queue=key, repeat=repeater.get(key))
                        if obj.first().has_error():
                              obj.delete()
                              task(queue=key, repeat=repeater.get(key))
                        continue
            return "All Tasks Has Been Scheduled Sucessfully!"
