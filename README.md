# Search Engine

This project is an investor-side Smart Search Engine. It helps investors to find the most favourable and profitable startups according their affinity alignment.<br>
As the engine ranks the most suitable startups within a platform that connects investors, startups, brokers, and freelancers.
## About

This project was part of my internship at Prodigal AI. It's a key piece of a new startup platform designed to bring together investors, startups, brokers, and freelancers. My part, the Smart Search Engine for investors, is a helpful tool that:

- Shows investors a ranked sorted list of startups that are a great fit for them.
- Uses a special "affinity score" to match what investors are looking for with what startups offer.
- Employs semantic search and vector embedding to understand the meaning behind search terms and startup descriptions, not just keywords.
- Includes a "profitability score" to highlight startups that look financially promising.
- Gives each startup an overall relevance score out of 100, making it easier for investors to make smart decisions.
<br>
Currently, only local-host is supported. Working on deploying it on custom server without losing accuracy.

> You’ll need Chrome browser to get the best experience.

<br>

Here’s a preview of the webApp:  
![Dashboard](frontend/public/searchPage.png)
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

  
# Project Setup

### Pre-requisites

- Obtain a Google API key from Google AI Studio.
- Create a .env file in the backend folder (details provided below).

### Setting up Redis
These instructions are for setting up Redis on Windows using WSL (Windows Subsystem for Linux). Ensure WSL is installed.

1. Open a command prompt as an administrator.
2. Install WSL if not already installed:

```bash
wsl --install
```

3. Launch WSL:
```bash
wsl
```

4. Add the Redis repository:
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

```

5. Update package lists and install Redis:
```bash
sudo apt-get update
sudo apt-get install redis
```

6. Start the Redis server:
```bash
sudo service redis-server start
```

7. Edit the Redis configuration file:
  - Open the file with:
  ```bash
  sudo nano /etc/redis/redis.conf
  ```
  - A vim environment will show a config file. <br>Make these changes:
  ```bash
  Change bind 127.0.0.1 ::1 -> bind 0.0.0.0
  Change protected-mode yes -> protected-mode no
  Comment out 'requirepass foobared' by removing '#' from the beginning
  # requirepass foobared -> requirepass your_password
  Save with Ctrl + O, press Enter, and exit with Ctrl + X
  ```

8. Restart the Redis server:
```bash
sudo service redis-server restart
```

9. Verify Redis is running:
```bash
redis-cli -a your_password
```


### Backend Setup

1. Open a command prompt in the project’s root directory.
2. Navigate to the backend directory:
```bash
cd backend
```

3. Create a virtual environment:
```bash
python -m venv venv
```

4. Activate the virtual environment:
```bash
On Windows: venv\Scripts\activate

On macOS/Linux: source venv/bin/activate
```



5. Install required packages:
```bash
pip install -r requirements.txt
```

6. Run the backend server:
```bash
uvicorn main:app --reload
```


### Frontend Setup

1. Open another command prompt in the project’s root directory.
2. Navigate to the frontend directory:cd frontend


3. Install dependencies:
```bash
npm install
```

4. Run the development server:
```bash
npm run dev
```


### .env File Structure
Place this in the backend folder:
```bash
MONGO_URI=mongodb+srv://yogeshxiix:hr16p1076@cluster0.a9ori37.mongodb.net/data?retryWrites=true&w=majority&appName=Cluster0
GOOGLE_API_KEY=AIzaSyD***********
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=your_password
```

- Replace your_password with your Redis password.
- Ensure the GOOGLE_API_KEY matches your actual key.

### Notes

> For testing, use the Chrome browser for better frontend integration.
