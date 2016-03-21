#!/usr/bin/env python
#
## Licensed to the .NET Foundation under one or more agreements.
## The .NET Foundation licenses this file to you under the MIT license.
## See the LICENSE file in the project root for more information.
#
##
# Title               :exclusion.py
#
# Script to create a new list file from the old list file by refelcting
# exclusion project file (issues.target)
#
################################################################################

import os
import os.path
import sys
import re

###############################################################################
# Main
################################################################################

if __name__ == "__main__":
  print "Starting exclusion"
  print "- - - - - - - - - - - - - - - - - - - - - - - - - - - -"
  print

  if len(sys.argv) == 3:
    # Update test file in place
    issuesFile = sys.argv[1]
    oldTestFile = sys.argv[2]
    newTestFile = oldTestFile
  elif len(sys.argv) == 4:
    issuesFile = sys.argv[1]
    oldTestFile = sys.argv[2]
    newTestFile = sys.argv[3]
  else:
    print "Ex usage: python exclusion.py <issues profile file> <old lst file> {<new lst file>}"
    exit(1)

  with open(issuesFile) as issuesFileHandle:
    issues = issuesFileHandle.readlines()

  with open(oldTestFile) as oldTestsHandle:
    oldTests = oldTestsHandle.readlines()

  # Build exculsion set from issues
  exclusions = set()
  for i in range(len(issues)):
    matchObj = re.search( r'(XunitTestBinBase\)\\)(.+)(\\)(.+)\"', issues[i])
    if matchObj:
      exclusions.add(matchObj.group(2));

  # Build new test by copying old test except the exclusion
  with open(newTestFile, 'w') as newTestsHandle:
    j = 0
    while(j < len(oldTests)):
      currLine = oldTests[j]
      matchObj = re.search( r'[(.+)]', currLine)
      if matchObj:
        nextLine = oldTests[j+1] 
        matchObj = re.search( r'(RelativePath=)(.+)(\\)(.+)(.exe)', nextLine)
        if matchObj:
          relPath = matchObj.group(2)
          if (relPath in exclusions):
            # Skip to the next item. Currently each test consists of 7 lines.
            j += 7 
            continue

      newTestsHandle.write(currLine)
      j += 1

  print newTestFile + " is successfuly built."

