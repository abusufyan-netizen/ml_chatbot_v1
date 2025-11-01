🧠 Digit Recognition AI

A Smart AI System for Handwritten Digit Identification

    


---

📘 Overview

Digit Recognition AI is a modern deep-learning web app built using Streamlit and TensorFlow/Keras.
It allows users to draw digits (0-9), predicts them using a trained neural network, and lets users correct wrong predictions, retrain automatically, and store data on Google Drive for persistent learning.


---

⚙️ Features

✅ Modern Interface (Dark/Light auto theme)
✅ Interactive Canvas to draw digits
✅ Self-Learning Model (Retrains after corrections)
✅ Prediction History Dashboard with green/red indicators
✅ Manual Data Upload & Training Panel
✅ Google Drive Sync for all backups (model, logs, dataset)
✅ Accuracy Monitoring Page


---

🧩 Project Structure

Digit_Recognition_AI/
│
├── app.py                  # Streamlit main application
├── train_model.py          # Model training and evaluation
├── utils/
│   ├── drive_backup.py     # Google Drive API integration
│   ├── helpers.py          # Data and UI utilities
│
├── model/
│   └── digit_model.keras   # Pretrained model (auto-updated)
│
├── data/
│   ├── dataset/            # Custom user uploads
│   └── logs/               # Training and correction logs
│
├── README.md
├── requirements.txt
├── setup.md
├── LICENSE
└── .gitignore


---

🚀 Quick Setup Guide

🧮 1. Clone Repository

git clone https://github.com/abusufyan-netizen/Digit_Recognition_AI.git
cd Digit_Recognition_AI

🧠 2. Create Virtual Environment

python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

📦 3. Install Dependencies

pip install -r requirements.txt

☁️ 4. Add Google Drive Credentials

Create a folder .streamlit/secrets.toml and paste:

[gdrive]
type = "service_account"
project_id = "digit-recognition-ai"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = "YOUR_PRIVATE_KEY"
client_email = "YOUR_CLIENT_EMAIL"
client_id = "YOUR_CLIENT_ID"

▶️ 5. Run Streamlit App

streamlit run app.py


---

🧠 Training and Improvement

The model auto-trains every time 5 new corrections are logged.

You can also manually trigger retraining from the Admin / Training page.

All updated models are backed up automatically to Google Drive.



---

🗂️ Backup Configuration

By default:

Local Backup: data/logs/ and model/

Cloud Backup: Google Drive folder — Digit_Recognition_AI_Backup


You can modify this in config.yaml.


---

🧪 Tech Stack

Component	Technology

Frontend	Streamlit
Backend	Python (Flask + Streamlit)
ML Model	Keras / TensorFlow
Storage	Google Drive API
Visualization	Matplotlib, Seaborn



---

📊 Accuracy

Metric	Description

Baseline Accuracy	98.4% (Trained on MNIST)
Improved Accuracy	Increases dynamically with user feedback
Loss Function	Categorical Crossentropy
Optimizer	Adam



---

👨‍💻 Author

Abu Sufyan — Student
GitHub: @abusufyan-netizen
Organization: Abu Zar


---

📜 License

This project is licensed under the MIT License.
Feel free to use and modify with credit.


---

🌟 Demo (Optional)

Once deployed, the app can be accessed via:
🔗 https://digit-recognition-ai.streamlit.app (example link)


---

❤️ Contributions

Pull requests are welcome!
If you find a bug or want to enhance features, open an issue with proper tagging.


---

🦯 Future Enhancements

🔹 Integration with Firebase for real-time sync

🔹 Adding multilingual support

🔹 Adding voice recognition for predictions

🔹 Auto-model versioning dashboard



---

Crafted with precision and care by Abu Sufyan under the Abu Zar Organization.
