import pandas as p #for table data



df = p.read_csv("gdp_with_continent_filled.xlsx - GDP.csv") #reading and converting to table
#print(df.head()) #testing with first 5 rows

#print(df.info())

print(df.isnull().sum())

