import pickle

# Step 1: Open the file in read-binary mode
with open('my_pick.pkl', 'rb') as file:
    # Step 2: Use pickle.load() to deserialize and load the dictionary
    loaded_dict = pickle.load(file)

oko=5