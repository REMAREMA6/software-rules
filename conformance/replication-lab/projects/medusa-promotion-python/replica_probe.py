import json
from decimal import Decimal
MISSING=object()
def stringify(v):
 if v is MISSING:return "undefined"
 if v is None:return "null"
 if isinstance(v,bool):return "true" if v else "false"
 return str(v)
def numeric(v):
 try:return Decimal(str(v))
 except Exception:return Decimal("NaN")
def evaluate(rule_values,operator,values):
 vals=values if isinstance(values,list) else [values]
 if not vals:
  return operator=="ne"
 if operator=="eq":return all(stringify(v) in set(rule_values) for v in vals)
 if operator=="in":return any(stringify(v) in set(rule_values) for v in vals)
 if operator=="ne":return all(stringify(v) not in set(rule_values) for v in vals)
 if operator in ("gt","gte","lt","lte"):
  def compare(v,r):
   a,b=numeric(v),numeric(r)
   if operator=="gt":return a>b
   if operator=="gte":return a>=b
   if operator=="lt":return a<b
   return a<=b
  return all(any(compare(v,r) for r in rule_values) for v in vals)
 return False
def pick(path,context):
 value=context
 for key in path.split("."):
  if not isinstance(value,dict) or key not in value:return MISSING
  value=value[key]
 return value
def are_rules_valid(rules,context,scope,mutation=None):
 mutation=mutation or {}
 if not rules:return True
 decisions=[]
 for rule in rules:
  attribute=rule.get("attribute")
  values=rule.get("values")
  if not attribute or not values:
   decisions.append(False)
   continue
  valid=[v.get("value") for v in values if isinstance(v.get("value"),str)]
  if mutation.get("keep_non_string_values"):
   valid=[stringify(v.get("value")) for v in values]
  if not valid:
   decisions.append(False)
   continue
  path=attribute
  if scope=="items" and not mutation.get("skip_scope_strip"):path=path.replace("items.","",1)
  elif scope=="shipping_methods" and not mutation.get("skip_scope_strip"):path=path.replace("shipping_methods.","",1)
  found=pick(path,context)
  if found is MISSING and mutation.get("missing_context_fails_ne"):
   decisions.append(False)
   continue
  decisions.append(evaluate(valid,rule.get("operator",""),found))
 return any(decisions) if mutation.get("any_rule_passes") else all(decisions)
CASES=[
 ("eq-scalar-string","condition",["red"],"eq","red"),
 ("eq-number-coercion","condition",["42"],"eq",42),
 ("eq-array-all-match","condition",["red","blue"],"eq",["red","blue"]),
 ("eq-array-one-mismatch","condition",["red","blue"],"eq",["red","green"]),
 ("in-array-any-match","condition",["red","blue"],"in",["green","blue"]),
 ("in-array-no-match","condition",["red","blue"],"in",["green","yellow"]),
 ("ne-empty-array","condition",["red"],"ne",[]),
 ("ne-array-no-match","condition",["red","blue"],"ne",["green","yellow"]),
 ("ne-array-has-match","condition",["red","blue"],"ne",["green","red"]),
 ("gt-numeric","condition",["2"],"gt","10"),
 ("gte-boundary","condition",["10"],"gte",10),
 ("lt-numeric","condition",["10"],"lt","2"),
 ("lte-boundary","condition",["10"],"lte",10),
 ("gt-numeric-lexical-trap","condition",["2"],"gt","10"),
 ("invalid-operator","condition",["x"],"contains","x"),
 ("ne-empty-rule-values","condition",[],"ne","anything"),
 ("empty-rules","context",[],{},{}),
 ("item-prefix-strip","context",[{"attribute":"items.product_id","operator":"eq","values":[{"value":"shirt"}]}],{"product_id":"shirt"},"items"),
 ("shipping-prefix-strip","context",[{"attribute":"shipping_methods.option_id","operator":"eq","values":[{"value":"express"}]}],{"option_id":"express"},"shipping_methods"),
 ("nested-attribute","context",[{"attribute":"customer.group.id","operator":"eq","values":[{"value":"vip"}]}],{"customer":{"group":{"id":"vip"}}},"order"),
 ("missing-attribute-ne","context",[{"attribute":"customer.group","operator":"ne","values":[{"value":"blocked"}]}],{},"order"),
 ("missing-attribute-eq","context",[{"attribute":"customer.group","operator":"eq","values":[{"value":"vip"}]}],{},"order"),
 ("empty-rule-values","context",[{"attribute":"product_id","operator":"eq","values":[]}],{"product_id":"shirt"},"items"),
 ("non-string-rule-values","context",[{"attribute":"product_id","operator":"eq","values":[{"value":42}]}],{"product_id":42},"items"),
 ("all-rules-must-pass","context",[{"attribute":"product_id","operator":"eq","values":[{"value":"shirt"}]},{"attribute":"customer.group","operator":"eq","values":[{"value":"vip"}]}],{"product_id":"shirt","customer":{"group":"regular"}},"items"),
 ("all-rules-pass","context",[{"attribute":"product_id","operator":"eq","values":[{"value":"shirt"}]},{"attribute":"customer.group","operator":"eq","values":[{"value":"vip"}]}],{"product_id":"shirt","customer":{"group":"vip"}},"items"),
 ("order-scope-does-not-strip-prefix","context",[{"attribute":"items.product_id","operator":"eq","values":[{"value":"shirt"}]}],{"product_id":"shirt"},"order"),
 ("context-eq-array-all","context",[{"attribute":"tags","operator":"eq","values":[{"value":"sale"},{"value":"new"}]}],{"tags":["sale","new"]},"items"),
 ("context-eq-array-one-mismatch","context",[{"attribute":"tags","operator":"eq","values":[{"value":"sale"},{"value":"new"}]}],{"tags":["sale","clearance"]},"items"),
 ("context-in-array-any","context",[{"attribute":"tags","operator":"in","values":[{"value":"sale"},{"value":"new"}]}],{"tags":["clearance","new"]},"items"),
 ("context-in-array-none","context",[{"attribute":"tags","operator":"in","values":[{"value":"sale"},{"value":"new"}]}],{"tags":["clearance","winter"]},"items"),
 ("context-no-rules","context",[],{"product_id":"shirt"},"items")
]
def capture(mutation=None):
 out=[]
 for label,mode,a,b,c in CASES:
  if mode=="condition":
   values=c
   if mutation and mutation.get("eq_uses_any") and b=="eq" and isinstance(values,list):
    result=any(stringify(v) in set(a) for v in values)
   elif mutation and mutation.get("in_uses_all") and b=="in" and isinstance(values,list):
    result=all(stringify(v) in set(a) for v in values)
   elif mutation and mutation.get("lexical_numeric") and b in ("gt","gte","lt","lte"):
    vals=values if isinstance(values,list) else [values]
    def cmp(v,r):
     x,y=stringify(v),stringify(r)
     return x>y if b=="gt" else x>=y if b=="gte" else x<y if b=="lt" else x<=y
    result=all(any(cmp(v,r) for r in a) for v in vals)
   elif mutation and mutation.get("ne_missing_fails") and b=="ne" and values==[]:result=False
   else:result=evaluate(a,b,values)
   inputs={"ruleValues":a,"operator":b,"valuesToCheck":values}
  else:
   result=are_rules_valid(a,b,c,mutation)
   inputs={"rules":a,"context":b,"contextScope":c}
  out.append({"label":label,"inputs":inputs,"output":bool(result)})
 return {"implementation":"Independent Python 3.12 promotion-rule evaluator","scenarios":out}
if __name__=="__main__":print(json.dumps(capture(),indent=2))
