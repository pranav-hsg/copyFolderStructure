import os
import shutil
extension_mapping = {
    'excel-files': ['xls', 'xlsx', 'csv'],
    'text-files': ['txt', 'md', 'log'],
    'image-files': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
    'audio-files': ['mp3', 'wav', 'ogg', 'flac'],
    'video-files': ['mp4', 'avi', 'mov', 'wmv', 'mkv'],
    'pdf-files': ['pdf'],
    'presentation-files': ['ppt', 'pptx'],
    'document-files': ['doc', 'docx','vdsx'],
    'compressed-files': ['zip', 'rar', '7z'],
    'json-files': ['json'],
    'sql-files': ['sql'],
    'jasper-files': ['jrxml','jasper'],
    'shell-files':['sh']
}
os.chdir("C:/Users/Sensei Team/OneDrive/Desktop")
print(f"Organizing files inside : {os.getcwd()} ")
def move_files_to_folder(file_extensions, folder_name):
    # Get all the files in the current directory
    all_files = os.listdir()

    # Filter the files by extension and move them to the folder
    for file in all_files:
        if any(file.endswith(ext) for ext in file_extensions):
            if not os.path.exists(folder_name):
                print(f"Directory {folder_name} does not exists creating one for you.")
                os.makedirs(folder_name)
            shutil.move(file, folder_name)
            print(f"Moving file {file} to {folder_name} ")
            
# Example usage:

for folder_name, file_extensions in extension_mapping.items():
	move_files_to_folder(file_extensions, os.path.join('auto-organizer',folder_name))
	
	
print("Finished organizing files!")