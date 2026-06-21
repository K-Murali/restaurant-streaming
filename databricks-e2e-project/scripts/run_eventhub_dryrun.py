import importlib.util
import pathlib
import json

p = pathlib.Path(__file__).parent.parent.joinpath("00_synthetic_data", "04_eventhub_orders.py").resolve()
spec = importlib.util.spec_from_file_location("eventhub_module", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print(json.dumps(module.generate_order(), indent=4))
