import pulp
import numpy as np

from helper import *


def schedule(employees, users, departments, day_requirement, days,
             department_names):

    if len(employees) == users:
        user_names = employees
    elif len(employees) < users:
        employees.extend(['User_{}'.format(i) for i in range(len(employees) + 1,
                                                             users + 1)])
        user_names = employees
    else:
        user_names = [employees[i] for i in range(users)]

    var = pulp.LpVariable.dicts('VAR', (range(departments), range(users),
                                        range(days)), 0, 1, 'Binary')
    problem = pulp.LpProblem('shift', pulp.LpMinimize)
    obj = None
    z = pulp.LpVariable.dicts('Z', (range(departments),
                                    range(users)), 0, 1, 'Binary')
    for h in range(departments):
        for user in range(users):
            obj += z[h][user]
    problem += obj
    for user in range(users):
        for h in range(departments):
            problem += z[h][user] <= pulp.lpSum(var[h][user][day]
                                                for day in range(days))
            problem += days * z[h][user] >= pulp.lpSum(var[h][user][day]
                                                       for day in range(days))
    for h in range(departments):
        for user in range(users):
            for day in range(days):
                obj += var[h][user][day]
    problem += obj
    for day in range(days):
        for h in range(departments):
            problem += pulp.lpSum(var[h][user][day]
                                  for user in range(users)) == \
                       day_requirement[h][day]
    for user in range(users):
        problem += pulp.lpSum([var[h][user][day] for day in range(days)
                               for h in range(departments)]) <= 6
    for user in range(users):
        for day in range(days):
            problem += pulp.lpSum([var[h][user][day]
                                   for h in range(departments)]) <= 1

    # Solve problem. We have a very complex solution so we set a timeout at
    # 10secs.
    status = problem.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=60))
    idx = pd.MultiIndex.from_product([department_names.values(), user_names],
                                     names=['department', 'User'])
    dashboard = pd.DataFrame(0, idx, wk_days)
    for h in range(departments):
        for user in range(users):
            for day in range(days):
                if var[h][user][day].value() > 0.001:
                    dashboard.loc[department_names[h],
                                  user_names[user]][wk_days[day]] = 1
    user_table = dashboard.groupby('User').sum()
    user_sums = user_table.sum(axis=1)
    # print(user_sums)
    day_sums = user_table.sum(axis=0)
    print("Status", pulp.LpStatus[status])
    return user_sums, dashboard, status, day_sums

