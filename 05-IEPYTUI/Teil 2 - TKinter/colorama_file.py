from colorama import init, Fore

# Initialisiere colorama (besonders wichtig unter Windows)
init()

print(Fore.GREEN + "ICH BIN GRÜN")
print(Fore.RED + "ICH BIN ROT")
print(Fore.BLUE + "ICH BIN BLAU")
print(Fore.YELLOW + "ICH BIN GELB")

# Zurücksetzen auf Standardfarbe (falls nötig)
print(Fore.RESET + "ICH BIN WIEDER NOR-.MAL")