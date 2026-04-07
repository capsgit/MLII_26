
# NLTK 
from textblob import TextBlob


text = "The movie is great. But the colors are bad. In Total , i am happy with the movie." 

blob = TextBlob(text)

total_polarity = 0 

print(blob)
# Polarity (-1 to 1) and Subjectivity (0 to 1)

for sentence in blob.sentences:
    print(sentence, "---->", sentence.sentiment.polarity)
    total_polarity += sentence.sentiment.polarity 

mean_polarity = total_polarity/len(blob.sentences)

print(f"THe total Polarity is {mean_polarity}")

if mean_polarity > 0:
    print("The overall sentiment is Positive")
else:
    print("The overall sentiment is Negative")
    





