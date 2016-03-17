# git-utilities
Collection of useful git helper scripts

## List tags containing submodule commit: ltsc.py

At work we make use a lot of submodules. Although the superproject, which 
refers to/contains the submodules, contains tags that allow us to easily
identify which of its commits are part of what tag, the same is not possible
with commits of the submodules (at least, I haven't found a way of doing it).

The script ``ltsc.py`` solves that problem. Run the following command from the
top directory of the checked out superproject:
```shell
ltsc.py <Path to submodule> <Branch to start searching backwards from> <commit SHA-1>
```

Let's take an example. Assume we have the following folder structure:
```
SuperProject/
  Src/
  Submodules/
    Submodule1/
```

If we run following command in the folder ```SuperProject```, it would be 
accomplishing the requested behavior:
```shell
ltsc.py Submodules/Submodule1 MyBranch 59fc166d1dfa2d0f87b02de0c32e3658266a81ab
```

It would search, starting from the head of ```MyBranch``` if it can find any
tags that would contain the referenced submodule commit (or any of it 
descendants).

The reason you actually need to specify a branch name is because I have not found
an efficient way of searching through all branches of the project. I also have
not yet found a way to get a list of all descendants of a commit, across all
branches, something that would be helpful to get cleaner implementation of the
script. 

Be that as it may, it is working and it was hacked together rather
quickly. Just remember to manually run the script for multiple branches if you
want to determine if the submodule commit is part of a number of tags across
different releases/branches.

Enjoy!