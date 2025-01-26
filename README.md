# Events Project

This repository contains the API endpoints for the **Events** application, built with FastAPI. The project provides authentication endpoints and other event-related functionalities.

## Project Setup

### Prerequisites

Before setting up the project, ensure that you have the following tools installed:

- **Python 3.7+** (Ensure you have a supported version of Python installed).
- **pip** (Python package manager).
- **Git** (to clone the repository).

### Setup Instructions

Follow these steps to set up and run the Events API:

1. **Clone the Repository**

   Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/KAVYAJAIN410/RoboViticsProject.git
   cd RoboViticsProject

2. **Create a Virtual Environment**

3. **Install the Requirements**

Install the required dependencies listed in requirements.txt:
pip install -r requirements.txt

4. **Add Environment Variables**

Create a .env file in the root of the project and include the following environment variables:

GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_LINK
SECRET_KEY
DATABASE_URL

5.**Running the Application**
Once the dependencies are installed and the environment variables are set up, you can run the FastAPI application using Uvicorn.

Start the Server:
uvicorn app.main:app --reload --host localhost --port 8000

6. **Authentication**
To authenticate users, navigate to the /login endpoint


