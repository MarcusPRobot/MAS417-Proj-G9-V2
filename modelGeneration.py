import os
import sys

## Command line commands to start generation, initials ##########################

destCmd = "cd dreamgaussian"

genLine_start = "python main.py --config configs/text.yaml prompt=\""
genLine_end = "\" save_path="

impLine_start = "python main2.py --config configs/text.yaml prompt=\""

## Build function ###############################################################

def gen_model(objName, objDesc):

    #envAct = "venv\Scripts\Activate.ps1"
    genCmd = genLine_start + objDesc + genLine_end + objName
    impCmd = impLine_start + objDesc + genLine_end + objName
    print(genCmd)
    print(impCmd)



    combCMD = destCmd + " && " + genCmd + " && " + impCmd # envAct + "&&" +

    print("Generating 3D model, estimated time is 7 minutes...")
    #subprocess.run(['cmd', '/c', combCMD], shell=True)
    os.system(combCMD)

# Example usage
#project_root = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.join(project_root, 'dreamgaussian'))
#sys.path.append(os.path.join(project_root, 'dreamgaussian', 'diff-gaussian-rasterization'))
#sys.path.append(os.path.join(project_root, 'dreamgaussian', 'guidance'))
#gen_model("deskOrganizer", "A modular design to neatly store office supplies.")