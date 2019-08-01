from shop.tasks import product_updater
from background_task.models import Task
from carts.tasks import delete_old_cart

task_to_schedule = {}

task_to_schedule["daily-tasks"] = [product_updater]
task_to_schedule["weekly-tasks"] = [delete_old_cart]
task_to_schedule["biweekly-tasks"] = []
task_obj = Task.objects.all()

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
