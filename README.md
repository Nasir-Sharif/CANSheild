# CANShield: Intrusion Detection System for CAN Bus Security

**Prepared by:** Nasir Sharif  
**Date:** July 18, 2025  

A Machine Learning-Based Web Application for Real-Time Intrusion Detection in Automotive CAN Bus Systems.

## 🚗 Overview

CANShield is a web-based system that uses machine learning to detect potential intrusions in vehicle CAN (Controller Area Network) bus logs. It accepts `.csv` log files, analyzes patterns, and identifies potential cyber-attacks like DoS, Fuzzy, and Impersonation.

## 🛠️ Features

- File upload for CAN logs
- Real-time prediction using trained ML models
- Detailed threat classification
- Clean and responsive frontend
- Flask-powered backend with scikit-learn model

## 🖥️ Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask), scikit-learn
- **ML Model**: Logistic Regression / Random Forest / SVM (based on training)
- **Data**: CAN Bus attack datasets (DoS, Fuzzy, Impersonation, Normal)

## 🚀 How to Run

1. Clone the repository:
git clone https://github.com/Nasir-Sharif/CANSheild.git
cd CANSheild


2. Install backend dependencies:
pip install -r requirements.txt


3. Run the backend:
python app.py



4. Open `index.html` in your browser to use the web app.

## 📁 Project Structure

CANShield/
├── backend/
│ ├── app.py
│ ├── model/
│ ├── data/
│ └── ...
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
└── README.md


## 📜 License

MIT License
<img width="878" height="407" alt="image" src="https://github.com/user-attachments/assets/78f53479-1098-447b-baeb-42827d5bd7e7" />
