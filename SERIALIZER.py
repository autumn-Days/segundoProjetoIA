class DataHandler:
    def __init__(self, locals_=None, eucDistancies=None, flows=None):
        self.locals_ = locals_ if locals_ is not None else []
        self.eucDistancies = eucDistancies if eucDistancies is not None else {}
        self.flows = flows if flows is not None else {}

    def serialize(self, filename):
        with open(filename, 'w') as file:
            file.write(" ".join(f"{a} {b}" for a, b in self.locals_) + "\n")
            file.write("-\n")

            for (a, b), (c, d) in self.eucDistancies:
                file.write(f"{a} {b} {c} {d} {self.eucDistancies[((a, b), (c, d))]}\n")
            file.write("-\n")

            for (a, b), value in self.flows.items():
                file.write(f"{a} {b} {value}\n")

    def deserialize(self, filename):
        with open(filename, 'r') as file:
            self.locals_ = []
            for line in file:
                line = line.strip()
                if line == "-":
                    break
                numbers = list(map(int, line.split()))
                self.locals_.extend([(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)])

            self.eucDistancies = {}
            for line in file:
                line = line.strip()
                if line == "-":
                    break
                numbers = list(map(int, line.split()))
                key = ((numbers[0], numbers[1]), (numbers[2], numbers[3]))
                value = numbers[4]
                self.eucDistancies[key] = value

            self.flows = {}
            for line in file:
                numbers = list(map(int, line.split()))
                key = (numbers[0], numbers[1])
                value = numbers[2]
                self.flows[key] = value
