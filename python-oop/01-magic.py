class A:
    def __init__(self):
        self.pub = "I am public"
        self._prot = "I am protected"
        self.__priv = "I am private"

x = A()
print (x.pub)

x.pub = x.pub + " and my value can be changed."
print (x.pub)

print (x._prot)

x._prot = x._prot + " and can my value be changed?"
print(x._prot)

print (x.__priv)