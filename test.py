from hack_table import HashTable
import matplotlib.pyplot as plt

with open("text.txt", "r") as r:
	text = r.read()

def get_words(text):
    new_text = ""
    for el in text:

        # Избавляемся от знаков препинания и перехода строки
        if el not in [",", ".", ":", ";", "-", "\n"]:
            new_text += el

    return new_text.split(" ")

def get_unic_length(words):
	unic_words = []
	for word in words:
		if word not in unic_words:
			unic_words.append(word)
	return len(unic_words)

words = get_words(text)
length = get_unic_length(words)

Table_1 = HashTable(length)
Table_2 = HashTable(length)
graph_1 = []
graph_2 = []
collision_1 = []
collision_2 = []
size = []

for word in words:
	graph_1.append(Table_1.insert_linear_collision(word))
	graph_2.append(Table_2.insert_quadratic_collision(word))
	collision_1.append(Table_1.collisions)
	collision_2.append(Table_2.collisions)
	size.append(round(Table_1.size_now / length * 100))

fig, (ax1,ax2) = plt.subplots(1, 2)

ax1.plot(graph_1,size)
ax1.plot(graph_2,size)
ax2.plot(collision_1,size)
ax2.plot(collision_2,size)
plt.show()
