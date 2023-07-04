

import basyx
import basyx.aas.adapter.json
import json

from aas2openapi.convert.convert_pydantic import rename_data_specifications_for_basyx, rename_semantic_id_for_basyx

with open("examplaaaa.json", "r", encoding="utf-8") as json_file:
    aas_dict = json.load(json_file)

rename_semantic_id_for_basyx(aas_dict)
rename_data_specifications_for_basyx(aas_dict)

print(json.dumps(aas_dict, indent=4))

