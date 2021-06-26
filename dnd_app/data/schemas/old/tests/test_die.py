import jsonschema
import json
from pathlib import Path, PurePath

from jsonschema import validate

def GetJSON(file_path):
  with open(file_path, 'r') as json_file:
    json_obj = json.load(json_file)
  return json_obj

def ValidateJSON(json_schema, json_obj):
  dir_path = Path("C:\\User Data\\DOCUMENTS\\Projects (old)\\Creative\\D&D_App\\code\\data\\schemas\\")
  data_dir = PurePath(dir_path)
  data_dir = data_dir.relative_to(data_dir.drive)
  print(data_dir.as_posix())
  resolver = jsonschema.RefResolver(referrer=json_schema, base_uri="file://" + dir_path)
  print(resolver.base_uri)

  try:
    validate(instance=json_obj, schema=json_schema, resolver=resolver)
    print("json valid!")
  except jsonschema.exceptions.ValidationError as err:
    print("expection")
    print(err)
    exit()

schema_file = r'C:\User Data\DOCUMENTS\Projects (old)\Creative\D&D_App\code\data\schemas\old\schema_die.json'
json_file = r'C:\User Data\DOCUMENTS\Projects (old)\Creative\D&D_App\code\data\schemas\old\tests\test_die.json'

schema_file = r"C:\User Data\DOCUMENTS\Projects (old)\Creative\D&D_App\code\data\schemas\main_schema.json"
json_file = r"C:\User Data\DOCUMENTS\Projects (old)\Creative\D&D_App\code\data\character\subs\main.json"

schema = GetJSON(schema_file) 
json_obj = GetJSON(json_file)

ValidateJSON(schema, json_obj)

print(json_obj)
