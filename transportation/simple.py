# %% [markdown]
# # Introduction
# The `gurobipy` API is Gurobi's own Python API. It is generally the recommended way of interacting with Gurobi, 
# as it is optimized for performance and contains all the latest features of the product.
#
# In this example, we will see how to formulate a very simple transportation problem using `gurobipy`.
#
# ## Data
# We use some very simple data to get started:

# %%
import gurobipy as gp
import time


DC = ['seattle','san-diego']
FC = ['new-york','chicago', 'topeka']
Capacity = {'seattle':350,'san-diego':600}
Demand = {'new-york':325,'chicago':300,'topeka':275}
Distances = {
    ('seattle',  'new-york') : 2.5,
    ('seattle',  'chicago')  : 1.7,
    ('seattle',  'topeka')   : 1.8,
    ('san-diego','new-york') : 2.5,
    ('san-diego','chicago')  : 1.8,
    ('san-diego','topeka')   : 1.4,
}
Price = 90
