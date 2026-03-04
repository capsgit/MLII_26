from pwinput import pwinput  # muss installiert werden

name = input("Benutzername: ")

passwort = pwinput("Passwort: ", mask='*')  # Das Passwort wird bei Eingabe mit "*" angezeigt.

