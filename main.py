from apiClient import get_prompt
from modelGeneration import gen_model
from modelViewer import viewModel
## Main program ###############################################################

def main():
    print("AI Powered Random 3D-Printable Object Generator")
    print("Choices:\n1. Generate random object\n2. Other options")
    main_options()

def main_options():
    choice = int(input("Enter choice: "))
    if choice == 1:
        initiate_model_generation(False)
    elif choice == 2:
        print("Other options")
        other_options()
    else:
        print("Invalid choice, please try again")
        main_options()

def other_options():
    print("Other options:\n1. Open 3D model in 3D Viewer\n2. Custom 3D model\n3. Exit program")
    otherChoice = int(input("Enter choice: "))
    if otherChoice == 1:
        print("Opening 3D model in 3D Viewer...")
        viewModel()
    elif otherChoice == 2:
        print("Custom 3D model\nPut in name and then a description. No spaces in the name.")
        name = str(input("Enter name: "))
        description = str(input("Enter description: "))
        print("Creating " + name + " with description: " + description + " model...")
        gen_model(name, description)
    elif otherChoice == 3:
        print("Exiting program...")
        exit()
    else:
        print("Invalid choice, please try again")
        other_options()

## Generation of 3D model #####################################################
def initiate_model_generation(wrongPress):
    apiLogs = open("API Logs.txt", "a")
    if not wrongPress:
        gptData = get_prompt()
        apiLogs.write(gptData + "\n")
        objectName = gptData.split("#")[0]
        objectDescription = gptData.split("#")[1]
        print("The random prompt generator has suggested the following model idea:\n"
              "Object Name: {}\n"
              "Object Description: {}".format(objectName, objectDescription))
    apiLogs.close()
    print("Would you like to generate the 3D model for this object?\n"
          "1. Yes\n2. No")
    initChoice = int(input("Enter choice: "))

    if initChoice == 1:
        gen_model(objectName, objectDescription)
        main()
    elif initChoice == 2:
        print("Returning to main menu...")
        main()
    else:
        print("Invalid choice, please try again")
        initiate_model_generation(True)


main()