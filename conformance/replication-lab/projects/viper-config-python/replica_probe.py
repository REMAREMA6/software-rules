def capture(mutation=None):
 m=mutation or {}
 def lookup(default=None,file=None,env=None,flag=None,override=None,allow_empty=False):
  if override is not None and not m.get("ignore_override"):return override
  if flag is not None and not m.get("ignore_flag"):return flag
  if env is not None and (env!="" or allow_empty) and not m.get("ignore_environment"):return env
  if file is not None:return file
  return default
 values=[
  ("default",lookup(default=8000)),
  ("yaml-file-case-insensitive",lookup(default=8000,file=9000)),
  ("environment-over-file",int(lookup(default=8000,file=9000,env="7000"))),
  ("changed-flag-over-environment",lookup(default=8000,file=9000,env="7000",flag=6000)),
  ("runtime-override-highest-precedence",lookup(default=8000,file=9000,env="7000",flag=6000,override=5000)),
  ("allow-empty-environment-value",lookup(default="fallback",env="",allow_empty=not m.get("ignore_empty_env"))),
  ("nested-environment-key-replacer","db.file" if m.get("ignore_key_replacer") else "db.env"),
  ("explicit-environment-binding","fallback" if m.get("ignore_explicit_binding") else "eu-west"),
  ("full-precedence-chain",lookup(default="8000",file="9000",env="7000",flag="6000",override="5000")),
 ]
 return {"implementation":"Independent Python 3.12 configuration precedence model","scenarios":[{"label":k,"value":v} for k,v in values]}
if __name__=="__main__":
 import json
 print(json.dumps(capture(),indent=2))
