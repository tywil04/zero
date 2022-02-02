"""
Password Generator

All packages used in this script are built-in packages.

This application has a graphical user interface - it does this with the aid of the TK UI toolkit.

Function names with _ is just a naming convention that signifies that these are internal functions only.

This application uses the my "Williams" ttk theme to make Tkinter look nice and modern.

~Tyler Williams
"""

import string;
import re;
import tkinter as tk;
from tkinter import ttk;
from tkinter import messagebox as mb;
import os;

# Global Settings
theme = "dark";

# Global Variables
cwd = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"); # Current working directory

class ceasar():
    def encode(self, key, plaintext, keepCase=True, keepUnknown=False) -> str:
        try:
            key = int(key);
            plaintext = str(plaintext).strip();

            ciphertext = "";
            for i in range(len(plaintext)):
                if re.match("[a-zA-Z]", plaintext[i]): # Check if plaintext[i] is only made up of letters (lowercase and uppercase)
                    abcPos = string.ascii_lowercase.index(plaintext[(i)].lower());
                    ciphertext += string.ascii_lowercase[(abcPos + key) % len(string.ascii_lowercase)];
                else:
                    if keepUnknown == True:
                        ciphertext += plaintext[i];

            return "".join([(lambda: ciphertext[i].upper() if plaintext[i].isupper() and keepCase == True else ciphertext[i].lower())() for i in range(len(ciphertext))]); # Sets the same capitalisation pattern that plaintext has
        except:
            mb.showerror(title="Error", message="Error Encountered!");

    def decode(self, key, ciphertext, keepCase=True, keepUnknown=False) -> str:
        try:
            key = int(key);
            ciphertext = ciphertext.strip();

            plaintext = "";
            for i in range(len(ciphertext)):
                try:
                    abcPos = string.ascii_lowercase.index(ciphertext[(i)].lower());
                    plaintext += string.ascii_lowercase[(abcPos - key) % len(string.ascii_lowercase)];
                except:
                    if keepUnknown == True:
                        plaintext += ciphertext[i];

            return "".join([(lambda: plaintext[i].upper() if ciphertext[i].isupper() and keepCase == True else plaintext[i].lower())() for i in range(len(plaintext))]); # Sets the same capitalisation pattern that plaintext has
        except:
            mb.showerror(title="Error", message="Error Encountered!");

class vigenere():
    def __init__(self) -> None:
        # Generate Vigenere Square
        self.vsquare = [];
        currentABC = [c for c in string.ascii_lowercase];

        for i in range(26):
            self.vsquare.append(currentABC);
            currentABC = currentABC.copy();
            currentABC.append(currentABC[0]);
            currentABC.remove(currentABC[0]);

    def encode(self, secret, plaintext, keepCase=True, keepUnknown=False) -> str:
        try:
            plaintext = str(plaintext).strip();
            secret = str(secret).strip();

            if keepUnknown == False:
                plaintext = plaintext.replace(r"[^a-zA-Z]", "");
                secret = secret.replace(r"[^a-zA-Z]", "");

            ciphertext = "";
            counter = 0;
            for i in range(len(plaintext)):
                if not re.match(r"[^a-zA-Z]", plaintext[i]):
                    result = self.vsquare[string.ascii_lowercase.index(secret[(i - counter) % len(secret)].lower())][string.ascii_lowercase.index(plaintext[i].lower())];
                    ciphertext += (lambda: result.upper() if plaintext[i].isupper() and keepCase == True else result.lower())();
                elif keepUnknown == True:
                    ciphertext += plaintext[i];
                else:
                    counter += 1;

            return ciphertext;
        except:
            mb.showerror(title="Error", message="Error Encountered!");

    def decode(self, secret, ciphertext, keepCase=True, keepUnknown=False) -> str:
        try:
            ciphertext = ciphertext.strip();
            secret = secret.strip();

            if keepUnknown == False:
                ciphertext = ciphertext.replace(r"[^a-zA-Z]", "");
                secret = secret.replace(r"[^a-zA-Z]", "");

            plaintext = "";
            counter = 0;
            for i in range(len(ciphertext)):
                if not re.match(r"[^a-zA-Z]", ciphertext[i]):
                    result = string.ascii_lowercase[self.vsquare[string.ascii_lowercase.index(secret[(i - counter) % len(secret)].lower())].index(ciphertext[i].lower())];
                    plaintext += (lambda: result.upper() if ciphertext[i].isupper() and keepCase == True else result.lower())();
                elif keepUnknown == True:
                    plaintext += ciphertext[i];
                else:
                    counter += 1;

            return plaintext;
        except:
            mb.showerror(title="Error", message="Error Encountered!");

class vernan():
    def encode(self, secret, plaintext, keepCase=True, hasWhitespaces=True) -> str:
        try:
            plaintext = re.sub(r"[^a-zA-Z]", "", str(plaintext).strip())
            secret = re.sub(r"[^a-zA-Z]", "", str(secret).strip())

            if keepCase == True:
                chars = string.ascii_letters;
            else:
                chars = string.ascii_lowercase;
                plaintext = plaintext.lower();

            key = "".join([secret * len(plaintext)])[:len(plaintext)];
            ciphertext = (lambda: " " if hasWhitespaces else "")().join([bin(chars.index(plaintext[i]) ^ chars.index(key[i]))[2:].zfill(8) for i in range(len(plaintext))]);

            return ciphertext;
        except:
            mb.showerror(title="Error", message="Error Encountered!");
            return;

    def decode(self, secret, ciphertext, keepCase=True, hasWhitespaces=True) -> str:
        try:
            ciphertext = ciphertext.strip().replace(" ", "");
            secret = secret.strip().replace(" ", "");

            if keepCase == True:
                chars = string.ascii_letters;
            else:
                chars = string.ascii_lowercase;
                plaintext = ciphertext.lower();

            ciphertextArray = re.findall( "........", ciphertext);
            key = "".join([secret * len(ciphertext)])[:len(ciphertext)];
            plaintext = "".join([chars[int(ciphertextArray[i], 2) ^ chars.index(key[i])] for i in range(len(ciphertextArray))]);

            return plaintext;
        except:
            mb.showerror(title="Error", message="Error Encountered!");
            return;

class cipherWindow():
    def __init__(self) -> None:
        def _writeToDisplay(string) -> None:
            self.outputWindow["state"] = ""
            self.outputWindow.delete(0, len(self.outputWindow.get()))
            self.outputWindow.insert(0, string);
            self.outputWindow["state"] = "readonly";

        def _generateCipher() -> None:
            if self.currentSelectedCipher.get() == "Select Cipher":
                mb.showerror(title="Error", message="Error: No cipher selected");
                return;

            elif self.plaintext.get().strip() == self.plaintextPlaceholder or self.secret.get().strip() == self.secretPlaceholder:
                mb.showerror(title="Error", message="Error: No plaintext/secret found");
                return;

            if self.currentSelectedCipher.get() == "Encode Ceasar" or self.currentSelectedCipher.get() == "Decode Ceasar":
                try: int(self.secret.get());
                except: mb.showerror(title="Error", message="Error: Ceasar cipher needs a number for a key"); return;
            elif re.match(r"[^a-zA-Z]", self.secret.get()):
                mb.showerror(title="Error", message="Error: Key needs to only contain a-z A-Z. No numbers or special characters."); 
                return;
            
            _writeToDisplay(self.ciphers[self.currentSelectedCipher.get()](self.secret.get(), self.plaintext.get(), self.setting1Bool.get(), self.setting2Bool.get()));

        def _updateSettingsLabels(new) -> None:
            if new == "Encode Vernan" or new == "Decode Vernan":
                self.setting2["text"] = "Seperate Binary";
            else:
                self.setting2["text"] = "Keep Unknown Characters";

        def _copyOutput() -> None: self.window.clipboard_clear(); self.window.clipboard_append(self.outputWindow.get());

        def _controlA(event) -> None: event.widget.select_range(0, "end"); event.widget.icursor("end"); return "break";

        self.ciphers = {
            "Encode Ceasar": ceasar().encode,
            "Encode Vigenere": vigenere().encode,
            "Encode Vernan": vernan().encode,
            "Decode Ceasar": ceasar().decode,
            "Decode Vigenere": vigenere().decode,
            "Decode Vernan": vernan().decode,
        }

        # Window
        self.window = tk.Tk(); # Create window
        self.window.call("source", cwd + "/Williams Theme/Williams.tcl");
        ttk.Style().theme_use('Williams');
        self.window.title("Cipher Suite");
        self.window.geometry("420x225");
        self.window.resizable(width=False, height=False);

        self.currentSelectedCipher = tk.StringVar(self.window);
        self.cipherSelector = ttk.OptionMenu(self.window , self.currentSelectedCipher, "Select Cipher", *list(self.ciphers.keys()), command=_updateSettingsLabels);
        self.cipherSelector.place(x=10, y=10, width=145, height=35);

        # Output Display
        self.outputWindow = ttk.Entry(self.window, state="readonly");
        self.outputWindow.place(x=165, y=10, width=175, height=35);

        self.copy = ttk.Button(self.window, text="Copy", command=_copyOutput);
        self.copy.place(x=350, y=10, width=60, height=35)

        # Inputs
        self.plaintextPlaceholder = "Enter Plaintext/Ciphertext";
        self.plaintext = ttk.Entry(self.window);
        self.plaintext.place(x=10, y=55, width=400, height=35);
        self.plaintext.insert(0, self.plaintextPlaceholder)
        self.plaintext.bind("<FocusIn>", lambda e: self.plaintext.delete(0, len(self.plaintextPlaceholder)) if self.plaintext.get().strip() == self.plaintextPlaceholder else "");
        self.plaintext.bind("<FocusOut>", lambda e: self.plaintext.insert(0, self.plaintextPlaceholder) if len(self.plaintext.get().strip()) == 0 else "");
        self.plaintext.bind("<Control-a>", _controlA);

        # Manage Placeholder Text
        self.secretPlaceholder = "Enter Key";
        self.secret = ttk.Entry(self.window);
        self.secret.place(x=10, y=100, width=400, height=35);
        self.secret.insert(0, self.secretPlaceholder)
        self.secret.bind("<FocusIn>", lambda e: self.secret.delete(0, len(self.secretPlaceholder)) if self.secret.get().strip() == self.secretPlaceholder else "");
        self.secret.bind("<FocusOut>", lambda e: self.secret.insert(0, self.secretPlaceholder) if len(self.secret.get().strip()) == 0 else "");
        self.secret.bind("<Control-a>", _controlA);

        # Settings
        self.setting1Bool = tk.BooleanVar(self.window);
        self.setting1 = ttk.Checkbutton(self.window, text="Keep Character Case", style="Switch", onvalue=True, offvalue=False, variable=self.setting1Bool)
        self.setting1.place(x=10, y=147.5, width=180, height=20);

        self.setting2Bool = tk.BooleanVar(self.window);
        self.setting2 = ttk.Checkbutton(self.window, text="Keep Unknown Characters", style="Switch", onvalue=True, offvalue=False, variable=self.setting2Bool)
        self.setting2.place(x=195, y=147.5, width=255, height=20);

        # Run Button
        self.run = ttk.Button(self.window, style="Accent", text="Compute", command=_generateCipher);
        self.run.place(x=10, y=180, width=400, height=35);

        # Start Window Loop
        self.window.mainloop();

cipherWindow();
