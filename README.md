# 🤖 AI Chatbot Desktop App (PyQt6)

A simple AI-powered chatbot desktop application built using Python and PyQt6.  
The project includes a graphical user interface, basic NLP response system, and memory storage using JSON.

---

## ✨ Features

- 💬 Chat-style GUI using PyQt6
- 🧠 Smart response system (TF-IDF based similarity)
- 💾 Memory system (saves chat history in JSON)
- 📁 Multiple chat sessions support
- 📊 Simple dashboard for chat statistics
- ⚡ Lightweight and fast desktop application

---

## 🛠️ Technologies Used

- Python 3.x
- PyQt6 (GUI)
- scikit-learn (NLP - TF-IDF)
- JSON (Data storage)

---

## 📁 Project Structure

```

Chatbot-Project/
│
├── chatbot.py          # Main application file
├── memory.json         # Chat memory storage (auto-generated)
└── README.md

````

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/chatbot-project.git
cd chatbot-project
````

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

Run the application using:

```bash
python chatbot.py
```

---

## 🧠 How it works

* The chatbot uses a simple NLP technique (TF-IDF + Cosine Similarity)
* It compares user input with predefined intents
* If no match is found, it returns a fallback response
* Chat history is stored locally in `memory.json`

---

## 📊 Dashboard

The app includes a simple dashboard that shows:

* Number of chats
* Number of messages
* Current active chat

---

## 💡 Future Improvements

* Add voice input/output 🎤
* Integrate OpenAI API 🤖
* Improve UI design (modern ChatGPT-like interface)
* Export chat as PDF 📄

---

## 👩‍💻 Author

Developed by: *Asmaa Mohamed*
Field: Artificial Intelligence Student
