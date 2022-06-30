class ActionsNode:
    def __init__(self, actions, nextnode=None):
        self.actions = actions
        self.nextnode = nextnode

    def run(self, machine, tree):
        for action in self.actions:
            action(machine, tree)

    def __str__(self):
        print(self.actions)
        print(self.nextnode)
