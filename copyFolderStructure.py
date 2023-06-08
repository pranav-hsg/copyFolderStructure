
import os;
from os import path ;
import argparse;
import json;
# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Define the flags/arguments
parser.add_argument('--fromPath', type=str, help='Path from which you want to copy folder structure.')
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
class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, enum.Enum):
            return obj.value
        return super().default(obj)

def get_type(item):
    mapping = {
        path.isfile(item) : ItemType.FILE  ,
        path.isdir(item): ItemType.FOLDER
    }
    return mapping.get(True)
def get_folder_structure_children(basePath,settings={}):
    dirs = os.listdir(basePath)
    folder_structure = []
    for d in dirs:
        absD = path.join(basePath,d)
        if(get_type(absD) == ItemType.FOLDER):
            temp = {'name' : d, 'basePath': basePath,'relPath':path.relpath(absD,basePath) , 'type' : ItemType.FOLDER, 'children': []}
            temp['children'] = get_folder_structure_children(absD,settings);
            if  not (settings.get('ignoreFolder',False)):
                folder_structure.append(temp)
        else:
            if not ( settings.get('ignoreFile',False)) :
                folder_structure.append({'name' : d, 'basePath': basePath,'relPath':path.relpath(absD,basePath) , 'type' : ItemType.FILE, 'children': []})
        
    return folder_structure;
        
def get_folder_structure(basePath,settings):
    return {'name' : path.basename(basePath), 'basePath': path.dirname(basePath) , 'relPath':'','type' :ItemType.FOLDER, 'children': get_folder_structure_children(basePath,settings)}


settings = {
    #'ignoreFolder': True,
    'ignoreFile' : True,
}
folder_structure = get_folder_structure(basePath,settings)

#################################################################################################

## Now from file list create folder

def create_folders_from_structure (folder_structure,toPath):
    for fs in folder_structure['children']:
        pathToCreate = path.relpath(fs['basePath'],basePath)
        pathToCreate  = path.join(pathToCreate,fs['name'])
        pathToCreate= path.normpath(pathToCreate)
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