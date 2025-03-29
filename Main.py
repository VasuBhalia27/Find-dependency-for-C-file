import re,os

dependencies_buffer = []
dependencies_path_buffer = []
all_dependencies_paths= []
final_result = []
#Function definations --------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


def find_includes(source_module_Fpath):
    # Regex pattern to match #include directives, whether it's in angle brackets or quotes
    include_pattern = re.compile(r'#include\s+[<"](.*?)[>"]')
    
    # List to store the included files
    included_files = []

    try:
        # Open the C file
        with open(source_module_Fpath, 'r') as file:
            for line in file:
                match = include_pattern.search(line)
                if match:
                    # Extract the included file name
                    included_files.append(match.group(1))
                    
        return included_files
    except FileNotFoundError:
        print(f"The file {source_module_Fpath} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def find_file(directory, filename):
    for root, dirs, files in os.walk(directory):  # Traverse the directory
        if filename in files:
            return os.path.join(root, filename)  # Return full path if file is found
    return None  # Return None if file not found

# User inputs ----------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------



source_module_Fpath = input("Enter source module path : ")

Project_directory = input("Enter directory path : ")



# Main Code ------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------



dependencies_buffer = find_includes(source_module_Fpath)

for i in range(len(dependencies_buffer)):
    current_path = find_file(Project_directory, dependencies_buffer[i])
    if current_path:
        dependencies_path_buffer.append(current_path)
        all_dependencies_paths.append(current_path)


dependencies_path_buffer = []
dependencies_buffer = []


print("Dependencies found:", dependencies_buffer)

print("Dependencies paths:", dependencies_path_buffer)