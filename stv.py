import numpy as np

# Takes in a list of *strings* corresponding to candidate rankings,
# which may be up to as long as (but not longer than) the number of candidates,
# and a list of all the candidates
# and outputs a numeric ranking list (of the form used by the rest of this program)
# with names corresponding to their candidate numbers given in the candidate references
def ballotFromNames(name, l, candidateReferences):
    rankingList = []
    for candidateName in l:
        num = getCandidateNumber(candidateName,candidateReferences)
        if num > 0:
            rankingList.append(num)
        else:
            print(name + "'s ballot has invalid candidate '" + candidateName + "'.")
            return None
    for i in range(len(l),len(candidateReferences)):
        rankingList.append(0)
    return Ballot(name, rankingList, 1, len(candidateReferences))

# Gets the numeric candidate identifier for a candidate name,
# based on a list of references
# Returns -2 (error code for "invalid candidate") if there is none
def getCandidateNumber(candidateName, candidateReferences):
    for i in range(len(candidateReferences)):
        if candidateReferences[i] == candidateName:
            return i+1
    return -2

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
                    #print(self.name+" top choice of "+str(c)+": "+str(self.rankingList))
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
        if (b.votingPower > 1):
            print (b.name+"'s ballot has voting power "+str(b.votingPower)+"!")
        if b.getRankedChoice(1) == candidateNumber:
            count += b.votingPower*1
            counted.append(b)
        if b.getRankedChoice(2) == candidateNumber:
            count += b.votingPower*1/1000
        if b.getRankedChoice(3) == candidateNumber:
            count += b.votingPower*1/1000000
    #print("Candidate " + str(candidateNumber) + " has "  + str(count) + " votes in favor from " + str(len(counted)) + " ballots.")
    return (count, counted)

# Gets either the top-ranked or lowest-ranked candidate
# mode  1: top ranked
# mode -1: lowest ranked
def extremeCandidate(ballots, mode):
    candidates = np.zeros(len(ballots[0].rankingList))
    for i in range(len(candidates)):
        candidates[i] = votesInFavor(ballots, i+1)[0]
    toReturn = -1/2
    for i in range(len(candidates)):
        if (candidates[i] != 0):
            toReturn = i+1
            break
    if toReturn == -1/2:
        print("TORETURN = 1/2:")
        for b in ballots:
            print(b.name+": " + str(b.rankingList))
    #print(candidates)
    for i in range(len(candidates)):
        if (mode*candidates[i] > mode*candidates[toReturn-1] and candidates[i] != 0):
            toReturn = i+1
    #print("Votes in favor of candidate",toReturn,":",str(candidates[toReturn-1]))
    #print("Votes in favor of candidate",1,":",str(candidates[0+1]))
    return toReturn

# Eliminates a candidate from a list of ballots
def eliminateCandidate(ballots, candidateNumber):
    #print("ELIMINATING CANDIDATE " + str(candidateNumber))
    for b in ballots:
        b.eliminate(candidateNumber)

#
def STV(ballots, k, candidateReferences):
    print("STV with",str(k),"winners,",str(len(ballots[0].rankingList)),"candidates,",str(len(ballots)),"ballots")
    #for b in ballots:
        #print(b.name + ": " + str(b.rankingList))
    winners = []
    totalVote = len(ballots)
    # Subsection 2
    while (len(winners) < k):
        # Subsection 3
        topCandidate = extremeCandidate(ballots,1)
        (topCandidateVotes, votesForTopCandidate) = votesInFavor(ballots, topCandidate)
        if topCandidateVotes >= totalVote/(k+1):
            # Paragraph 3(a)
            winners.append(candidateReferences[topCandidate-1])
            # Paragraph 3(b)
            print ("win",candidateReferences[topCandidate-1])#,topCandidateVotes,str(totalVote/(k+1)))
            eliminateCandidate(ballots, topCandidate)
            #print("quota:",str(np.ceil(totalVote/(k+1))),"from total remaining voting power of",str(totalVote))
            for b in votesForTopCandidate:
                b.votingPower *= (topCandidateVotes-totalVote/(k+1))/topCandidateVotes
            # Paragraph 3(c)
        # Subsection 4
        else:
            # Paragraph 4(a)
            bottomCandidate = extremeCandidate(ballots, -1)
            print("elim",candidateReferences[bottomCandidate-1])#,str(votesInFavor(ballots, bottomCandidate)[0]),str(totalVote/(k+1)))
            eliminateCandidate(ballots, bottomCandidate)
        # Subsection 6
        for b in ballots:
            if b.isExhausted():
                #print(b.name+"'s ballot is exhausted!")
                totalVote -= b.votingPower
                #print("totalVote has been reduced by " + str(b.votingPower) + "! It is now " + str(totalVote))
                b.votingPower = 0
    return winners

cand = ["Wyatt","Xavier","Yvette","Zoe"]
b1 = ballotFromNames("Alice", ["Yvette", "Wyatt", "Xavier", "Zoe"], cand)
b2 = ballotFromNames("Bob", ["Zoe", "Xavier", "Yvette"], cand)
b3 = ballotFromNames("Claire", ["Wyatt"], cand)
b4 = ballotFromNames("David", ["Yvette", "Zoe", "Wyatt", "Xavier"], cand)
b5 = ballotFromNames("Eliza", ["Wyatt", "Zoe", "Xavier"], cand)
bs = [b1,b2,b3,b4,b5]

print(STV(bs,1,cand))

