from nltk.corpus import wordnet as wn
food = wn.synset('food.n.02')
food_list = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
f = open('food_list.txt', 'w')
for food_item in food_list:
    food_item = food_item.replace('_',' ')
    f.write(food_item)
    f.write('\n')
f.close()
