#AUTHOR = Karl Sachs

class Party():
    def __init__(self, name, G, g, q, sigma):
        self.name = name

        self.G = G        # Group
        self.g = g        # generator
        self.q = q        # Prime

        self.sigma = sigma

        print(name)
        print(self.Stage1())
        return 
    
    def Stage1(self):
        self.x_1 = self.G.RandomlyGenerateGroupElement()
        self.x_2 = self.G.RandomlyGenerateGroupElement()

        self.X_1 = self.G.GroupSpecificDLP(self.g, self.x_1)
        self.X_2 = self.G.GroupSpecificDLP(self.g, self.x_2)

        self.pi_1 = self.Prv()
        self.pi_2 = self.Prv()

        return (self.x_1, self.x_2, self.X_1, self.X_2, self.pi_1, self.pi_2)

    # specifi sJ-PAKE function for Proving
    def Prv(self):
        return None
    
    
