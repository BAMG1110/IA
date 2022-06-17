class pw():
    def __init__(self, name, peso):
        self.name = name
        self.peso = peso

    def __repr__(self):
        return f"{self.peso}"


p0 = pw("prueba", 2)
p1 = pw("prueba", 11)
p2 = pw("prueba", 5)
p3 = pw("prueba", 6)
p4 = pw("prueba", 7)

lista = [p0, p1, p2, p3, p4]

newlist = sorted(lista, key=lambda obj: obj.peso)

print(newlist)