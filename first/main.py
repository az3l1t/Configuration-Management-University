import os
import zipfile
#Разработать эмулятор командной строки vshell. 
# В качестве аргумента vshell принимает образ файловой системы известного формата (tar, zip).
# Обратите внимание: программа должна запускаться прямо из командной строки, 
# а файл с виртуальной файловой системой не нужно распаковывать у пользователя.
# В vshell должны поддерживаться команды pwd, ls, cd и cat. 
# Ваша задача сделать работу vshell как можно более похожей на сеанс bash в Linux. 
# Реализовать vshell можно на Python или других ЯП, но кроссплатформенным образом.
class VShell:
    def __init__(self, zip_file):
        self.zip_file = zip_file
        self.current_path = ""

    def run(self):
        if not self.extract_zip_file():
            print("Failed to extract ZIP file")
            return
        
        while True:
            command = input(f"{self.current_path}$ ")
            if command == "exit":
                break
            elif command.startswith("cd "):
                self.change_directory(command[3:])
            elif command == "pwd":
                self.print_working_directory()
            elif command == "ls":
                self.list_directory()
            elif command.startswith("cat "):
                self.print_file_content(command[4:])
            else:
                print("Unknown command")

        self.cleanup()
    
    def extract_zip_file(self):
        try:
            with zipfile.ZipFile(self.zip_file, "r") as zip_ref:
                file_list = zip_ref.namelist()
                common_prefix = os.path.commonprefix(file_list)
                if common_prefix.endswith('/'):
                    self.current_path = common_prefix
                else:
                    self.current_path = os.path.dirname(common_prefix) + '/'
        except Exception as e:
            print(f"Failed to extract ZIP file: {str(e)}")
            return False
        return True
        
    def cleanup(self):
        try:
            os.remove(self.zip_file)
        except OSError:
            pass
    
    def change_directory(self, path):
        new_path = os.path.join(self.current_path, path)
        new_path = os.path.normpath(new_path)
        if new_path[-1] == "/":
            new_path = new_path[:-1]
        if os.path.isdir(os.path.join(self.zip_file, new_path)):
            self.current_path = new_path
        else:
            print(f"Directory {new_path} does not exist")
    
    def print_working_directory(self):
        print(self.current_path)
    
    def list_directory(self):
        file_list = []
        with zipfile.ZipFile(self.zip_file, "r") as zip_ref:
            for name in zip_ref.namelist():
                if name.startswith(self.current_path) and name != self.current_path:
                    file_list.append(name[len(self.current_path):].split('/')[0])
                    
        for file in set(file_list):
            print(file)
    
    def print_file_content(self, file_name):
        file_path = os.path.join(self.current_path, file_name)
        with zipfile.ZipFile(self.zip_file, "r") as zip_ref:
            try:
                with zip_ref.open(file_path, "r") as file:
                    print(file.read().decode())
            except KeyError:
                print(f"File {file_name} does not exist")

if __name__ == "__main__":
    zip_file = input("Enter the path to the ZIP file: ")
    vshell = VShell(zip_file)
    vshell.run()
