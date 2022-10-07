# Password manager
import random

# -------------imports------------
from cryptography.fernet import Fernet


# --------------------------------

# ------------Class---------------
class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]


def main():
    # declarate
    pm = PasswordManager()

    done = False
    while not done:
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("enter the path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("enter the path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("enter the path: ")
            password = input("enter your password: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("enter the path: ")
            pm.load_password_file(path)
        elif choice == "5":
            site = input("enter the site: ")
            # no_encrypted
            lower = "abcdefghijklmnopqrstuvwxyz"
            cap = lower.upper()
            num = "0123456789"
            simb = "@()[]{}*,:/-_¿?.!$<#>&+%=`"

            base = lower + cap + num + simb
            lengt = 12
            result = random.sample(base, lengt)
            password = "".join(result)
            pm.add_password(site, password)
