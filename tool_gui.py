import cv2, numpy as np, os, tkinter as tk
from tkinter import ttk, messagebox

# -------- Utility Functions --------
int_to_bits = lambda num, l: [int(b) for b in format(num, f'0{l}b')]
str_to_bits = lambda s: [int(b) for char in s for b in format(ord(char), '08b')]
bits_to_int = lambda bits: int("".join(str(b) for b in bits), 2)
bits_to_str = lambda bits: "".join(chr(int("".join(str(b) for b in bits[i:i+8]), 2)) for i in range(0, len(bits), 8))

def embed_data(img, data_bits):
    flat = img.flatten()
    if len(data_bits) > len(flat): 
        raise ValueError("Data too large to embed!")
    for i, bit in enumerate(data_bits):
        flat[i] = (flat[i] & 254) | bit
    return flat.reshape(img.shape)

# -------- Encryption & Decryption --------
def encrypt():
    folder = r"F:\Python\steganography project"  # Change if needed
    img_path = os.path.join(folder, "mypic.jpg")
    if not os.path.exists(img_path): 
        return messagebox.showerror("Error", "Input image not found!")
    image = cv2.imread(img_path)
    if image is None: 
        return messagebox.showerror("Error", "Failed to load image!")
    
    secret, code = enc_secret_message_entry.get(), enc_passcode_entry.get()
    if not secret or not code: 
        return messagebox.showerror("Error", "Secret message and passcode are required!")
    
    header = int_to_bits(len(code), 16) + str_to_bits(code) + int_to_bits(len(secret), 32) + str_to_bits(secret)
    try:
        encoded = embed_data(image, header)
    except ValueError as e:
        return messagebox.showerror("Error", str(e))
    
    cv2.imwrite(os.path.join(folder, "encryptedpic.png"), encoded)
    messagebox.showinfo("Success", "Encryption complete!")

def decrypt():
    folder = r"F:\Python\steganography project"  # Change if needed
    img_path = os.path.join(folder, "encryptedpic.png")
    if not os.path.exists(img_path): 
        return messagebox.showerror("Error", "Encrypted image not found!")
    image = cv2.imread(img_path)
    if image is None: 
        return messagebox.showerror("Error", "Failed to load encrypted image!")
    
    flat = image.flatten()
    # Retrieve passcode
    p_len = bits_to_int([flat[i] & 1 for i in range(16)])
    start = 16
    embedded_code = bits_to_str([flat[i] & 1 for i in range(start, start + p_len * 8)])
    start += p_len * 8
    # Retrieve secret message
    s_len = bits_to_int([flat[i] & 1 for i in range(start, start + 32)])
    start += 32
    secret = bits_to_str([flat[i] & 1 for i in range(start, start + s_len * 8)])
    
    if dec_passcode_entry.get() == embedded_code:
        messagebox.showinfo("Decryption Result", secret)
    else:
        messagebox.showerror("Error", "Incorrect passcode!")

# -------- GUI Setup --------
root = tk.Tk()
root.title("Steganography")
root.geometry("500x400")
root.resizable(True, True)
root.configure(bg='#2e2e2e')

style = ttk.Style(root)
style.theme_use('clam')
for widget in ['TFrame','TNotebook']:
    style.configure(widget, background='#2e2e2e')
style.configure('TLabel', background='#2e2e2e', foreground='white')
style.configure('TButton', background='#3e3e3e', foreground='white')
style.configure('TEntry', fieldbackground='#3e3e3e', foreground='white')
style.configure('TNotebook.Tab', background='#3e3e3e', foreground='white')
style.map('TNotebook.Tab', background=[('selected', '#1e1e1e')])

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# --- Encryption Tab ---
enc_tab = ttk.Frame(notebook, padding="20")
notebook.add(enc_tab, text="Encryption")
ttk.Label(enc_tab, text="Secret Message:").grid(row=0, column=0, sticky="w", pady=5)
enc_secret_message_entry = ttk.Entry(enc_tab, width=50)
enc_secret_message_entry.grid(row=1, column=0, pady=5)
ttk.Label(enc_tab, text="Passcode:").grid(row=2, column=0, sticky="w", pady=5)
enc_passcode_entry = ttk.Entry(enc_tab, width=50, show="*")
enc_passcode_entry.grid(row=3, column=0, pady=5)
ttk.Button(enc_tab, text="Encrypt", command=encrypt).grid(row=4, column=0, pady=20)

# --- Decryption Tab ---
dec_tab = ttk.Frame(notebook, padding="20")
notebook.add(dec_tab, text="Decryption")
ttk.Label(dec_tab, text="Enter Passcode:").grid(row=0, column=0, sticky="w", pady=5)
dec_passcode_entry = ttk.Entry(dec_tab, width=50, show="*")
dec_passcode_entry.grid(row=1, column=0, pady=5)
ttk.Button(dec_tab, text="Decrypt", command=decrypt).grid(row=2, column=0, pady=20)

root.mainloop()