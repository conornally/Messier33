from sys import stdout

class Loading:
    def __init__(self, n_max, length=25):
        self.n_max=n_max
        self.frac=0
        self.n=0
        self.length=length

    def __call__(self, i):
        if(i==0): 
            stdout.write("|")
            for i in range(self.length): stdout.write(" ")
            stdout.write("|\x1b[%sD"%(self.length+1))
        else:
            self.frac=i/self.n_max
            _n= int(self.length*self.frac)
            if(_n>self.n):
                self.n=_n
                self.display()

    def display(self):
        stdout.write("=>\x1b[1D")
        stdout.flush()

        
if __name__=="__main__":
    import time
    l=Loading(100, 30)
    for i in range(100):
        time.sleep(0.1)
        l(i)
