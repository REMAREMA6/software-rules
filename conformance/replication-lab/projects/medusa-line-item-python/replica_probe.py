from decimal import Decimal,getcontext
import json
getcontext().prec=28
def D(x):return Decimal(str(x))
def r8(x):return None if x is None else float(x.quantize(Decimal("0.00000001")))
def calculate(item,mutation=None):
 mutation=mutation or {}
 q=D(item["quantity"]);unit=D(item["unit_price"])
 rates=[D(x["rate"]) for x in item.get("tax_lines",[])]
 sum_rate=(max(rates) if mutation.get("max_tax_rate") and rates else sum(rates,Decimal(0)))/100
 inclusive=bool(item.get("is_tax_inclusive",False))
 gross=unit*q
 subtotal=gross/(1+sum_rate) if inclusive else gross
 adjustments=item.get("adjustments",[])
 adj_sub=Decimal(0);adj_tax=Decimal(0);adj_total=Decimal(0);rows=[]
 for a in adjustments:
  amount=D(a["amount"]);inc=bool(a.get("is_tax_inclusive",False))
  one_sub=amount/(1+sum_rate) if inc and not mutation.get("skip_inclusive_conversion") else amount
  one_tax=one_sub*sum_rate
  one_total=one_sub+one_tax
  adj_sub+=one_sub;adj_tax+=one_tax;adj_total+=one_total
  rows.append({"amount":r8(amount),"is_tax_inclusive":inc,
   "subtotal":r8(adj_sub if mutation.get("cumulative_adjustment") else one_sub),
   "total":r8(adj_total if mutation.get("cumulative_adjustment") else one_total)})
 detail=item.get("detail") or {}
 returned=D(detail.get("return_received_quantity",0))+D(detail.get("return_dismissed_quantity",0))
 current_qty=q-returned
 current_gross=unit*current_qty
 current_sub=current_gross/(1+sum_rate) if inclusive else current_gross
 per_item_discount=adj_sub/(q if q!=0 else Decimal(1))
 current_discount_sub=adj_sub if mutation.get("wrong_quantity_allocation") else per_item_discount*current_qty
 original_tax=current_sub*sum_rate
 tax_base=current_sub-current_discount_sub
 tax=tax_base*sum_rate
 if mutation.get("tax_not_recalculated_after_discount"):tax=original_tax
 total=(current_sub-current_discount_sub)+tax
 original_total=current_gross if inclusive else current_sub+original_tax
 original_sub=current_gross-original_tax if inclusive else current_sub
 if mutation.get("original_tax_uses_discounted_base"):original_total=total
 result={"quantity":r8(q),"unit_price":r8(unit),"subtotal":r8(current_sub),"total":r8(total),
  "original_subtotal":r8(original_sub),"original_total":r8(original_total),
  "discount_subtotal":r8(current_discount_sub),"discount_tax_total":r8(original_tax-tax),
  "discount_total":r8(current_discount_sub+original_tax-tax),"tax_total":r8(tax),"original_tax_total":r8(original_tax),
  "adjustments":rows}
 if any(k in detail for k in ("return_requested_quantity","return_received_quantity","return_dismissed_quantity")):
  discount=adj_total if inclusive else adj_sub
  discount_per_unit=discount/q if q!=0 else Decimal(0)
  refundable_sub=current_qty*unit-current_qty*discount_per_unit
  refundable_tax=Decimal(0) if inclusive else refundable_sub*sum_rate
  refundable_total=refundable_sub+refundable_tax
  result["refundable_total"]=r8(refundable_total)
  result["refundable_total_per_unit"]=r8(Decimal(0) if current_qty==0 else refundable_total/current_qty)
 return result
FIXTURES=[
 {"label":"basic-no-tax","unit_price":50,"quantity":2,"tax_lines":[],"adjustments":[]},
 {"label":"exclusive-tax-20","unit_price":50,"quantity":2,"tax_lines":[{"rate":20}],"adjustments":[]},
 {"label":"multiple-additive-tax-lines","unit_price":100,"quantity":1,"tax_lines":[{"rate":10},{"rate":5}],"adjustments":[]},
 {"label":"inclusive-tax-20","unit_price":120,"quantity":1,"is_tax_inclusive":True,"tax_lines":[{"rate":20}],"adjustments":[]},
 {"label":"exclusive-discount-with-tax","unit_price":100,"quantity":1,"tax_lines":[{"rate":20}],"adjustments":[{"amount":20,"is_tax_inclusive":False}]},
 {"label":"inclusive-discount-with-tax","unit_price":120,"quantity":1,"is_tax_inclusive":True,"tax_lines":[{"rate":20}],"adjustments":[{"amount":24,"is_tax_inclusive":True}]},
 {"label":"multiple-exclusive-adjustments","unit_price":50,"quantity":2,"tax_lines":[{"rate":20}],"adjustments":[{"amount":10,"is_tax_inclusive":False},{"amount":5,"is_tax_inclusive":False}]},
 {"label":"mixed-inclusive-exclusive-adjustments","unit_price":50,"quantity":2,"tax_lines":[{"rate":20}],"adjustments":[{"amount":24,"is_tax_inclusive":True},{"amount":10,"is_tax_inclusive":False}]},
 {"label":"fractional-quantity","unit_price":40,"quantity":2.5,"tax_lines":[{"rate":10}],"adjustments":[]},
 {"label":"zero-quantity","unit_price":100,"quantity":0,"tax_lines":[{"rate":20}],"adjustments":[]},
 {"label":"empty-tax-context-with-discount","unit_price":100,"quantity":1,"tax_lines":[],"adjustments":[{"amount":20,"is_tax_inclusive":False}]},
 {"label":"inclusive-price-with-multiple-tax-lines","unit_price":115,"quantity":1,"is_tax_inclusive":True,"tax_lines":[{"rate":10},{"rate":5}],"adjustments":[{"amount":11.5,"is_tax_inclusive":True}]},
 {"label":"returned-quantity-prorated-discount","unit_price":25,"quantity":4,"tax_lines":[{"rate":20}],"adjustments":[{"amount":40,"is_tax_inclusive":False}],"detail":{"return_received_quantity":1}},
 {"label":"inclusive-return-refund","unit_price":120,"quantity":2,"is_tax_inclusive":True,"tax_lines":[{"rate":20}],"adjustments":[{"amount":24,"is_tax_inclusive":True}],"detail":{"return_dismissed_quantity":1}}
]
def capture(mutation=None):
 out=[]
 for item in FIXTURES:
  out.append({"label":item["label"],"inputs":{"unit_price":item["unit_price"],"quantity":item["quantity"],
   "is_tax_inclusive":item.get("is_tax_inclusive",False),"tax_lines":item["tax_lines"],"adjustments":item["adjustments"],"detail":item.get("detail")},
   "output":calculate(item,mutation)})
 return {"implementation":"Independent Python 3.12 Decimal line-item calculator","scenarios":out}
if __name__=="__main__":print(json.dumps(capture(),indent=2))
