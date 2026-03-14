from search import search

query = input("Ask something: ")

results = search(query)

print("\nTop results:\n")

for r in results:
    print("-", r)
