def string_twister(str) -> str:
    return str[::-1]

def word_count(str) -> int:
    return len(str.split())

print(string_twister("Hallo Welt!"))
print(word_count("Hallo Welt perro hijo de puta!"))