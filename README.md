

---

<div align="center">
    
  # GITHUB USER-ACTIVITY CLI

</div>
  
---

## Overview

Github user-activity CLI is a command line tool to fetch the recent activity of a GitHub user and display it in the terminal. With this tool, you can fetch the user’s recent activity using the GitHub API, and display it in the terminal.
## Features

- **Activity Filter**: Github activities can be filtered using event types [Visit GitHub Events Documentation](https://github.comhttps://docs.github.com/en/rest/using-the-rest-api/github-event-types).
- **Activity Cache**: Activities are cached using TTLCache to improve performance.
- **Activity Sorting**: Activities are sorted to provide readability for users.

###  Installation
  Ensure you have **Python** Installed
  
  Clone the repository:
  

   ```bash
   git clone https://github.com/Omarko65/github-user-activity
   cd github-user-activity
   ```


   Create Virtual Environment:
   ```bash
   python -m venv myenv
   source myenv/bin/activate
  ```

  Install libraries:
  ```bash
  pip install -r requirements.txt
  ```

##  Usage

- **Start by running the app**:

  ```bash
  python main.py
  # Output: Welcome to Github User Activity Tracker!!!
  #         Type 'exit' to end session
  ```

- **Fetch activity of a user**:

  ```bash
  github-activity omarko65 
  # Output: list activities of user
  ```


- **Fetach all activity**:

  ```bash
  github-activity omarko65 ListAll
  # Ouput: All activities of user over the last 90days
  ```

- **Refresh Cache**:

```bash
 github-activity omarko65 Refresh
 # Output: Activities refreshed successfully
 ```

- **Fetch activity of a user based on event**:

  ```bash
  github-activity omarko65 [WatchEvent, CreateEvent, DeleteEvent, PullRequestEvent, ...]
  # Output: List of activities based on selected event
  ```

- **Exiting**:
  ```bash
  github-activity exit
  # Output: Goodbye!!!
  ```


## CC
https://roadmap.sh/projects/github-user-activity
