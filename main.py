import eel
from random import randint
import os
from PyPDF2 import PdfWriter, PdfReader
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import re

user = os.getlogin()
dest_path = fr"C:\\Users\\{user}\\Documents\\"


def open_multiple_file():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_paths = tk.filedialog.askopenfilenames(title="Select multiple files")
        root.attributes('-topmost', False)
        if file_paths:
            return "|".join(file_paths)
        else:
            return "1"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "1"


def open_file():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = tk.filedialog.askopenfilename(title="Select a file")
        root.attributes('-topmost', False)
        if file_path:
            return file_path
        else:
            return "1"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "1"


def get_password(eCode):
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        if eCode == '5':
            password = simpledialog.askstring(
                title="Password",
                prompt="Incorrect password. Please enter the correct password: ",
                show='*'
            )
        else:
            password = simpledialog.askstring(
                title="Password",
                prompt="Enter the PDF password: ",
                show='*'
            )
        if password:
            return password
        else:
            messagebox.showerror("Error", "No password entered")
            return get_password(eCode)
    except Exception as e:
        print(f"An error occurred in get_password: {e}")
        return None
    finally:
        root.destroy()


def get_pages():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        pages = simpledialog.askstring(
            title="Pages",
            prompt="Enter the page numbers(either use ',' or '-') to split the PDF: "
        )
        if re.fullmatch(r'(\d+(-\d+)?)(,(\d+(-\d+)?))*', pages):
            pages = pages.split(",")
            a = set()
            for i in pages:
                if '-' in i:
                    start, end = map(int, i.split('-'))
                    a.update(range(min(start, end), max(start, end) + 1))
                else:
                    a.add(int(i))
            a.discard(0)
            return sorted(a)
        else:
            messagebox.showerror("Error", "Invalid format (e.g. 1,2,3 or 1-3 or 1,3,5-7)")
            return get_pages()
    except Exception as e:
        print(f"An error occurred in get_pages: {e}")
        return None
    finally:
        root.destroy()


@eel.expose
def merge_pdf():
    try:
        output = open_multiple_file()
        if output != "1":
            eel.showLoadingBar()
            merger = PdfWriter()
            for pdf in output.split("|"):
                merger.append(pdf)
            merger.write(f"{dest_path}merged_{randint(101,999)}.pdf")
            merger.close()
            return "0"
        else:
            return "1"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "1"


@eel.expose
def split_pdf():
    try:
        output = open_file()
        if output != "1":
            eel.showLoadingBar()
            reader = PdfReader(output)
            writer = PdfWriter()
            pages = get_pages()
            if pages:
                for page in pages:
                    if page <= len(reader.pages):
                        writer.add_page(reader.pages[page - 1])
                writer.write(f"{dest_path}split_pdf_{randint(101,999)}.pdf")
                writer.close()
                return "0"
            else:
                return "1"
        else:
            return "1"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "1"


@eel.expose
def decrypt_pdf():
    try:
        output = open_file()
        if output != "1":
            reader = PdfReader(output)
            writer = PdfWriter()
            if reader.is_encrypted:
                password = get_password('0')
                eel.showLoadingBar()
                for _ in range(3):
                    if reader.decrypt(password):
                        for page in reader.pages:
                            writer.add_page(page)
                        writer.write(f"{dest_path}decrypted_{randint(101,999)}.pdf")
                        writer.close()
                        return "0"
                    else:
                        password = get_password('5')
            else:
                for page in reader.pages:
                    writer.add_page(page)
                writer.write(f"{dest_path}decrypted_{randint(101,999)}.pdf")
                writer.close()
                return "0"
        else:
            return "1"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "1"


@eel.expose
def encrypt_pdf():
    try:
        output = open_file()
        if output != "1":
            reader = PdfReader(output)
            writer = PdfWriter()
            password = get_password('0')
            eel.showLoadingBar()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)
            writer.write(f"{dest_path}encrypted_{randint(101,999)}.pdf")
            writer.close()
            return "0"
        else:
            return "1"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "1"


@eel.expose
def compress_pdf():
    try:
        output = open_file()
        if output != "1":
            reader = PdfReader(output)
            writer = PdfWriter()
            eel.showLoadingBar()
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            writer.write(f"{dest_path}compressed_{randint(101,999)}.pdf")
            return "0"
        else:
            return "1"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "1"


@eel.expose
def open_dest():
    try:
        os.startfile(dest_path)
    except Exception as e:
        print(f"An error occurred in open_dest: {e}")


if __name__ == "__main__":
    try:
        eel.init(".")
        eel.start("index.html", block=True, disable_cache=True)
    except Exception as e:
        print(f"An error occurred while starting the application: {e}")
