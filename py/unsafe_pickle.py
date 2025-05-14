import pickle
data = input("Enter pickled data:")
obj = pickle.loads(data)
print(obj)
