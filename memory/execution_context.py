
class ExecutionContext:


    def __init__(self):

        self.data = {}



    def add(
            self,
            key,
            value
    ):

        self.data[key] = value



    def get(
            self,
            key
    ):

        return self.data.get(key)



    def all(self):

        return self.data