"""
    Quasigroup Class
"""
import numpy as np
import random
import time
from RandomnessTest import RandomnessTest

SHIFT_CONSTANT = 2

class PRNGQG():
    def __init__(self, N=256):
        self.N = N # Order of the number range
        self.QG = [[0 for x in range(self.N)] for y in range(self.N)]
        self.gen_matrix = [[0 for x in range(self.N)] for y in range(self.N)]
        self.init_PRNGQG = False
        self.idx = 0
        self.init = False

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

    def generate_seed_from_string(self, s):
        """
            Generate seeds from string
        """
        str1 = s[:(len(s)//2)]
        str2 = s[len(s)//2:]
        int1 = sum(map(ord, str1)) % self.N
        int2 = sum(map(ord, str2)) % self.N
        return (int1, int2)

    def Shuffle_Matrix(self, s1, s2, limit):
        """
            Generate random number using 2 seeds number
            that chose randomly as input.
            limit parameter used to limit the iteration process.
        """
        if (self.init == False):
            self.Initialize_Matrix()
            self.init = True
        for i in range(limit):
            rnd = self.QG[s1][s2]
            s1 = s2
            s2 = rnd
            self.ShuffleColumn(self.idx, s1)
            self.ShuffleRow(self.idx, s2)
            rnd = self.QG[s1][s2]
            self.idx = (self.idx+1)%self.N

    def LookupOperator(self, table, i, j):
        return table[i][j]

    def Phase_1(self):
        if self.init_PRNGQG == True:
            tmp_matrix = self.QG
        else:
            tmp_matrix = self.gen_matrix
        for i in range(self.N):
            if (i < self.N-1):
                for j in range(self.N):
                    if (j < self.N-1):
                        self.gen_matrix[i][j] = self.LookupOperator(tmp_matrix, tmp_matrix[i][j], tmp_matrix[i][j+1])
                    else:
                        self.gen_matrix[i][j] = self.LookupOperator(tmp_matrix, tmp_matrix[i][j], tmp_matrix[i+1][1])
            else:
                for j in range(self.N):
                    if (j < self.N-1):
                        self.gen_matrix[i][j] = self.LookupOperator(tmp_matrix, tmp_matrix[i][j], tmp_matrix[i][j+1])
                    else:
                        self.gen_matrix[i][j] = self.LookupOperator(tmp_matrix, tmp_matrix[i][j], tmp_matrix[1][1])
        self.init_PRNGQG = False

    def Phase_2(self):
        seq = []
        for i in range(self.N):
            seq += self.gen_matrix[i]
        return seq

    def ShiftRow(self, row):
        new_row = [[] for x in range(self.N)]
        for i in range(self.N):
            new_row[i] = row[(i+2) % self.N]
        return new_row

    def Phase_3(self):
        for i in range(self.N):
            self.gen_matrix[i] = self.ShiftRow(self.gen_matrix[i])

    def Generate_Number_Sequence(self, seed_key="haha", limit_shuffle=4, limit=10):
        """
            Function to generate a pseudorandom number sequence
        """
        seq = []
        s1, s2 = self.generate_seed_from_string(seed_key)
        self.Shuffle_Matrix(s1, s2, limit_shuffle)
        self.init_PRNGQG = True
        while (len(seq) < limit):
            self.Phase_1()
            self.init_PRNGQG = False
            seq += self.Phase_2()
            self.Phase_3()
        if (len(seq) > limit):
            seq = seq[:limit]
        return seq

    def extract_qg(self):
        seq = []
        for i in range(self.N):
            seq += self.QG[i]
        return seq

    def Generate_Number_Sequence1(self, seed_key="haha", limit_shuffle=2, limit=10):
        seq = []
        s1, s2 = self.generate_seed_from_string(seed_key)
        self.Shuffle_Matrix(s1, s2, limit_shuffle)
        while (len(seq) < limit):
            seq += self.extract_qg()
            self.Shuffle_Matrix(s1, s2, limit_shuffle)
        if (len(seq) > limit):
            seq = seq[:limit]
        return seq

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

    def shuffle(self, seq, key_seed, opt):
        """
            Shuffle a sequence using provided seed using Fisher-Yates shuffle
        """
        start = time.time()
        rand_seq = self.Generate_Number_Sequence(key_seed, limit_shuffle=2, limit=len(seq))
        # rand_seq = self.Generate_Number_Sequence1(key_seed, limit_shuffle=2, limit=len(seq))
        end = time.time()
        print ("Runtime : {}".format(end-start))
        if (opt):
            i = len(seq)-1
            k = len(seq)-1
            while (i > 1):
                j = rand_seq[k] % i
                seq[j], seq[i] = seq[i], seq[j]
                i = i - 1
                k = k - 1
        else:
            i = 1
            k = 1
            while (i < len(seq)):
                j = rand_seq[k] % i
                seq[j], seq[i] = seq[i], seq[j]
                i = i + 1
                k = k + 1

        return seq

    def get_number(self, seed):
        seq = self.Generate_Number_Sequence(limit=seed+SHIFT_CONSTANT)
        return seq[seed]

def main():
    rnd = PRNGQG(2).Generate_Number_Sequence(limit_shuffle=2, limit=20)
    print ("Random number generator : {}".format(rnd))

    # Test shuffle
    # seq = [x for x in range(92507)]
    # key = "otista"
    # randomizer = PRNGQG(256)
    # seq = randomizer.shuffle(seq, key, True)
    # seq = randomizer.shuffle(seq, key, False)

    # Monobit test
    rnd = [str(x) for x in rnd]
    result = RandomnessTest().monobit(rnd)
    print (result)
    
if __name__ == '__main__':
    main()
