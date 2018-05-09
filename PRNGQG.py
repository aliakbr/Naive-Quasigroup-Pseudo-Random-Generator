"""
    Quasigroup Class
"""
import numpy as np

class PRNGQG():
    def __init__(self, N=256):
        self.N = N # Order of the number range
        self.QG = [[0 for x in range(self.N)] for y in range(self.N)]
        self.idx = 0

    def ShuffleRow(self, i, j):
        """
            Function to shuffle row i and j in QG
        """
        tmp = []
        tmp = self.QG[i]
        self.QG[i] = self.QG[j]
        self.QG[j] = tmp

    def ShuffleColumn(self, i, j):
        """
            Function to shuffle column i and j in QG
        """
        i_col = [self.QG[x][i] for x in range(self.N)]
        j_col = [self.QG[x][j] for x in range(self.N)]
        for x in range(self.N):
            for y in range(self.N):
                if y == j:
                    self.QG[x][y] = i_col[x]
                elif y == i:
                    self.QG[x][y] = j_col[x]

    def Initialize_Matrix(self):
        """
            Function to generate quasigroup matrix in 256 order.
            Rule to fill the matrix :
                v = c + r
            Default N = 256
        """
        for i in range(self.N):
            for j in range(self.N):
                self.QG[i][j] = (i + j)%self.N
        self.idx = 0

    def Generate(self, s1, s2):
        """
            Generate random number using 2 seeds number
            that chose randomly as input.
            limit parameter used to limit the iteration process.
        """
        self.Initialize_Matrix()
        rnd = self.QG[s1][s2]
        s1 = s2
        s2 = rnd
        self.ShuffleColumn(self.idx, s1)
        self.ShuffleRow(self.idx, s2)
        rnd = self.QG[s1][s2]
        self.idx = (self.idx+1)%self.N
        return rnd

    def Save_Matrix(self, filename):
        """
            Function to save the current matrix state in filename
        """
        with open(filename, "w") as f:
            for i in range(self.N):
                for j in range(N):
                    if (j != N-1):
                        f.write("{} ".format(self.QG[i][j]))
                    else:
                        f.write("{}".format(self.QG[i][j]))
                f.write("\n")

    def shuffle(self, seq, key_seed):
        """
            Shuffle a sequence using provided seed using Fisher-Yates shuffle
        """
        i = len(seq)-1
        randomizer = PRNGQG(len(seq)-1)
        while (i > 1):
            randomizer1 = PRNGQG(i-1)
            s1, s2 = randomizer1.generate_seed_from_string(key_seed)
            j = randomizer.Generate(s1, s2)
            tmp = seq[i]
            seq[i] = seq[j]
            seq[j] = tmp
            i = i-1
        return seq

    def generate_seed_from_string(self, s):
        """
            Generate seeds from string
        """
        str1 = s[:(len(s)//2)]
        str2 = s[len(s)//2:]
        int1 = sum(map(ord, str1)) % self.N
        int2 = sum(map(ord, str2)) % self.N
        return (int1, int2)


def main():
    rnd = PRNGQG(11).Generate(2, 8)
    print ("Random number generator : {}".format(rnd))

    # Test shuffle
    seq = [x for x in range(100)]
    key = "otista"
    randomizer = PRNGQG(len(seq))
    seq = randomizer.shuffle(seq, key)
    print (seq[:20])
if __name__ == '__main__':
    main()
