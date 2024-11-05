import subprocess
import os
import sys

## Command line commands to start generation, initials ##########################

# Folder destination
destCmd = "cd dreamgaussian"

# Mesh generation command building-strings
genLine_start = "python main.py --config configs/text.yaml prompt=\""
genLine_end = "\" save_path="

# Mesh improvement command building-string
impLine_start = "python main2.py --config configs/text.yaml prompt=\""

## Build function ###############################################################

def gen_model(objName, objDesc):

    genCmd = genLine_start + objDesc + genLine_end + objName
    impCmd = impLine_start + objDesc + genLine_end + objName

    combCMD = destCmd + " && " + genCmd + " && " + impCmd

    print("Generating 3D model, estimated time 2-5 minutes...")
    subprocess.run(['cmd', '/c', combCMD], shell=True)

# Example usage
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, 'dreamgaussian'))
sys.path.append(os.path.join(project_root, 'dreamgaussian', 'diff-gaussian-rasterization'))
sys.path.append(os.path.join(project_root, 'dreamgaussian', 'guidance'))
gen_model("deskOrganizer", "A modular design to neatly store office supplies.")