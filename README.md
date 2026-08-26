# Submitly

Submitly is an Assignment Submission & Evaluation Platform designed for colleges and academic institutions. It provides a centralized workflow for assignment creation, submission, evaluation, grading, and feedback.

## Technology Stack

*   **Backend:** Python + Django
*   **Frontend:** Django Templates + HTML + CSS + JavaScript
*   **Database:** SQLite (local development)

## Local Setup

Follow these steps to set up the project locally:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Mdsahil01/submitly.git
    cd submitly
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the Virtual Environment:**
    *   **Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
    *   **Windows (CMD):**
        ```cmd
        .venv\Scripts\activate.bat
        ```
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

## Running the Development Server

To start the local development server:

```bash
python manage.py runserver
```

Once started, the application will be accessible at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
