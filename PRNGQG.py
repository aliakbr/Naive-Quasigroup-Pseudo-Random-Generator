"""
    Quasigroup Class
"""

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

    def Generate(self, s1, s2, limit):
        """
            Generate random number using 2 seeds number
            that chose randomly as input.
            limit parameter used to limit the iteration process.
        """
        self.Initialize_Matrix()
        while (self.idx < limit):
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

def main():
    rnd = PRNGQG().Generate(131, 150, 100)
    print ("Random number generator : {}".format(rnd))

if __name__ == '__main__':
    main()
