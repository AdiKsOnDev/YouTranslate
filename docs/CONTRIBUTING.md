# 📜 Conventions for contributions
This file contains guidelines for creating *commits, PRs, branches, issues, and etc*.

## Index

- [Commits](#➕-commits)
  - [Commit Message Structure](#🗃️-commit-message-structure)
  - [Example Commit](#example-commit)
  - [Commit Types](#📑-commit-types)
  - [Breaking Changes](#❗️-breaking-changes)
- [Branching](#🌳-branching)
  - [Example Branch Name](#📄-example-branch-name)
- [Pull Requests (PRs)](#pull-requests-prs)
  - [PR message structure](#🗃️-pr-message-structure)
  - [Example PR Message](#📄-example-pr-message)

> [!NOTE]  
> **READ BEFORE CONTRIBUTING!**<br>
> If you have any questions on the following information, text me (Adil), I will take you through it.

---

## ➕ Commits
First, let's answer the questions **"When do I commit? And how many files do I commit at once?"**
<br>
The answer is very simple! Commit anytime you are done with ANY task. **For ex:**
<br>
<br>
Let's say you are adding a login page. That's a big task, so you divide it on small ***sub-tasks***. (Make a login box, make a button, connect firebase, and etc.)

Everytime you are done with a subtask, make a commit! 

> [!WARNING] 
> Please, don't stage all the files in one commit. Stage only the files that are relevant to the subtask you finished.<br>
> This is going to be unbelievably helpful down the road.

### 🗃️ Commit message Structure
---
Commits should consist of **three** parts:
```
<type> Message
<blank space>
<body>
```

### Example Commit
---
```
fix: Fixed login button bug

The bug where login button would successfully authenticate the user, but didn't take him to the homepage as needed.
```

### 📑 Commit Types
---
Is recommended to be one of the below items. Only **feat** and **fix** show up in the changelog, in addition to breaking changes (See breaking changes section below).

* **feat**: A new feature
* **fix**: A bug fix
* **docs**: Documentation only changes
* **refactor**: A code change that neither fixes a bug or adds a feature
* **test**: Adding missing tests
* **chore**: Changes to the build process or auxiliary tools and libraries such as documentation
  generation

### ❗️ Breaking Changes
---
Put any breaking changes with migration instructions in the commit body.

If there is a breaking change, put "BREAKING CHANGE:" in your ***commit body***, and it will show up in the **changelog**.

## 🌳 Branching
Try to have 1 branch per 1 issue. When you take up an issue (task) to work on, assign it to yourself on the issue's page, and comment: "@AdiKsOnDev, I am working on this issue."


The name of the branch has to be as follows:
```
<issue-number>-<branch-name>
```

### 📄 Example branch name
```
9-migrating-to-reactJS
```

## Pull Requests (PRs)
Make a pull request when you are completely done with your issue. Assign me as a reviewer & assignee, as the milestone choose the according milestone.

### 🗃️ PR message structure
---
```
<heading>
<body>

TODO: (If something needs to be done further)

Closes Issue #number-of-the-issue
```

### 📄 Example PR message
---

```
Login Page finished

Connected firebase, cookies are stored in the browser and are called "user_id", "user_login"

TODO: Add login page to the Router in App.js

Closes Issue #5
```
