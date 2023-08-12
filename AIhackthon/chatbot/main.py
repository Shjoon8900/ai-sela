import streamlit as st
import random
import json
import os
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Load model and other data (similar to your original code)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# os.chdir("d:\Projects\chatbot")
# ... (rest of your code)
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "chatbot_qa.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Four"

# Streamlit App
def main():
    st.title("Chatbot Service")
    st.write("Your problem will be solved, don't worry!")

    sentence = st.text_input("You:", "")

    if st.button("Send"):

        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    bot_response = random.choice(intent['responses'])
                    st.write(f"{bot_name}: {bot_response}")
                    break
        else:
            st.write(f"{bot_name}: I do not understand...")

if __name__ == "__main__":
    main()
