# AESChat

## Run the server  
python -m app.server
## Run client in another terminal
python -m app.client# AESChat


## Process to push changes to the repo, and prepare it for incorporation into develop. 
  1) Make sure you are on your branch.
     git checkout your-branch-name
  2) Check what has changed
     get status
  3) Stage your changes
    git add .
  4) Commit with a short message
     git commit -m "Details of commit"
  
     --The commit is necessary here, because we'll be switching to develop in a minute. Unstaged changes need to be saved.
  5) Pull the latest develop into your branch. !!! Do this before trying to push.
     get checkout develop
     git pull origin develop
     git checkout your-branch-name
     git merge develop
  
     If this creates conflicts, fix them. Then:
     git add .
     git commit
  
  6) Push branch to GitHub
     git push -u origin your-branch-name
  7) Open a pull request.
     Go to the repo on GitHub.
     You'll see a yellow box talking about opening a pull request for the branch. Click it.
     Set the base branch = develop and compare branch = your-branch-name.
     Add a description of what you did.
     Submit.
  
  8) Once it's been reviewed, it will get merged into develop.
  
  *** Main should not be merged into directly. 
