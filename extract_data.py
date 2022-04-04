import os
import csv
file = open("extracted_data.csv",encoding='latin1')

data = csv.reader(file)
header = next(data)

d = {}
unit_price = {}
count = 1

"""
Required format for unit price : {'WHITE HANGING HEART T-LIGHT HOLDER': 2.55, 'WHITE METAL LANTERN': 3.39, 'CREAM CUPID HEARTS COAT HANGER': 2.75, 'KNITTED UNION FLAG HOT WATER BOTTLE': 3.39}
"""
for row in data:
	if row[0] not in d:
		d[row[0]] = [(row[1],int(row[2]))]
	else:
		d[row[0]].append((row[1],int(row[2])))
	if row[1] not in unit_price:
		unit_price[row[1]] = float(row[3])
file.close()

transaction = []
"""
Required format of Transcation Data : [(1, [('WHITE HANGING HEART T-LIGHT HOLDER', 6), ('WHITE METAL LANTERN', 6), ('CREAM CUPID HEARTS COAT HANGER', 8), ('KNITTED UNION FLAG HOT WATER BOTTLE', 6), ('RED WOOLLY HOTTIE WHITE HEART.', 6), ('SET 7 BABUSHKA NESTING BOXES', 2), ('GLASS STAR FROSTED T-LIGHT HOLDER', 6)]), (2, [('HAND WARMER UNION JACK', 6),
"""
count = 1
for i in d:
	transaction.append((count,d[i]))
	count += 1

file = open("transcation_data.txt","w+")
file.write("{}".format(transaction))
file.close()



file = open("unit_price.txt","w+")
file.write("{}".format(unit_price))
file.close()
