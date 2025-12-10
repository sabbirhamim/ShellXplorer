class History:
    def __init__(self):
        self.commands = []

    def add(self, cmd):
        self.commands.append(cmd)

    def show(self):
        for i, cmd in enumerate(self.commands):
            print(i, cmd)

    def last(self):
        return self.commands[-1] if self.commands else ""

    def get(self, index):
        return self.commands[index] if index < len(self.commands) else ""
