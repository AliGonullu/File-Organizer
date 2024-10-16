import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def organize_files(directory: str):
    file_types = {
        'Word Files': ['.docx', '.doc', '.rtf', '.odt'],
        'PDF Files': ['.pdf'],
        'Text Files': ['.txt', '.md', '.log'],
        'Spreadsheets': ['.xlsx', '.xls', '.ods', '.xlsm'],
        'Presentations': ['.pptx', '.ppt', '.odp', '.key'],
        'Data Files': ['.json', '.csv', '.xml', '.yaml', '.yml', '.pickle'],
        'Configuration Files': ['.ini', '.cfg', '.env', '.properties'],
        'Executables': ['.exe', '.msi', '.bat', '.sh', '.bin', '.apk'],
        'Scripts': ['.py', '.js', '.html', '.css', '.c', '.cpp', '.java', '.rb', '.php', '.go', '.ts', '.swift', '.r', '.pl'],
        'Database Files': ['.sql', '.db', '.sqlite', '.db3', '.accdb', '.mdb'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.heic', '.webp', '.ico', '.raw'],
        'Vector Graphics': ['.svg', '.eps', '.ai'],
        'Music': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'],
        'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.m4v'],
        '3D Models': ['.obj', '.fbx', '.stl', '.3ds', '.blend'],
        'Compressed Files': ['.zip', '.rar', '.tar', '.gz', '.7z', '.iso', '.bz2', '.xz'],
        'Disk Images': ['.iso', '.img', '.vdi', '.vmdk'],
        'Web Files': ['.html', '.htm', '.css', '.js', '.php', '.aspx', '.jsp'],
        'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
        'CAD Files': ['.dwg', '.dxf', '.step', '.stp'],
        'Design Files': ['.psd', '.ai', '.xd', '.sketch', '.fig'],
        'Audio Production': ['.flp', '.als', '.aiff', '.logicx'],
        'Programming Languages': ['.py', '.java', '.cpp', '.c', '.js', '.ts', '.go', '.rs', '.swift', '.r', '.jl', '.pl', '.sh', '.bat'],
        'System Files': ['.sys', '.dll', '.drv'],
        'Logs': ['.log', '.out', '.err'],
        'Backup Files': ['.bak', '.tmp', '.old'],
        'GIS Files': ['.shp', '.gpx', '.kml', '.kmz', '.geojson'],
        'Documents': ['.pdf', '.doc', '.docx', '.odt', '.rtf', '.txt'],
        'Others': []
    }

    directory_path = Path(directory)
    if not directory_path.is_dir():
        print(f"Error: '{directory}' is not a valid directory path.")
        return

    for folder_name in file_types.keys():
        folder_path = directory_path / folder_name
        folder_path.mkdir(exist_ok=True)

    for file_path in directory_path.iterdir():
        if file_path.is_file():
            file_extension = file_path.suffix.lower()
            moved = False

            for folder_name, extensions in file_types.items():
                if file_extension in extensions:
                    target_folder = directory_path / folder_name
                    move_file(file_path, target_folder)
                    moved = True
                    break

            if not moved:
                move_file(file_path, directory_path / 'Others')

    remove_empty_folders(directory_path)
    print(f"Files in '{directory}' have been organized successfully.")

def move_file(file_path: Path, target_folder: Path):
    destination = target_folder / file_path.name

    if destination.exists():
        base = file_path.stem
        extension = file_path.suffix
        counter = 1

        while destination.exists():
            destination = target_folder / f"{base}_{counter}{extension}"
            counter += 1

    shutil.move(str(file_path), str(destination))
    print(f"Moved: '{file_path.name}' -> '{destination}'")

def remove_empty_folders(directory_path: Path):
    for folder_path in directory_path.iterdir():
        if folder_path.is_dir() and not any(folder_path.iterdir()):
            folder_path.rmdir()
            print(f"Removed empty folder: '{folder_path.name}'")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_path.set(directory)
        output_log.insert(tk.END, f"Selected directory: {directory}\n")

def organize():
    directory = directory_path.get()
    if not directory:
        messagebox.showwarning("Warning", "Please select a directory first.")
        return

    output_log.insert(tk.END, "Starting file organization...\n")
    try:
        organize_files(directory)
        output_log.insert(tk.END, "File organization completed successfully!\n")
    except Exception as e:
        output_log.insert(tk.END, f"Error: {e}\n")

root = tk.Tk()
root.title("Python File Organizer")
root.geometry("550x600")

directory_path = tk.StringVar()
tk.Label(root, text="Select Directory to Organize:").pack(pady=5)
tk.Entry(root, textvariable=directory_path, width=50).pack(padx=10, pady=5)
tk.Button(root, text="Browse", command=select_directory, bg="darkred", fg="white").pack(pady=5)
tk.Button(root, text="Organize Files", command=organize, bg="green", fg="white").pack(pady=15)

output_log = scrolledtext.ScrolledText(root, width=60, height=10)
output_log.pack(pady=5)

root.mainloop()
