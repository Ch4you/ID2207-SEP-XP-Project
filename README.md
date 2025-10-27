# ID2207 - SEP Internal System (XP Project)

This repository contains the final project for the ID2207 Modern Methods in Software Engineering course. The objective is to build an internal management system for the "Swedish Events Planners (SEP)" company.

The project is developed following Extreme Programming (XP) practices, including User Stories, Test-Driven Development (TDD), and Pair Programming (simulated via Pull Request reviews).

## Core Functionality

The system focuses on implementing the following four core business workflows:

1.  Event Request Workflow (Customer Service $\rightarrow$ SCS $\rightarrow$ FM $\rightarrow$ AM $\rightarrow$ SCS)
2.  Task Distribution Workflow (SM/PM $\rightarrow$ Subteam $\rightarrow$ SM/PM)
3.  Staff Recruitment Management (SM/PM $\rightarrow$ HR $\rightarrow$ SM/PM)
4.  Financial Request Management (SM/PM $\rightarrow$ FM $\rightarrow$ SM/PM)

## Team Members

* [Changhe You]
* [Zekai Lin]
* [Shuchang Hu]

## Tech Stack

* **Language:** Python 3.10+
* **Framework:** Flask
* **Templating:** Jinja2
* **Testing:** Pytest

---

## 🚀 Getting Started

All team members **must** follow these steps to ensure a consistent development environment.

### 1. Clone the Repository
```bash
git clone [https://github.com/Ch4you/ID2207-SEP-XP-Project.git]
cd ID2207-SEP-XP-Project
```
### 2. Create and Activate Virtual Environment

Now, from inside the ID2207-SEP-XP-Project directory, create the virtual environment:

### On macOS / Linux:

```bash

python3 -m venv venv
source venv/bin/activate
```

### On Windows (CMD or Git Bash):

```Bash

python -m venv venv
`.\venv\Scripts\activate
```

### 3. Install All Dependencies
While the virtual environment is active, install all required libraries from the requirements.txt file:

```Bash

pip install -r requirements.txt
```
### 4. Setup Complete!
The project is now fully set up. You can run the server for the first time:

```Bash

flask run --debug
```

### Development
How to Run the Local Server
This command starts the server in debug mode, which will automatically reload when you save code changes.

```Bash

flask run --debug
The application will be available at: http://127.0.0.1:5000
```

## 🤝 Git Workflow

We follow a strict Pull Request (PR) workflow. **No one may push directly to the `main` branch.**

1.  **Start New Work:** Always get the latest `main` branch before starting.
    ```bash
    git checkout main
    git pull origin main
    ```

2.  **Create a Branch:** Create a new, descriptive branch for your User Story.
    ```bash
    # Example:
    git checkout -b feature/login-story
    ```

3.  **Develop:** Write your tests (TDD) and code. Commit your changes locally.
    ```bash
    # ...write tests and code...
    pytest
    git add .
    git commit -m "feat: add login page and route"
    ```

4.  **Push:** Push your new branch to GitHub.
    ```bash
    git push origin feature/login-story
    ```

5.  **Create Pull Request:** Go to the GitHub repository and open a Pull Request to merge your branch into `main`.

6.  **Review:** Tag your teammates to review your PR. At least **one approval** is required. Discuss changes in the PR's comment thread.

7.  **Merge:** After the PR is approved and all TDD checks (GitHub Actions) are green, the author or reviewer can merge the PR (preferably using **"Squash and Merge"**).

8.  **Clean up:** After merging, you can delete your feature branch.