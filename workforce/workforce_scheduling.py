# -*- coding: utf-8 -*-
# %% [markdown]
# # Workforce Scheduling Problem
#
# ## Objective and Prerequisites
#
# In this example, you’ll learn how to solve a critical, central problem in the services industry: workforce scheduling. We’ll demonstrate how you can use mathematical optimization to generate an optimal workforce schedule that meets your business requirements, maximizes employee fairness and satisfaction, and minimizes the number of temporary workers your company needs to hire.
#
# This modeling example is at the advanced level, where we assume that you know Python and the Gurobi Python API and that you have advanced knowledge of building mathematical optimization models. Typically, the objective function and/or constraints of these examples are complex or require advanced features of the Gurobi Python API.
#
# **Download the Repository** <br />
# You can download the repository containing this and other examples by clicking [here](https://github.com/Gurobi/modeling-examples/archive/master.zip). 
#
# **Gurobi License** <br />
# In order to run this Jupyter Notebook properly, you must have a Gurobi license. If you do not have one, you can request an [evaluation license](https://www.gurobi.com/downloads/request-an-evaluation-license/?utm_source=3PW&utm_medium=OT&utm_campaign=WW-MU-PRO-OR-O_LEA-PR_NO-Q3_FY20_WW_JPME_workforce-scheduling_COM_EVAL_GITHUB_&utm_term=workforce-scheduling-problem&utm_content=C_JPM) as a *commercial user*, or download a [free license](https://www.gurobi.com/academia/academic-program-and-licenses/?utm_source=3PW&utm_medium=OT&utm_campaign=WW-MU-PRO-OR-O_LEA-PR_NO-Q3_FY20_WW_JPME_workforce-scheduling_ACADEMIC_EVAL_GITHUB_&utm_term=workforce-scheduling-problem&utm_content=C_JPM) as an *academic user*.
#
# ## Motivation
# People are the most important asset for companies in the services industry as well as their largest source of costs.
# Workforce allocation and personnel scheduling deal with the arrangement of work schedules  and the assignment of personnel shifts in order to cover the demand for resources that vary over time.
#
# These problems are very important for companies in the services industries who rely on workforce resources such as:
# - Telephone operators
# - Hospital nurses
# - Policemen
# - Transportation personnel (plane crews, bus drivers, etc.)
# - Hospitality personnel
# - Restaurant personnel
#
# ## Problem Description
#
# Consider a service business, like a restaurant, that develops its workforce plans for the next two weeks (considering a 7-day week). The service requires only one set of skills. There are a number of employed workers with the same set of skills and with identical productivity that are available to work on some of the days during the two-week planning horizon. There is only one shift per workday. Each shift may have different resource (worker) requirements on each workday. The service business may hire extra (temp) workers from an agency to satisfy shift requirements. The service business wants to minimize the number of extra workers that it needs to hire, and as a secondary objective, it wants to balance the workload of employed workers to ensure fairness.

# %%
# This command imports the Gurobi functions and classes.

import gurobipy as gp
import pandas as pd

from pylab import *
import matplotlib
import matplotlib.pyplot as plt

# Number of workers required for each shift.
# The multidict function returns a list which maps each shift (key) to the number of workers required 
# by the shift duirng work day.
shifts, shiftRequirements = gp.multidict({
  "Mon1":  3,
  "Tue2":  2,
  "Wed3":  4,
  "Thu4":  4,
  "Fri5":  5,
  "Sat6":  6,
  "Sun7":  5,
  "Mon8":  2,
  "Tue9":  2,
  "Wed10": 3,
  "Thu11": 4,
  "Fri12": 6,
  "Sat13": 7,
  "Sun14": 5 })

# Amount each worker is paid to work one shift.
workers, pay = gp.multidict({
  "Amy":   10,
  "Bob":   12,
  "Cathy": 10,
  "Dan":   8,
  "Ed":    8,
  "Fred":  9,
  "Gu":    11 })

# Worker availability: defines on which day each employed worker is available.
# The Gurobi tuple list is a sub-class of the Python list class that is designed to efficiently
# support a usage pattern that is quite common when building optimization models. In particular, if a
# tuplelist is populated with a list of tuples, the select function on this class efficiently selects 
# tuples whose values match specified values in specified tuple fields. To give an example, the 
# statement l.select(1, ’*’, 5) would select all member tuples whose first field is equal to ’1’ and 
# whose third field is equal to ’5’. The ’*’ character is used as a wildcard to indicate that any 
# value is acceptable in that field.
availability = gp.tuplelist([
('Amy', 'Tue2'), ('Amy', 'Wed3'), ('Amy', 'Fri5'), ('Amy', 'Sun7'),
('Amy', 'Tue9'), ('Amy', 'Wed10'), ('Amy', 'Thu11'), ('Amy', 'Fri12'),
('Amy', 'Sat13'), ('Amy', 'Sun14'), ('Bob', 'Mon1'), ('Bob', 'Tue2'),
('Bob', 'Fri5'), ('Bob', 'Sat6'), ('Bob', 'Mon8'), ('Bob', 'Thu11'),
('Bob', 'Sat13'), ('Cathy', 'Wed3'), ('Cathy', 'Thu4'), ('Cathy', 'Fri5'),
('Cathy', 'Sun7'), ('Cathy', 'Mon8'), ('Cathy', 'Tue9'), ('Cathy', 'Wed10'),
('Cathy', 'Thu11'), ('Cathy', 'Fri12'), ('Cathy', 'Sat13'),
('Cathy', 'Sun14'), ('Dan', 'Tue2'), ('Dan', 'Wed3'), ('Dan', 'Fri5'),
('Dan', 'Sat6'), ('Dan', 'Mon8'), ('Dan', 'Tue9'), ('Dan', 'Wed10'),
('Dan', 'Thu11'), ('Dan', 'Fri12'), ('Dan', 'Sat13'), ('Dan', 'Sun14'),
('Ed', 'Mon1'), ('Ed', 'Tue2'), ('Ed', 'Wed3'), ('Ed', 'Thu4'),
('Ed', 'Fri5'), ('Ed', 'Sun7'), ('Ed', 'Mon8'), ('Ed', 'Tue9'),
('Ed', 'Thu11'), ('Ed', 'Sat13'), ('Ed', 'Sun14'), ('Fred', 'Mon1'),
('Fred', 'Tue2'), ('Fred', 'Wed3'), ('Fred', 'Sat6'), ('Fred', 'Mon8'),
('Fred', 'Tue9'), ('Fred', 'Fri12'), ('Fred', 'Sat13'), ('Fred', 'Sun14'),
('Gu', 'Mon1'), ('Gu', 'Tue2'), ('Gu', 'Wed3'), ('Gu', 'Fri5'),
('Gu', 'Sat6'), ('Gu', 'Sun7'), ('Gu', 'Mon8'), ('Gu', 'Tue9'),
('Gu', 'Wed10'), ('Gu', 'Thu11'), ('Gu', 'Fri12'), ('Gu', 'Sat13'),
('Gu', 'Sun14')
])

# %%
model = gp.Model("Scheduling")

y = model.addVars(availability, vtype=gp.GRB.BINARY, name='Tired')
x = model.addVars(workers, name='VeryTired')
n = model.addVars(shifts, name='ExhaustedGoGermany')
maxWork = model.addVar()
minWork = model.addVar()

model.addConstrs((y.sum('*',s) + n[s] == shiftRequirements[s] for s in shifts), 
                 name='JustGoToWork')
model.addConstrs((y.sum(w,'*') == x[w] for w in workers), name='Workers')

model.addConstr(maxWork == gp.max_(x), name="maxconstr")
model.addConstr(minWork == gp.min_(x), name="minconstr")

model.setObjectiveN(n.sum(), 0)
model.setObjectiveN(maxWork - minWork, 1)

# %%
model.optimize()

# %%
for v in y:
    if y[v].x > 0.5:
        print(v)

# %%
