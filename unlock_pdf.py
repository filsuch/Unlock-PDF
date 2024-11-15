import os
import subprocess
import sys
import time  


def check_and_install_package(package):
    try:
        __import__(package)
        print(f"Knihovna '{package}' je již nainstalována.")
    except ImportError:
        print(f"Knihovna '{package}' není nainstalována. Instalace...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


check_and_install_package("PyPDF2")
check_and_install_package("pycryptodome")


from PyPDF2 import PdfReader, PdfWriter


script_directory = os.path.dirname(os.path.abspath(__file__))


heslo = "heslo" #zadej heslo pdf
lock_folder = os.path.join(script_directory, "lock")
unlock_folder = os.path.join(script_directory, "unlock")


if not os.path.exists(lock_folder):
    os.makedirs(lock_folder)
    print(f"Složka '{lock_folder}' vytvořena.")

if not os.path.exists(unlock_folder):
    os.makedirs(unlock_folder)
    print(f"Složka '{unlock_folder}' vytvořena.")


for filename in os.listdir(lock_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(lock_folder, filename)
        try:
           
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                
              
                if reader.is_encrypted:
                    reader.decrypt(heslo)  
                    
                  
                    writer = PdfWriter()
                    for page_num in range(len(reader.pages)):
                        writer.add_page(reader.pages[page_num])
                    
                  
                    output_path = os.path.join(unlock_folder, filename)
                    
                  
                    with open(output_path, "wb") as output_file:
                        writer.write(output_file)
                    
                    print(f"Soubor '{filename}' byl úspěšně odheslován a přesunut do složky '{unlock_folder}'.")
                    
                    
                    time.sleep(1)
                    
                   
                    os.remove(file_path)
                else:
                    print(f"Soubor '{filename}' není zaheslovaný.")
        except Exception as e:
            print(f"Chyba při zpracování souboru '{filename}': {e}")
