class A():
    def set_a(self,aa):
        fp=open("test_p","w")
        fp.write(aa)
        fp.close()
    def get_a(self):
        fp=open("test_p","r")
        str=fp.read()
        fp.close()
        return str

class B(A):
    def say(self):
        print self.get_a()
    def a_change(self,b):
        self.set_a(b)

class C(A):
    def say(self):
        print self.get_a()
    def a_change(self,c):
        self.set_a(c)

if __name__=="__main__":
    bb=B()
    bb.say()
    bb.a_change("change by B")
    bb.say()
    cc=C()
    cc.say()


    # bb.
