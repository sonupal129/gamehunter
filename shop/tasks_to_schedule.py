from carts.tasks import delete_old_cart

# Code Starts Below

task_to_schedule = {}
task_to_schedule["daily-tasks"] = []
task_to_schedule["weekly-tasks"] = [delete_old_cart]
task_to_schedule["biweekly-tasks"] = []
