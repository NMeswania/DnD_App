import jsonschema
import json

print(json.__spec__)

from jsonschema import validate

def GetJSON(file_path):
  with open(file_path, 'r') as json_file:
    json_obj = json.load(json_file)
  return json_obj

def ValidateJSON(json_schema, json_obj):
  try:
    validate(instance=json_obj, schema=json_schema)
    print("json valid!")
  except jsonschema.exceptions.ValidationError as err:
    print("expection")
    print(err)
    exit()

schema_file = r'C:\User Data\DOCUMENTS\Projects (old)\Creative\D&D_App\code\data\schemas\old\schema_die.json'
json_file = r'C:\User Data\DOCUMENTS\Projects (old)\Creative\D&D_App\code\data\schemas\old\tests\test_die.json'

schema = GetJSON(schema_file) 
json_obj = GetJSON(json_file)

ValidateJSON(schema, json_obj)

print(json_obj)
