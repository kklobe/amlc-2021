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
