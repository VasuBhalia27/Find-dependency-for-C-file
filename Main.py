import os
import re
import pandas as pd


def find_includes(file_path): #finds includes in a particular file 
    include_pattern = re.compile(r'#include\s+[<"]([^">]+)[">]')
    includes = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = include_pattern.match(line.strip())
                if match:
                    includes.append(match.group(1))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return includes


def find_file(filename, search_path):
    exclude_dirs = {'Bootloaders', 'mtb-pdl-cat2'}  # Set of directory names to exclude

    for root, dirs, files in os.walk(search_path, topdown=True):
        # Modify dirs in-place to exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        if filename in files:
            print(f'File "{filename}" found in {root}')
            return os.path.join(root, filename)
    return None


def collect_dependencies(file_path, search_path):

    visited = set()
    dependencies = []
    stack = [os.path.abspath(file_path)]      

    while stack:
        current_file = stack.pop()
        if current_file in visited:
            continue
        visited.add(current_file)

        includes = find_includes(current_file)
        for inc in includes:
            inc_path = find_file(inc, search_path)
            if inc_path:
                abs_inc_path = os.path.abspath(inc_path)
                if abs_inc_path not in visited:
                    dependencies.append(abs_inc_path)
                    stack.append(abs_inc_path)

    return dependencies


if __name__ == "__main__":
    source_module_path = input("Enter source module path: ").strip('"')
    project_directory = input("Enter project directory path: ").strip('"')

    if not os.path.isfile(source_module_path):
        print(f"Source file {source_module_path} does not exist.")
    elif not os.path.isdir(project_directory):
        print(f"Project directory {project_directory} does not exist.")
    else:
        all_dependencies = collect_dependencies(source_module_path, project_directory)
        print("\nAll dependencies found:")

        data = []
        for dep in all_dependencies:
            all_dependencies_path, all_dependencies_filename = os.path.split(dep)
            row = {
                'Filename': all_dependencies_filename,
                'Filepath': all_dependencies_path
            }
            data.append(row)

        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset='Filepath', keep='first')

        # Define the output Excel file path
        output_file_name = os.path.basename(source_module_path)
        output_file = f"{output_file_name}.xlsx"

        # Write the DataFrame to the Excel file
        df.to_excel(output_file, index=False)
        print(f"\nData has been written to {output_file}")
