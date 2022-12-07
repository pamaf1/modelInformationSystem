import numpy as np

class FunRand:
    @staticmethod
    def erlanga(timeMean, k):
        return np.random.gamma(shape = k, scale = timeMean / k)

    @staticmethod
    def exp(timeMean):
        a = 0
        while a == 0:
            a = np.random.rand()
        return -timeMean * np.log(a)
    
    @staticmethod
    def unif(timeMin, timeMax):
        a = 0
        while a == 0:
            a = np.random.rand()
        a = timeMin + a * (timeMax - timeMin)
        return a
    
    @staticmethod
    def norm(timeMean, timeDiversion):
        return np.random.normal(loc = timeMean, scale = timeDiversion)