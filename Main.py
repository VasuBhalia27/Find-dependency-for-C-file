import os
import re

def find_includes(file_path):
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
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def collect_dependencies(file_path, search_path, visited=None):
    if visited is None:
        visited = set()
    dependencies = []
    abs_file_path = os.path.abspath(file_path)
    if abs_file_path in visited:
        return dependencies
    visited.add(abs_file_path)
    includes = find_includes(file_path)
    for inc in includes:
        inc_path = find_file(inc, search_path)
        if inc_path:
            abs_inc_path = os.path.abspath(inc_path)
            if abs_inc_path not in visited:
                dependencies.append(abs_inc_path)
                sub_deps = collect_dependencies(abs_inc_path, search_path, visited)
                dependencies.extend(sub_deps)
    return dependencies

if __name__ == "__main__":
    source_module_path = input("Enter source module path: ").strip()
    project_directory = input("Enter project directory path: ").strip()


    if not os.path.isfile(source_module_path):
        print(f"Source file {source_module_path} does not exist.")
    elif not os.path.isdir(project_directory):
        print(f"Project directory {project_directory} does not exist.")
    else:


        all_dependencies = collect_dependencies(source_module_path, project_directory)
        print("\nAll dependencies found:")
        for dep in all_dependencies:
            print(dep)
