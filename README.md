# Calendo

Welcome to Calendo! This is a friendly chatbot that helps you book appointments with a tailor. It's designed to be simple and easy to use, just like talking to a real assistant.

## What It Can Do 

- **Chat to Book:** Ask for available appointment times and book them directly through the chat.
- **See Open Slots:** The app shows you a list of open slots for today and tomorrow, so you know what's available at a glance.
- **Google Calendar Integration:** When you book an appointment, it's automatically added to a Google Calendar.

## How It's Built 

This project has two main parts that work together:

- **Frontend (What you see):** A simple and clean chat interface built with **Streamlit**. This is where you'll talk to the bot.
- **Backend (The brains):** A smart API built with **FastAPI**. This part contains the AI agent, which is powered by **Google Gemini** and **LangChain**. It understands your messages and connects to Google Calendar to manage bookings.

## Getting Started

Follow these steps to get Calendo running on your own computer.

### 1. Prerequisites

Before you start, make sure you have the following:

- **Python:** You'll need Python installed on your system.
- **Google Cloud Project:**
  - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
  - Enable the **Google Calendar API** for your project.
  - Create an **OAuth 2.0 Client ID** and download the `credentials.json` file.
  - Get a **Google API Key** to use the AI model.

### 2. Set Up Your Project

1.  **Place Credentials:**
    - Put your downloaded `credentials.json` file in the main `Calendo` folder.
2.  **Create `.env` file:**
    - In the `backend` folder, create a new file named `.env`.
    - Add your Google API key to this file like this:
      ```
      GOOGLE_API_KEY="YOUR_API_KEY_HERE"
      ```

### 3. Install and Run the Backend

Open a terminal and navigate to the `backend` folder:

```bash
# Go into the backend directory
cd backend

# Install the necessary Python packages
pip install -r req.txt

# Start the backend server
uvicorn app.main:app --reload
```

The backend will now be running at `http://127.0.0.1:8000`.

### 4. Install and Run the Frontend

Open a **new** terminal and navigate to the `frontend` folder:

```bash
# Go into the frontend directory
cd frontend

# Install the necessary Python packages
pip install -r req.txt

# Run the Streamlit app
streamlit run app.py
```

Your web browser should open with the Calendo chat interface, ready for you to use!

## How to Use It

Once everything is running, you can start chatting with the bot. Try asking things like:

- "Are there any slots available tomorrow?"
- "Book me an appointment for tomorrow at 3pm for a suit fitting."
- "What times are free on July 5th, 2025?"

The bot will help you find a time and confirm your booking. Enjoy!

## Licence
ISC

## Author
Sudhanshu Shukla
