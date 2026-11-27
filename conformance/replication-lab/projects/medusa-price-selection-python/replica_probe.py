from copy import deepcopy

def price(pid,amount,list_id=None,list_type=None):
 return {"id":pid,"amount":str(amount),"raw_amount":{"value":str(amount),"precision":20},
  "currency_code":"eur","price_list_id":list_id,"price_list_type":list_type,
  "min_quantity":None,"max_quantity":None}
FIXTURES=[
 ("default-only",["ps-default"],[price("default-100",100)]),
 ("sale-below-default",["ps-sale-low"],[price("sale-80",80,"pl-sale","sale"),price("default-100",100)]),
 ("sale-above-default",["ps-sale-high"],[price("default-100",100),price("sale-120",120,"pl-sale","sale")]),
 ("sale-equal-default",["ps-sale-equal"],[price("sale-100",100,"pl-sale","sale"),price("default-100",100)]),
 ("override-only",["ps-override"],[price("override-90",90,"pl-override","override"),price("default-100",100)]),
 ("sale-below-override",["ps-sale-under-override"],[price("sale-80",80,"pl-sale","sale"),price("override-90",90,"pl-override","override"),price("default-100",100)]),
 ("override-below-sale",["ps-override-under-sale"],[price("override-90",90,"pl-override","override"),price("sale-95",95,"pl-sale","sale"),price("default-100",100)]),
 ("multiple-overrides-lowest-first",["ps-multiple-overrides"],[price("override-80",80,"pl-override-low","override"),price("override-90",90,"pl-override-high","override"),price("default-100",100)]),
 ("sale-only-no-original-and-missing-set",["ps-sale-only","ps-missing"],[price("sale-75",75,"pl-sale","sale")]),
]
def select(rows,ids,mutation=None):
 mutation=mutation or {}
 grouped={}
 for row in rows: grouped.setdefault(row["price_set_id"],[]).append(row)
 output=[]
 for set_id in ids:
  prices=grouped.get(set_id,[])
  list_price=next((p for p in prices if p["price_list_id"]),None)
  default=next((p for p in prices if not p["price_list_id"]),None)
  if not prices or (not list_price and not default): continue
  non_sale=[p for p in prices if p["price_list_type"]!="sale"]
  non_sale_list=next((p for p in non_sale if p["price_list_id"]),None)
  calculated=default
  original=default if mutation.get("default_as_original") else (non_sale_list or default)
  if list_price:
   if list_price["price_list_type"]=="override":
    calculated=list_price
    original=default if mutation.get("default_as_original") else list_price
   elif list_price["price_list_type"]=="sale":
    if mutation.get("always_choose_sale"):
     calculated=list_price
    else:
     reference=original
     if reference is None:
      calculated=list_price
     else:
      calculated=list_price if float(list_price["amount"])<=float(reference["amount"]) else reference
    if mutation.get("sale_as_original"): original=list_price
  def details(p):
   if p is None:return {"id":None,"price_list_id":None,"price_list_type":None,"min_quantity":None,"max_quantity":None}
   return {"id":p["id"],"price_list_id":p["price_list_id"],"price_list_type":p["price_list_type"],
     "min_quantity":None,"max_quantity":None}
  output.append({"id":set_id,"is_calculated_price_price_list":bool(calculated and calculated["price_list_id"]),
   "is_calculated_price_tax_inclusive":False,
   "calculated_amount":float(calculated["amount"]) if calculated else None,
   "raw_calculated_amount":calculated["raw_amount"] if calculated else None,
   "is_original_price_price_list":bool(original and original["price_list_id"]),
   "is_original_price_tax_inclusive":False,
   "original_amount":float(original["amount"]) if original else None,
   "raw_original_amount":original["raw_amount"] if original else None,
   "currency_code":calculated["currency_code"] if calculated else None,
   "calculated_price":details(calculated),"original_price":details(original)})
 return output

def capture(mutation=None):
 scenarios=[]
 for label,ids,rows in FIXTURES:
  scenarios.append({"label":label,"inputs":{"priceSetIds":ids,"candidates":rows},"output":select(rows,ids,mutation)})
 return {"implementation":"Independent Python 3.12 price-selection model","scenarios":scenarios}

if __name__=="__main__":
 import json
 print(json.dumps(capture(),indent=2))
