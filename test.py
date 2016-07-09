titles_database = [1,1,1,1,1,1,1,2,2,2,22,2,3,3,3,3,3,3,3,3,3,4,5,6]
print titles_database
titles = titles_database
titles = sorted(titles)
uniques = set(titles)
print titles
print uniques
for unique in uniques:
    titles.remove(unique)

print titles
for title in titles:
    # db.pages.delete_one({'title': {'$regex': title}})
    titles_database.remove(title)
print set(sorted(titles_database))



