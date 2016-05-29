class A():
    def __init__(self,a):
        self.a=a
    def set_a(self,aa):
        self.a=aa
    def get_a(self):
        return self.a

if __name__=="__main__":
    ta=A("this is a test")
    print ta.get_a()
    ta.set_a("this is a change")
    print ta.get_a()


    # bb.
