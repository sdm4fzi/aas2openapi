

import basyx
import basyx.aas.adapter.json
import json

from aas2openapi.convert.convert_pydantic import rename_data_specifications_for_basyx


with open('aas_data.json', encoding='utf-8-sig') as json_file:
    file = json.load(json_file)
    file = rename_data_specifications_for_basyx(file)
    file = json.dumps(file, indent=4)
    print(file)
    json_file_data = json.loads(file, cls=basyx.aas.adapter.json.AASFromJsonDecoder)

print(json_file_data)
for el in json_file_data:
