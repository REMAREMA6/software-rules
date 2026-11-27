package main

import (
 "encoding/json"
 "fmt"
 "os"
 "path/filepath"
 "strings"

 "github.com/spf13/pflag"
 "github.com/spf13/viper"
)
type Scenario struct { Label string `json:"label"`; Value any `json:"value"` }
func configFile(content string) string {
 dir,err:=os.MkdirTemp("","viper-config-"); if err!=nil {panic(err)}
 path:=filepath.Join(dir,"config.yaml")
 if err=os.WriteFile(path,[]byte(content),0600);err!=nil {panic(err)}
 return path
}
func read(v *viper.Viper,path string) { v.SetConfigFile(path); if err:=v.ReadInConfig();err!=nil {panic(err)} }
func main(){
 var out []Scenario
 v:=viper.New();v.SetDefault("port",8000);out=append(out,Scenario{"default",v.GetInt("port")})
 v=viper.New();v.SetDefault("port",8000);read(v,configFile("PORT: 9000\n"));out=append(out,Scenario{"yaml-file-case-insensitive",v.GetInt("port")})
 v=viper.New();v.SetDefault("port",8000);read(v,configFile("port: 9000\n"));v.SetEnvPrefix("APP");v.SetEnvKeyReplacer(strings.NewReplacer(".","_"));v.AutomaticEnv();_ = os.Setenv("APP_PORT","7000");out=append(out,Scenario{"environment-over-file",v.GetInt("port")});_ = os.Unsetenv("APP_PORT")
 v=viper.New();v.SetDefault("port",8000);read(v,configFile("port: 9000\n"));v.SetEnvPrefix("APP");v.AutomaticEnv();_ = os.Setenv("APP_PORT","7000")
 flags:=pflag.NewFlagSet("test",pflag.ContinueOnError);flags.String("port","6000","");_ = flags.Set("port","6000");if err:=v.BindPFlags(flags);err!=nil {panic(err)}
 out=append(out,Scenario{"changed-flag-over-environment",v.GetInt("port")});_ = os.Unsetenv("APP_PORT")
 v=viper.New();v.SetDefault("port",8000);read(v,configFile("port: 9000\n"));v.SetEnvPrefix("APP");v.AutomaticEnv();_ = os.Setenv("APP_PORT","7000");flags=pflag.NewFlagSet("test",pflag.ContinueOnError);flags.String("port","6000","");_ = flags.Set("port","6000");if err:=v.BindPFlags(flags);err!=nil {panic(err)};v.Set("port",5000)
 out=append(out,Scenario{"runtime-override-highest-precedence",v.GetInt("port")});_ = os.Unsetenv("APP_PORT")
 v=viper.New();v.SetDefault("mode","fallback");v.SetEnvPrefix("APP");v.AutomaticEnv();v.AllowEmptyEnv(true);_ = os.Setenv("APP_MODE","");out=append(out,Scenario{"allow-empty-environment-value",v.GetString("mode")});_ = os.Unsetenv("APP_MODE")
 v=viper.New();v.SetConfigType("yaml");if err:=v.ReadConfig(strings.NewReader("database:\n  host: db.file\n"));err!=nil {panic(err)};v.SetEnvPrefix("APP");v.SetEnvKeyReplacer(strings.NewReplacer(".","_"));v.AutomaticEnv();_ = os.Setenv("APP_DATABASE_HOST","db.env");out=append(out,Scenario{"nested-environment-key-replacer",v.GetString("database.host")});_ = os.Unsetenv("APP_DATABASE_HOST")
 v=viper.New();_ = os.Setenv("CUSTOM_REGION","eu-west");if err:=v.BindEnv("region","CUSTOM_REGION");err!=nil {panic(err)};out=append(out,Scenario{"explicit-environment-binding",v.GetString("region")});_ = os.Unsetenv("CUSTOM_REGION")
 v=viper.New();v.SetDefault("port",8000);read(v,configFile("port: 9000\n"));v.SetEnvPrefix("APP");v.SetEnvKeyReplacer(strings.NewReplacer(".","_"));v.AutomaticEnv();_ = os.Setenv("APP_PORT","7000");flags=pflag.NewFlagSet("test",pflag.ContinueOnError);flags.String("port","6000","");_ = flags.Set("port","6000");if err:=v.BindPFlags(flags);err!=nil {panic(err)};v.Set("port","5000");out=append(out,Scenario{"full-precedence-chain",v.GetString("port")});_ = os.Unsetenv("APP_PORT")
 result:=map[string]any{"source":"spf13/viper","sourceCommit":os.Getenv("VIPER_SOURCE_COMMIT"),"scenarios":out}
 b,err:=json.MarshalIndent(result,"","  ");if err!=nil {panic(err)};fmt.Println(string(b))
}
