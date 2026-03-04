user = {
    "f_name": "Thomas",
    "l_name": "müller",
    "age": 53,
    "kids": [
        {"f_name": "Lena", "age": 20, "pet": ["dog", "cat"]},
        {"f_name": "Anna", "age": 5, "pet": ["fish", "lo"]},
        {"f_name": "Juan", "age": 15, "pet": ["cat", "fish"]},
        {"f_name": "Jose", "age": 10, "pet": ["lo", "bear"]}
    ]
}


print(user["kids"][0]["pet"][1])
print(user["kids"][1]["pet"][-1])
print(user["kids"][-2]["pet"][-1])
print(user["kids"][-1]["pet"][-1])
