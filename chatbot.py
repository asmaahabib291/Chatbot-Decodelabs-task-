import sys
import json
import os

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# KNOWLEDGE BASE (Expanded)
# =========================
INTENTS = {
    "hello": "Hey 👋 How can I help you today?",
    "hi": "Hello 👋",
    "how are you": "I'm doing great 🤖 thanks for asking!",
    "what is your name": "I'm your AI assistant 🤖",
    "who are you": "I'm a smart chatbot built with Python",
    "help me": "Sure 👍 tell me your problem",
    "thank you": "You're welcome 😊",
    "bye": "Goodbye 👋",

    # daily questions
    "what time is it": "I can't see real time yet, but your system knows it ⏰",
    "what is ai": "AI means Artificial Intelligence 🤖",
    "what is python": "Python is a powerful programming language 🐍",
    "how to learn programming": "Start with basics, practice daily, and build projects 💡",
    "what is machine learning": "It's a branch of AI where machines learn from data 📊",
    "what is data science": "Field that combines data, statistics and AI 📈",
    "how are you today": "I'm always fine 🤖",
    "tell me a joke": "Why did the computer get cold? It left its Windows open 😂",
    "good morning": "Good morning ☀️ hope you have a great day!",
    "good night": "Good night 🌙 sleep well!",
}


# =========================
# BOT ENGINE (NLP upgrade)
# =========================
class ChatBot:
    def __init__(self):
        self.questions = list(INTENTS.keys())
        self.answers = list(INTENTS.values())

        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(self.questions)

    def get_reply(self, msg):
        msg = msg.lower().strip()

        user_vec = self.vectorizer.transform([msg])
        similarity = cosine_similarity(user_vec, self.vectors)

        best_index = similarity.argmax()
        best_score = similarity[0, best_index]

        if best_score > 0.3:
            return self.answers[best_index]

        if "sad" in msg or "bad" in msg:
            return "I'm here for you 🤍 stay strong"

        if "?" in msg:
            return "That's interesting 🤖 I'm still learning that topic"

        return "I don't fully understand yet 🤖 but I'm improving daily"


# =========================
# MAIN APP
# =========================
class ChatApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Chat Pro 🚀")
        self.resize(1000, 650)
        self.setStyleSheet("background:#0f0f0f; color:white;")

        self.bot = ChatBot()

        self.data_file = "memory.json"
        self.chats = self.load_data()

        if not self.chats:
            self.chats = {"Chat 1": []}

        self.current_chat = "Chat 1"

        self.build_ui()
        self.load_chat()

    # ================= UI =================
    def build_ui(self):
        layout = QHBoxLayout()

        # ===== Sidebar =====
        left = QVBoxLayout()

        self.sidebar = QListWidget()
        self.sidebar.addItems(self.chats.keys())
        self.sidebar.itemClicked.connect(self.switch_chat)

        new_chat_btn = QPushButton("➕ New Chat")
        new_chat_btn.clicked.connect(self.new_chat)

        stats_btn = QPushButton("📊 Dashboard")
        stats_btn.clicked.connect(self.show_dashboard)

        left.addWidget(self.sidebar)
        left.addWidget(new_chat_btn)
        left.addWidget(stats_btn)

        # ===== Chat area =====
        right = QVBoxLayout()

        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignmentFlag.AlignTop)

        container = QWidget()
        container.setLayout(self.chat_area)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(container)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type message...")
        self.input.returnPressed.connect(self.send)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send)

        right.addWidget(self.scroll)
        right.addWidget(self.input)
        right.addWidget(send_btn)

        layout.addLayout(left, 1)
        layout.addLayout(right, 3)

        self.setLayout(layout)

    # ================= CHAT BUBBLE =================
    def bubble(self, text, user=True):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(f"""
            padding:10px;
            border-radius:10px;
            background:{'#2563eb' if user else '#333'};
            max-width:400px;
        """)

        row = QHBoxLayout()
        if user:
            row.addStretch()
            row.addWidget(label)
        else:
            row.addWidget(label)
            row.addStretch()

        w = QWidget()
        w.setLayout(row)

        self.chat_area.addWidget(w)

        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    # ================= SEND =================
    def send(self):
        msg = self.input.text()
        if not msg:
            return

        self.bubble(msg, True)

        reply = self.bot.get_reply(msg)
        self.bubble(reply, False)

        self.chats[self.current_chat].append({"role": "user", "msg": msg})
        self.chats[self.current_chat].append({"role": "bot", "msg": reply})

        self.save_data()
        self.input.clear()

    # ================= SWITCH CHAT =================
    def switch_chat(self, item):
        self.current_chat = item.text()
        self.load_chat()

    def new_chat(self):
        name = f"Chat {len(self.chats) + 1}"
        self.chats[name] = []
        self.sidebar.addItem(name)
        self.current_chat = name
        self.load_chat()

    # ================= LOAD CHAT =================
    def load_chat(self):
        for i in reversed(range(self.chat_area.count())):
            self.chat_area.itemAt(i).widget().deleteLater()

        for msg in self.chats[self.current_chat]:
            self.bubble(msg["msg"], msg["role"] == "user")

    # ================= SAVE =================
    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.chats, f, indent=2)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        return {}

    # ================= DASHBOARD =================
    def show_dashboard(self):
        total_chats = len(self.chats)
        total_msgs = sum(len(v) for v in self.chats.values())

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Dashboard 📊")
        msg_box.setText(
            f"Chats: {total_chats}\n"
            f"Messages: {total_msgs}\n"
            f"Current Chat: {self.current_chat}"
        )
        msg_box.exec()


# ================= RUN =================
app = QApplication(sys.argv)
window = ChatApp()
window.show()
sys.exit(app.exec())