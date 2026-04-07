from textblob import TextBlob

# un texto NL cualquiera con puntos y comas
text = "The film was good. The history was horrible. But in total i´m not happy"
blob = TextBlob(text)
mean = 0

print(blob)

for sentence in blob.sentences:
    print("\n","***" * 10)
    print("Sentence: ", sentence, "||", "Polarity: ", sentence.polarity, "||", "Subjectivity:", sentence.subjectivity)

    mean += sentence.sentiment.polarity

polaridad = mean/len(blob.sentences)

print(f"\n\nla polaridad es {polaridad}")

if polaridad > 0:
    print("in total the polaridad is positive")
elif polaridad < 0:
    print("in total the polaridad is negative")
elif polaridad == 0:
    print("in total the polaridad is zero")
else:
    print("error")