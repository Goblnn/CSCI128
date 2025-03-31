import matplotlib.pyplot as plt

categories = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"]
votes = [20, 12, 14, 25, 29, 4, 9]
colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"] 

plt.bar(categories, votes, color=colors) 
plt.title("What is your favorite color?")
plt.xlabel("Colors")
plt.ylabel("Votes")

plt.show()