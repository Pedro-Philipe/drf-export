from .models import User

def fill_spreadsheet(spreadsheet, queryset):
    spreadsheet.write(0, 0, "Name")
    spreadsheet.write(0, 1, "Job")
    spreadsheet.write(0, 2, "Age")

    last_line = 0

    users = queryset

    for i, user in enumerate(users, start=1):
        spreadsheet.write(i, 0, user.name)
        spreadsheet.write(i, 1, user.job)
        spreadsheet.write(i, 2, user.age)

        last_line = i

    return last_line