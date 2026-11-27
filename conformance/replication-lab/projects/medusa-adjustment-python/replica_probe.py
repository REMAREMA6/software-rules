from decimal import Decimal, getcontext
import json
getcontext().prec=28
def D(x): return Decimal(str(x))
def round8(x):
 if x is None:return None
 return float(x.quantize(Decimal("0.00000001")))
def calculate(quantity, tax_rate, adjustments, mutation=None):
 mutation=mutation or {}
 # Match the source's JS truthy fallback: missing or zero quantity becomes one.
 q=D((1 if quantity is None else quantity) if mutation.get("zero_quantity_no_fallback") else (quantity or 1))
 rate=None if tax_rate is None else D(tax_rate)
 subtotal=Decimal(0); tax=Decimal(0); total=Decimal(0); rows=[]
 for adj in adjustments:
  amount=adj.get("amount")
  if amount is None and not mutation.get("include_missing_amount"):
   continue
  amount=D(amount or 0)
  inclusive=bool(adj.get("is_tax_inclusive"))
  if rate is not None and inclusive and not mutation.get("skip_inclusive_tax_conversion"):
   adj_sub=amount/(Decimal(1)+rate)
  else:
   adj_sub=amount
  adj_tax=adj_sub*rate if rate is not None and not mutation.get("skip_exclusive_tax") else Decimal(0)
  adj_total=adj_sub+adj_tax
  subtotal+=adj_sub; tax+=adj_tax; total+=adj_total
  rows.append({"amount":round8(amount),"is_tax_inclusive":inclusive,
   "subtotal":round8(subtotal if mutation.get("cumulative_adjustment_values") else adj_sub),
   "total":round8(total if mutation.get("cumulative_adjustment_values") else adj_total)})
 per_item=total/q if q!=0 else Decimal(0)
 per_sub=subtotal/q if q!=0 else Decimal(0)
 per_tax=tax/q if q!=0 else Decimal(0)
 if mutation.get("skip_per_item_allocation"):
  per_item,per_sub,per_tax=total,subtotal,tax
 return {"adjustmentsTotal":round8(total),"adjustmentsSubtotal":round8(subtotal),
  "adjustmentsTaxTotal":round8(tax),"adjustmentPerItem":round8(per_item),
  "adjustmentSubtotalPerItem":round8(per_sub),"adjustmentTaxTotalPerItem":round8(per_tax),
  "adjustments":rows}
FIXTURES=[
 ("no-adjustments",1,0.2,[]),
 ("single-exclusive",2,0.2,[{"amount":20,"is_tax_inclusive":False}]),
 ("multiple-exclusive",4,0.2,[{"amount":20,"is_tax_inclusive":False},{"amount":10,"is_tax_inclusive":False}]),
 ("inclusive-single",2,0.2,[{"amount":24,"is_tax_inclusive":True}]),
 ("mixed-inclusive-exclusive",2,0.2,[{"amount":24,"is_tax_inclusive":True},{"amount":10,"is_tax_inclusive":False}]),
 ("missing-adjustment-amount",2,0.2,[{"amount":None,"is_tax_inclusive":False},{"amount":10,"is_tax_inclusive":False}]),
 ("zero-quantity",0,0.2,[{"amount":20,"is_tax_inclusive":False}]),
 ("fractional-quantity",2.5,0.2,[{"amount":10,"is_tax_inclusive":False}]),
 ("no-tax-context",2,None,[{"amount":20,"is_tax_inclusive":True}])
]
def capture(mutation=None):
 scenarios=[]
 for label,q,rate,adjustments in FIXTURES:
  scenarios.append({"label":label,"inputs":{"quantity":q,"taxRate":rate,"adjustments":adjustments},
   "output":calculate(q,rate,adjustments,mutation)})
 return {"implementation":"Independent Python 3.12 Decimal adjustment model","scenarios":scenarios}
if __name__=="__main__": print(json.dumps(capture(),indent=2))
