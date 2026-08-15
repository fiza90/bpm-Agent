from services.mining_service import MiningService



class MiningAgent:


    def __init__(self):

        self.mining_service = MiningService()



    def analyze(self, file):


        return self.mining_service.analyze_event_log(
            file
        )