class dog:
    def __init__(self,name,race):
        self.dogsname = name
        self.dogsrace = race

    def ppp(self):
        print('dogsname:',self.dogsname)
        print('race:',self.dogsrace)

toby = dog('toby','little')
toby.ppp()