import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet

# -------------------------------
# Helper Functions
# -------------------------------

def generate_key():
    key = Fernet.generate_key().decode()
    key_entry.delete(0, tk.END)
    key_entry.insert(0, key)

def get_fernet():
    key = key_entry.get().strip()
    if not key:
        messagebox.showerror("Error", "Key cannot be empty")
        return None
    try:
        return Fernet(key.encode())
    except Exception:
        messagebox.showerror("Error", "Invalid Fernet key format.")
        return None

def encrypt_text():
    f = get_fernet()
    if not f:
        return
    text = encrypt_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Nothing to encrypt.")
        return
    try:
        encrypted = f.encrypt(text.encode()).decode()
        encrypt_output.delete("1.0", tk.END)
        encrypt_output.insert("1.0", encrypted)
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{e}")

def decrypt_text():
    f = get_fernet()
    if not f:
        return
    token = decrypt_input.get("1.0", tk.END).strip()
    if not token:
        messagebox.showerror("Error", "Nothing to decrypt.")
        return
    try:
        decrypted = f.decrypt(token.encode()).decode()
        decrypt_output.delete("1.0", tk.END)
        decrypt_output.insert("1.0", decrypted)
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed:\n{e}")


# -------------------------------
# GUI
# -------------------------------

root = tk.Tk()
root.title("Fernet Encrypt / Decrypt Tool")
root.geometry("650x500")

# Notebook for tabs
tabs = ttk.Notebook(root)
tabs.pack(expand=True, fill="both")

# ----- Key Frame -----
key_frame = ttk.Frame(root)
key_frame.pack(fill="x", padx=10, pady=10)

ttk.Label(key_frame, text="Fernet Key:").pack(side="left")
key_entry = ttk.Entry(key_frame, width=70)
key_entry.pack(side="left", padx=5)

generate_btn = ttk.Button(key_frame, text="Generate Key", command=generate_key)
generate_btn.pack(side="right")


# ----- Encrypt Tab -----
encrypt_tab = ttk.Frame(tabs)
tabs.add(encrypt_tab, text="Encrypt")

ttk.Label(encrypt_tab, text="Text to Encrypt:").pack(anchor="w", padx=10, pady=5)
encrypt_input = tk.Text(encrypt_tab, height=8)
encrypt_input.pack(fill="both", padx=10)

ttk.Button(encrypt_tab, text="Encrypt", command=encrypt_text).pack(pady=10)

ttk.Label(encrypt_tab, text="Encrypted Result:").pack(anchor="w", padx=10)
encrypt_output = tk.Text(encrypt_tab, height=8)
encrypt_output.pack(fill="both", padx=10, pady=5)


# ----- Decrypt Tab -----
decrypt_tab = ttk.Frame(tabs)
tabs.add(decrypt_tab, text="Decrypt")

ttk.Label(decrypt_tab, text="Encrypted Token:").pack(anchor="w", padx=10, pady=5)
decrypt_input = tk.Text(decrypt_tab, height=8)
decrypt_input.pack(fill="both", padx=10)

ttk.Button(decrypt_tab, text="Decrypt", command=decrypt_text).pack(pady=10)

ttk.Label(decrypt_tab, text="Decrypted Text:").pack(anchor="w", padx=10)
decrypt_output = tk.Text(decrypt_tab, height=8)
decrypt_output.pack(fill="both", padx=10, pady=5)


root.mainloop()
