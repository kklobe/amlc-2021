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
Price = 90  # $/[1000km * unit]

# %%
model = gp.Model("AMLC2021")

x = model.addVars(DC, FC, name='flow')

model.addConstrs((x.sum(i,'*') <= Capacity[i] for i in DC), name='Capacity')
model.addConstrs((x.sum('*',j) >= Demand[j] for j in FC), name='Demand')

model.setObjective(Price*x.prod(Distances))


# %%
model.optimize()

# %%
for v in x:
    print(f'{v}: {x[v].x}')

# %%
model.ObjVal

# %%
