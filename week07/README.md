# Week 7 - Git & Team work

* `git log` - <https://git-scm.com/docs/git-log>
  * `git --no-pager log --pretty=format:"%H"` - <https://git-scm.com/docs/pretty-formats>
* `git show` - <https://git-scm.com/docs/git-show>
* `git rebase` - <https://git-scm.com/docs/git-rebase>
  * `git rebase -i <hash>^`
  * `git rebase -i --root`
  * `git rebsae -i --keep-empty`
* `git cherry-pick` - <https://git-scm.com/docs/git-cherry-pick>

Take latest master without merging:

```
git checkout master
git pull origin master
git checkout <feature-branch>
git rebase master
git push --force-with-lease origin <feature-branch>
```

Do an interactive rebase for the last 2 commits:

```
git rebase -i HEAD~2
git push --force-with-lease origin <feature-branch>
```

Someone rebased master & force pushed into the remote:

```
git checkout somewhere
git branch -D master
git fetch origin
git checkout master
```
