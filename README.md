# Project

This project is an investor-focused Smart Search Engine. It helps investors find and rank the most suitable startups within a platform that connects investors, startups, brokers, and freelancers.
## About

This project was part of my internship at Prodigal AI. It's a key piece of a new startup platform designed to bring together investors, startups, brokers, and freelancers. My part, the Smart Search Engine for investors, is a helpful tool that:

- Shows investors a ranked list of startups that are a great fit for them.
- Uses a special "affinity score" to match what investors are looking for with what startups offer.
- Employs semantic search and vector embedding to understand the meaning behind search terms and startup descriptions, not just keywords.
- Includes a "profitability score" to highlight startups that look financially promising.
- Gives each startup an overall relevance score out of 100, making it easier for investors to make smart decisions.
- Use a simple and modern UI with React and TailwindCSS
<br>
Currently, only local-host is supported. Working on deploying it on custom server without losing accuracy.

> You’ll need Chrome browser to get the best experience.

<br>

Here’s a preview of the webApp:  
![Dashboard](frontend/src/assets/searchPage.png)
<br>

## Tech Stack

### Frontend
- Next.js
- TailwindCSS

### Backend 
- FastAPI
- Uvicorn
- Python
- PyMongo

### Database
- MongoDB

### Model
- LangChain
- LangChain-Google-GenAi
- LangChain-Community

  
## Pre-requisites
From https://aistudio.google.com/apikey
Initialize a **.env file** in your backend folder with GOOGLE_API_KEY as:

```bash
GOOGLE_API_KEY=AfcX2******
```

## Backend Setup
1. Create a virtual environment:
   
   ```bash
   python -m venv venv # in /backend
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
2. Install required packages:
   
   ```bash
    pip install -r requirements.txt
   ```

## Installation

```bash
npm install # in /frontend
```

## Local Development
1. To run the backend:
    ```bash
    uvicorn main:app --reload
    ```
2. To run the frontend:

    ```bash
    npm run dev
    ```

### Notes
- You need to configure .env with your Google api key.
- For testing, use Chrome browser for better integration with your frontend.
