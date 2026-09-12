## Project Overview: Intelligent Search Visualizer

In this assignment, you will implement, configure, and deploy an interactive map-based search visualizer for **either Myanmar or Thailand**. You are required to implement six search algorithms, API data-fetching logic, and the web backend.

The final outcome of this project is a fully functional web application deployed to a public, live URL.

### Learning Objectives

1. **Algorithm Implementation:** Understand classic AI search strategies (BFS, DFS, UCS, IDS, Greedy Best-First Search, and A*).
2. **Algorithm Understanding:** Explain the main concept behind each search strategy and how it determines which node to expand next.
3. **API Integration and Data Fetching:** Interact with external geocoding and routing APIs to construct a real-world spatial road network.
4. **Web Application Development & Deployment:** Build a complete web backend and deploy a functional search visualization application.

---

## Submission Guidelines

To submit your project, please ensure you complete all the required tasks and follow these instructions carefully.

### 1. Preparation Checklist
Before pushing your final submission, verify that:
*   [ ] You have chosen a geographic focus (**Myanmar** or **Thailand**).
*   [ ] You have implemented the four search algorithms in [`uninformed.py`](file:///Volumes/Data/MLAI_Projects/MMDT_AI_SEARCH/uninformed.py) (BFS, DFS, UCS, IDS).
*   [ ] You have implemented the two search algorithms in [`informed.py`](file:///Volumes/Data/MLAI_Projects/MMDT_AI_SEARCH/informed.py) (Greedy Best-First, A*).
*   [ ] You have implemented [`data_fetcher.py`](file:///Volumes/Data/MLAI_Projects/MMDT_AI_SEARCH/data_fetcher.py) and generated [`map_data.json`](file:///Volumes/Data/MLAI_Projects/MMDT_AI_SEARCH/map_data.json) (minimum 20 cities/locations).
*   [ ] You have built the Flask backend in [`app.py`](file:///Volumes/Data/MLAI_Projects/MMDT_AI_SEARCH/app.py) and frontend in [`templates/index.html`](file:///Volumes/Data/MLAI_Projects/MMDT_AI_SEARCH/templates/index.html).
*   [ ] You have completed the AI Student Declaration on [PETRA AI](https://www.petraai.org/student) and saved it as `AI_declaration.png` in the repository root.
*   [ ] You have completed all sections in [`report.md`](file:///Volumes/Data/MLAI_Projects/MMDT_AI_SEARCH/report.md) (with your Name, MMDT ID, Telegram username, live deployment URL, and video presentation link). Do not alter the structure of [`report.md`](file:///Volumes/Data/MLAI_Projects/MMDT_AI_SEARCH/report.md).
*   [ ] You have recorded a 5–7 minute video presentation (.mp4, face visible) demonstrating the application, and uploaded it to YouTube, Google Drive, or Dropbox (with public view access).

### 2. How to Submit
Once everything is ready, commit and push your code to your GitHub repository's `main` or `master` branch:
```bash
git add .
git commit -m "Submit Project 1: AI Search"
git push origin main
```
The automated autograding system will automatically run tests upon pushing to the `main` or `master` branch.

---

## Checking Grades

You can check your project grades both locally and online via GitHub Actions.

### 1. Locally (Before Submitting)
You can run the autograding tests on your local machine.
1. Make sure you have installed all the dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Run `pytest` inside the project root:
   ```bash
   pytest tests/
   ```
3. A scorecard summarizing your earned marks will be outputted directly in the terminal under the section **"AUTOGRADING SCORECARD"**.

### 2. On GitHub (After Submitting)
Every push to the repository triggers the online autograder.
1. Go to the **Actions** tab of your GitHub repository.
2. Select the latest run (e.g., "Autograder Check" or your commit message).
3. Under the run details, scroll to the bottom or open the job logs to view the **Autograding Scorecard** step summary, which details your score out of 70 marks.

### 3. Grading Details & Passing Requirements
*   **Total Score:** 70 marks (40 marks for implementation, 30 marks for report/video presentation).
*   **Passing Score:** **70 marks**.
*   **Deadline:** **September 13, 2026, at 23:59:59**.
*   **Late Submission Policy:** A penalty of **-10 marks per day** will be applied for late submissions.
*   **Commitment Fee:** Any late, missing, or failed project (score < 70%) will carry a **30,000 MMK commitment fee**, calculated and collected at the end of the 10-week challenge.
