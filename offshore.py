import pandas as pd

# Read in the data
df = pd.read_excel('offshore.xlsx')
price_per_km = 1e6
capacity = 65 # Amount of MW that a cable can carry
produced = 8