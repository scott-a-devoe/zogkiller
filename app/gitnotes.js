// pull from the remote master
git checkout master
git pull [origin master]
// branch from the local master
git checkout -b branch_name
  MAKE CHANGES TO AND SAVE LOCAL FILES
// commit the changes to your local branch
git add --all
git commit -m "message"
// merge those changes with local master
git checkout master
git merge branch_name
// push up to the remote master branch
git push origin master