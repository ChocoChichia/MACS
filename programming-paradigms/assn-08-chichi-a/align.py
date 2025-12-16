#!/usr/bin/env python

import random # for seed, random
import sys    # for stdout



################################### TEST PART ##################################
################################################################################

# Tests align strands and scores
# Parameters types:
#    score          =  int   example: -6
#    plusScores     = string example: "  1   1  1"
#    minusScores    = string example: "22 111 11 "
#    strandAligned1 = string example: "  CAAGTCGC"
#    strandAligned2 = string example: "ATCCCATTAC"
#
#   Note: all strings must have same length
def test(score, plusScores, minusScores, strandAligned1, strandAligned2):
    print("\n>>>>>>START TEST<<<<<<")

    if testStrands(score, plusScores, minusScores, strandAligned1, strandAligned2):
        sys.stdout.write(">>>>>>>Test SUCCESS:")
        sys.stdout.write("\n\t\t" + "Score: "+str(score))
        sys.stdout.write("\n\t\t+ " + plusScores)
        sys.stdout.write("\n\t\t  " + strandAligned1)
        sys.stdout.write("\n\t\t  " + strandAligned2)
        sys.stdout.write("\n\t\t- " + minusScores)
        sys.stdout.write("\n\n")
    else:
        sys.stdout.write("\t>>>>!!!Test FAILED\n\n")


# converts character score to int
def testScoreToInt(score):
    if score == ' ':
        return 0
    return int(score)


# computes sum of scores
def testSumScore(scores):
    result = 0
    for ch in scores:
        result += testScoreToInt(ch)
    return result


# test each characters and scores
def testValidateEach(ch1, ch2, plusScore, minusScore):
    if ch1 == ' ' or ch2 == ' ':
        return plusScore == 0 and minusScore == 2
    if ch1 == ch2:
        return plusScore == 1 and minusScore == 0
    return plusScore == 0 and minusScore == 1


# test and validates strands
def testStrands(score, plusScores, minusScores, strandAligned1, strandAligned2):
    if len(plusScores) != len(minusScores) or len(minusScores) != len(strandAligned1) or len(strandAligned1) != len(
            strandAligned2):
        sys.stdout.write("Length mismatch! \n")
        return False

    if len(plusScores) == 0:
        sys.stdout.write("Length is Zero! \n")
        return False

    if testSumScore(plusScores) - testSumScore(minusScores) != score:
        sys.stdout.write("Score mismatch to score strings! TEST FAILED!\n")
        return False
    for i in range(len(plusScores)):
        if not testValidateEach(strandAligned1[i], strandAligned2[i], testScoreToInt(plusScores[i]),
                                testScoreToInt(minusScores[i])):
            sys.stdout.write("Invalid scores for position " + str(i) + ":\n")
            sys.stdout.write("\t char1: " + strandAligned1[i] + " char2: " +
                             strandAligned2[i] + " +" + str(testScoreToInt(plusScores[i])) + " -" +
                             str(testScoreToInt(minusScores[i])) + "\n")
            return False

    return True

######################## END OF TEST PART ######################################
################################################################################


def findOptimalAlignment(strand1, strand2, memo=None):
    if memo is None:
        memo = {}

    if (strand1, strand2) in memo:
        return memo[(strand1, strand2)]

    if len(strand1) == 0:
        result = (-2 * len(strand2), " " * len(strand2), strand2)
        memo[(strand1, strand2)] = result
        return result
    if len(strand2) == 0:
        result = (-2 * len(strand1), strand1, " " * len(strand1))
        memo[(strand1, strand2)] = result
        return result

    score_with, align1_with, align2_with = findOptimalAlignment(strand1[1:], strand2[1:], memo)
    if strand1[0] == strand2[0]:
        score_with += 1
    else:
        score_with -= 1
    align1_with = strand1[0] + align1_with
    align2_with = strand2[0] + align2_with

    score_gap1, align1_gap1, align2_gap1 = findOptimalAlignment(strand1, strand2[1:], memo)
    score_gap1 -= 2
    align1_gap1 = " " + align1_gap1
    align2_gap1 = strand2[0] + align2_gap1

    score_gap2, align1_gap2, align2_gap2 = findOptimalAlignment(strand1[1:], strand2, memo)
    score_gap2 -= 2
    align1_gap2 = strand1[0] + align1_gap2
    align2_gap2 = " " + align2_gap2

    if score_with >= score_gap1 and score_with >= score_gap2:
        best_result = (score_with, align1_with, align2_with)
    elif score_gap1 >= score_with and score_gap1 >= score_gap2:
        best_result = (score_gap1, align1_gap1, align2_gap1)
    else:
        best_result = (score_gap2, align1_gap2, align2_gap2)

    memo[(strand1, strand2)] = best_result
    return best_result


def generateRandomDNAStrand(minlength, maxlength):
    assert minlength > 0, "Minimum length must be positive."
    assert maxlength >= minlength, "Maximum length must be at least as large as the minimum length."
    length = random.randint(minlength, maxlength)
    bases = ['A', 'T', 'G', 'C']
    return ''.join(random.choice(bases) for _ in range(length))


def printAlignment(score, strandAligned1, strandAligned2, out=sys.stdout):
    out.write("Optimal alignment score is {}\n".format(score))
    out.write("Aligned strand 1: {}\n".format(strandAligned1))
    out.write("Aligned strand 2: {}\n".format(strandAligned2))


# Main function for testing and random DNA alignment
def main():
    test(-4,
         "  11 1 1 11 ",
         "12  2 2 1  2",
         "G ATCG GCAT ",
         "CAAT GTGAATC")
    
    while True:
        sys.stdout.write("Generate random DNA strands? (yes/no): ")
        answer = sys.stdin.readline().strip().lower()
        if answer in ["n", "no"]:
            break
        elif answer in ["y", "yes"]:
            strand1 = generateRandomDNAStrand(8, 10000)
            strand2 = generateRandomDNAStrand(8, 10000)
            sys.stdout.write("Aligning these two strands:\n  {}\n  {}\n".format(strand1, strand2))
            score, aligned1, aligned2 = findOptimalAlignment(strand1, strand2)
            printAlignment(score, aligned1, aligned2)
        else:
            sys.stdout.write("Please answer 'yes' or 'no'.\n")




if __name__ == "__main__":
    main()
