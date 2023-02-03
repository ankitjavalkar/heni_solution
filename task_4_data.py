"""
Task 4.1

INNER JOIN: An inner join operation only returns rows where the join condition is true.
LEFT JOIN: This join returns all the rows of the table on the left side of the join and matches rows for the table on the right side of the join. In case there is no matching row on the right side, the result will contain NULL
RIGHT JOIN: Similar to Left Join, it returns all the rows of the table on the right side of the join and matching rows for the table on the left side of the join. In case there is no matching row on the left side, the result will contain null.
FULL JOIN: A result containing rows from both tables matching the specified condition, this is equivalent to combining the results of LEFT JOIN and RIGHT JOIN, any rows that do not have a match in the other table will be represented by null

Task 4.2

Prerequisites

Install the pandas package using the command:

pip install pandas

"""

import pandas as pd
flights = pd.read_csv("candidateEvalData/flights.csv")
airports = pd.read_csv("candidateEvalData/airports.csv")
weather = pd.read_csv("candidateEvalData/weather.csv")
airlines = pd.read_csv("candidateEvalData/airlines.csv")

flnamedf = flights.merge(airlines, on="carrier")
jbdf = flnamedf[flnamedf['name'].str.contains("JetBlue")]
dforigsort = jbdf.sort_values(by ='origin')
origcounts = dforigsort['origin'].value_counts()
origcountsdf = pd.DataFrame({'origin': origcounts.index, 'numFlights': origcounts.values})
result = origcountsdf[origcountsdf['numFlights']>100]
print(result)
