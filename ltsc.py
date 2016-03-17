#!/usr/bin/env python

# Takes two arguments: 
# - path to the submodule
# - commit hash

import sys
import os
import subprocess

def runCmdAndCollectOutputAsStringList(command, workingDir):
    ret = []
    p = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=workingDir)
    for line in p.stdout:
        ret.append(line[:-1])
    return ret


def findTagsForSubmoduleCommit(submodPath, branchToSearchIn, commithash):
    tags = runCmdAndCollectOutputAsStringList(["git", "rev-list", branchToSearchIn, "^" + commithash + "~"], submodPath)
    #print tags
    # ls-tree output looks like this: 160000 commit 30ef129b26090a5bebd34a33752548cea23696d9	Software/statmuxUrcLib
    distanceFromHeadContainingCommit = -1

    # Find all commits of the superproject that reference one of the tags collected above
    i = 0
    while True:
        submodCommit = runCmdAndCollectOutputAsStringList(["git", "ls-tree", "%s~%d" % (branchToSearchIn, i), submodPath], None)

        try:
            if submodCommit[0].split(" ")[2].split("\t")[0] in tags:
                distanceFromHeadContainingCommit = i
        except:
            # Likely the submodule was not present this far in history
            break
        i+=1

    print "Oldest superproject commit containing the submodule commit: %s~%s" % (branchToSearchIn, distanceFromHeadContainingCommit)
    # For all of these commits, collect the user-defined build tags
    uniqueTags = set()
    if distanceFromHeadContainingCommit != -1:
        uniqueTags = set(runCmdAndCollectOutputAsStringList(["git", "tag", "--contains", "%s~%d" % (branchToSearchIn, distanceFromHeadContainingCommit)], None))
    sortedTags = [x for x in uniqueTags]
    sortedTags.sort()
    print "\n".join(sortedTags)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Run as: %s PathToSubmodule BranchToSearchIn CommmitHash" % os.path.basename(sys.argv[0])
        sys.exit(1)

    findTagsForSubmoduleCommit(sys.argv[1], sys.argv[2], sys.argv[3])
