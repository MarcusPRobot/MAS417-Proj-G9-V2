import os
import sys
import requests
from apiKey import Meshy_APIKey

## Command line commands to start generation, initials ##########################

destCmd = "cd dreamgaussian"

genLine_start = "python main.py --config configs/text.yaml prompt=\""
genLine_end = "\" save_path="

impLine_start = "python main2.py --config configs/text.yaml prompt=\""

## Build function ###############################################################

    def gen_model(mesh_name, mesh_description):
        url = "http://api.meshy.ai/v1/text-to-texture"
        headers = {
            'Authorization': f'Bearer {Meshy_APIKey}',
            'Content-Type': 'application/json'
        }
        payload = {
            'name': mesh_name,
            'description': mesh_description
        }

        try:
            response = requests.post(url, headers=headers, json=payload, allow_redirects=True)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            print("Mesh created successfully:")
            print(data)
            return data
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.text}")
        except Exception as err:
            print(f"An error occurred: {err}")

# Example usage
#project_root = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.join(project_root, 'dreamgaussian'))
#sys.path.append(os.path.join(project_root, 'dreamgaussian', 'diff-gaussian-rasterization'))
#sys.path.append(os.path.join(project_root, 'dreamgaussian', 'guidance'))
#gen_model("deskOrganizer", "A modular design to neatly store office supplies.")