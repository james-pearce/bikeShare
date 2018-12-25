# def hi(obj):
#     print ("Hi, I am " + obj.name)

class Robot:
    def __init__(self, name=None, build_year=2000):
        self.name = name
        self.build_year = build_year

    def __repr__(self):
        return "Robot('" + self.name + "', " + str(self.build_year) + ")"

    def __str__(self):
        return "Name: " + self.name + "; Build year: " + str(self.build_year)

    def say_hi(self):
        if self.name:
            print ("Hi, I am " + self.name + ".")
        else:
            print ("Hi, I am a robot without a name.")
        if self.build_year:
            print ("I was built in " + str(self.build_year) + ".")
        else:
            print("It's not known when I was created.")

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_build_year(self, by):
        self.build_year = by

    def get_build_year(self):
        return self.build_year

if __name__ == "__main__":
    x = Robot("Marvin", 1979)
    y = Robot("Caliban", 1943)

    for rob in [x, y]:
        rob.say_hi()
        if rob.get_name() == "Caliban":
            rob.set_build_year(1993)
        print ("I was built in the year " + str(rob.get_build_year()) + "!")

