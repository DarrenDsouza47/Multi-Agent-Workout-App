from langflow.load import run_flow_from_json
import requests
from typing import Optional
import json
BASE_API_URL = "http://localhost:7860"

def ask_ai(profile,question):
    TWEAKS = {
    "TextInput-75Ot8": {
        "input_value": question
    },
    "TextInput-H3Gfo": {
        "input_value": profile
    }
    }

    result = run_flow_from_json(flow="Ask_AI_flow.json",
                                input_value="message",
                                session_id="", # provide a session id if you want to use session state
                                fallback_to_env_vars=False, # False by default
                                tweaks=TWEAKS)

    return (result[0].outputs[0].results['text'].data['text'])


def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
def get_macros(goals,profile):
    print(goals)
    print(profile)
    TWEAKS = {
    "TextInput-ka8FW": {
        "input_value": ", ".join(goals)
    },
    "TextInput-IL7DZ": {
        "input_value": dict_to_string(profile)
    }
    }
    return run_flow("",tweaks=TWEAKS)

def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  api_key: Optional[str] = None) -> dict:
    
    api_url = f"{BASE_API_URL}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    print(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
    return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])

