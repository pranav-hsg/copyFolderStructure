
import os;
from os import path ;
import argparse;
import json;
# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Define the flags/arguments
parser.add_argument('--fromPath', type=str, help='Path from which you want to copy folder structure.') # When --help flag is put, it will show this description.
parser.add_argument('--toPath', type=str, help = 'Path to which you want to paste folder structure')
# Parse the command-line arguments
args = parser.parse_args()

# If arguments contain --path flag.
basePath = args.fromPath if args.fromPath else os.getcwd();
toPath = args.toPath if args.toPath else os.getcwd();
import enum
# Using enum class create enumerations
class ItemType(enum.Enum):
   FILE = "file"
   FOLDER = "Folder"
   
 #  Extend (Inherit) json.JSONEncoder class
class EnumEncoder(json.JSONEncoder):
    # While serialization process enum serialization will throw error hence we are overriding JSONEncoder
    def default(self, obj):
        # If and only if serializing object is enum then return its value part , else proceed in a default way.
        if isinstance(obj, enum.Enum):
            return obj.value
        return super().default(obj)

def get_type(item):
    #  Switch case version for python
    mapping = {
        path.isfile(item) : ItemType.FILE  ,
        path.isdir(item): ItemType.FOLDER
    }
    return mapping.get(True)
    
# Given a basePath (from path) and settings it will create a json structure of folder (tree representation of folder structure.) .
def get_folder_structure_children(basePath,settings={}):
    # List all directories (files and folders as array.)
    dirs = os.listdir(basePath)
    folder_structure = []
    for d in dirs:
        absD = path.join(basePath,d)
        if(get_type(absD) == ItemType.FOLDER):
            temp = {'name' : d, 'basePath': basePath,'relPath':path.relpath(absD,basePath) , 'type' : ItemType.FOLDER, 'children': []}
            # If folder has a sub folder recursively call this function
            temp['children'] = get_folder_structure_children(absD,settings);
            if  not (settings.get('ignoreFolder',False)): # If ignore folder then dont output folder in json.
                folder_structure.append(temp)
        else:
            if not ( settings.get('ignoreFile',False)) : # If ignore file then dont output file in json.
                folder_structure.append({'name' : d, 'basePath': basePath,'relPath':path.relpath(absD,basePath) , 'type' : ItemType.FILE, 'children': []})
        
    return folder_structure; # return as json.
        
def get_folder_structure(basePath,settings):
    # Add first level folder structure (base folder details)
    return {'name' : path.basename(basePath), 'basePath': path.dirname(basePath) , 'relPath':'','type' :ItemType.FOLDER, 'children': get_folder_structure_children(basePath,settings)}


settings = {
    #'ignoreFolder': True,
    'ignoreFile' : True,
}
# get folder structure json
#{
#"name": "impl",
#"basePath": "C:\\apple-workspace\\apple-server\\apple\\src\\main\\java\\com\\ap\\op\\apple\\application\\facade",
#"relPath": "impl",
#"type": "Folder",
#"children": []
# }
folder_structure = get_folder_structure(basePath,settings)

#################################################################################################

## Now from file list create folder

def create_folders_from_structure (folder_structure,toPath):
    for fs in folder_structure['children']:
        # extract relative path form 'fromPath'.
        pathToCreate = path.relpath(fs['basePath'],basePath)
        # Add folder name to path
        pathToCreate  = path.join(pathToCreate,fs['name'])
        # Remove extra . , which has come due to relPath.
        pathToCreate= path.normpath(pathToCreate)
        # join that relative folder path to 'toPath'
        folderToCreate = path.join(toPath,pathToCreate)
        try:
            os.mkdir(folderToCreate)
            print(f"Folder {fs['name']} has been created under {path.dirname(folderToCreate)}")
        except:
            print(f"Folder {fs['name']} skipped under {path.dirname(folderToCreate)}")
        if(len(fs['children']) > 0):
            create_folders_from_structure(fs,toPath)
            
            
create_folders_from_structure(folder_structure,toPath)
#with open('output.json', 'w+') as file:
#   json.dump(folder_structure,file, cls=EnumEncoder,indent=2)
#print(folder_structure);