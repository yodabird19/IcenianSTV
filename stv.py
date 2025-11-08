import numpy as np

# Takes in a list, where each index is a ranking, and each value is a candidate
# (ex. index 4 has value 8 -> voter has candidate #8 in 5th rank)
# Validates that it is of the correct form
# A value of 0 corresponds to a blank ranking
# (These can only be at the bottom of the ballot)
# A value of -1 corresponds to an eliminated candidate
# NOTE: This function will error if a ballot with -1 is put in
# Also takes in the number of candidates running
# (so if there are 26 candidates, input 26 for the second argument)
def validateRankingList(l, candidateCount):
    presence = np.zeros(candidateCount)
    zero = False
    if len(l) != candidateCount:
        return (False, "Ballot has incorrect length " + str(len(l)) + " for " + str(candidateCount) + " candidates")
    for c in l:
        if c > candidateCount or c < 0:
            return (False, "Ballot has invalid candidate number " + str(c))
        if c != 0:
            presence[c-1] += 1
            if presence[c-1] > 1:
                return (False, "Ballot has more than one ranking for candidate number " + str(c))
        if c == 0:
            zero = True
        if zero and c != 0:
            return (False, "Ballot has non-trailing blank rankings")
    return (True, "")

class Ballot:
    def __init__(self, name, rankingList, votingPower, candidateCount):
        valid = validateRankingList(rankingList, candidateCount)
        if (valid[0]):
            self.name = name
            self.rankingList = rankingList
            self.votingPower = votingPower
        else:
            print(name + " is invalid: " + valid[1])

    # num = 1 for top choice
    # num = 2 for second top choice
    # etc
    def getRankedChoice(self, num):
        for c in self.rankingList:
            if c != -1:
                if num == 1:
                    return c
                else:
                    num -= 1
        return 0

    def eliminate(self,candidateNumber):
        for i in range(len(self.rankingList)):
            if self.rankingList[i] == candidateNumber:
               self.rankingList[i] = -1

    def isExhausted(self):
        for c in self.rankingList:
            if c != -1 and c != 0:
                return False
        return True

# Assesses the number of votes (taking weighting ito account) in favor
# of the candidate
# For tiebreaking purposes, 2nd-choice votes are included x1/1000, and
# 3rd-choice as x1/1000000 (Subsection 5)
def votesInFavor(ballots, candidateNumber):
    count = 0
    counted = []
    for b in ballots:
        if b.getRankedChoice(1) == candidateNumber:
            count += b.votingPower*1
            counted.append(b)
        if b.getRankedChoice(2) == candidateNumber:
            count += b.votingPower*1/1000
            counted.append(b)
        if b.getRankedChoice(3) == candidateNumber:
            count += b.votingPower*1/1000000
            counted.append(b)
    return (count, counted)

# Gets either the top-ranked or lowest-ranked candidate
# mode  1: top ranked
# mode -1: lowest ranked
def extremeCandidate(ballots, mode):
    candidates = np.zeros(len(ballots[0].rankingList))
    for i in range(len(candidates)):
        candidates[i] = votesInFavor(ballots, i+1)[0]
    toReturn = 1
    for i in range(len(candidates)):
        if (mode*candidates[i] > mode*candidates[toReturn-1] and candidates[i] != 0):
            toReturn = i+1
    return toReturn

# Eliminates a candidate from a list of ballots
def eliminateCandidate(ballots, candidateNumber):
    for b in ballots:
        b.eliminate(candidateNumber)

#
def STV(ballots, k):
    winners = []
    print("STV with",str(k),"winners,",str(len(ballots[0].rankingList)),"candidates,",str(len(ballots)),"ballots")
    totalVote = len(ballots)
    # Subsection 2
    while (len(winners) < k):
        # Subsection 3
        topCandidate = extremeCandidate(ballots,1)
        (topCandidateVotes, votesForTopCandidate) = votesInFavor(ballots, topCandidate)
        if np.floor(topCandidateVotes) >= np.ceil(totalVote/(k+1)):
            # Paragraph 3(a)
            winners.append(topCandidate)
            # Paragraph 3(b)
            eliminateCandidate(ballots, topCandidate)
            print ("win",str(topCandidate))
            for b in votesForTopCandidate:
                b.votingPower *= (k+1)*np.floor(topCandidateVotes)/totalVote
            # Paragraph 3(c)
        # Subsection 4
        else:
            # Paragraph 4(a)
            bottomCandidate = extremeCandidate(ballots, -1)
            eliminateCandidate(ballots, bottomCandidate)
            print("elim",str(bottomCandidate))
        # Subsection 6
        for b in ballots:
            if (b.isExhausted()):
                totalVote -= b.votingPower
                b.votingPower = 0
    return winners


b1 = Ballot("Alice", [3, 1, 2, 4], 1, 4)
b2 = Ballot("Bob", [4, 2, 3, 0], 1, 4)
b3 = Ballot("Claire", [1, 0, 0, 0], 1, 4)
b4 = Ballot("David", [3, 4, 1, 2], 1, 4)
b5 = Ballot("Eliza", [1, 4, 2, 0], 1, 4)
bs = [b1,b2,b3,b4,b5]

print(STV(bs,1))