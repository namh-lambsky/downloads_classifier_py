import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Categories that will be observed
categories = {
    "Documents": [".pdf", ".docx", ".xlsx",".csv",".r",".py",".txt",".rtf"],
    "Images": [".jpg", ".png", ".gif",".jpeg",".webp",".NEF"],
    "Videos": [".mp4", ".mov"],
    "Compressed Files": [".zip", ".rar",".7zip"],
    "Executables":[".exe",".jar"],
    "Adobe files":[".psd",".ai"]
}

#Class that manages the directory
class FileHandler(FileSystemEventHandler):
    def __init__(self,base_dir):
        self.base_dir=base_dir

    def on_created(self, event):
        #Checks files on creation
        if os.path.isfile(event.src_path):
            self.organize_file(event.src_path)

    def organize_existing_items(self):
        #Checks for any existing files on the directory
        print("Organizing existing files...")
        for item in os.listdir(downloads_directory):
            item_path = os.path.join(downloads_directory, item)
            if os.path.isfile(item_path):
                self.organize_file(item_path)
        print("Files Organized!")

    def organize_file(self, filepath):
        #Classifies a file given its extension
        _, ext = os.path.splitext(filepath)
        for category, extensions in categories.items():
            if ext.lower() in extensions:
                dest_dir = os.path.join(downloads_directory, category)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(filepath, dest_dir)
                print(f"File {os.path.basename(filepath)} moved to {dest_dir}")
                break

if __name__ == "__main__":
    #Directory path given the current windows user
    downloads_directory=os.path.expanduser("~/Downloads")
    #Instance of FileHandler Class
    handler=FileHandler(downloads_directory)
    #Organizing Files before constant monitoring
    handler.organize_existing_items()
    #Creating the directory observer
    observer=Observer()
    observer.schedule(handler,downloads_directory,recursive=False)
    observer.start()

