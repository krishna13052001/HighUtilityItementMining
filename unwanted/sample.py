import unitprice
import transcationData as td
print("hi")
print(td.get_transactional_data())
# print(unitprice.get_unit_price())
print("bye")

def get_unit_price():
    for item in unit_price:
        unit_price[item] = float(unit_price[item])
    return unit_price