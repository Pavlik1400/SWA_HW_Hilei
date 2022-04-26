class Value:
    # amount = 0

    # def __eq__(self, other: 'Value'):
    #     other.__class__ = Value
    #     return self.amount == other.amount

    def __init__(self, other: 'Value'=None):
        if other is not None:
            self.amount = other.amount
        else:
            self.amount = 0

N = 20000