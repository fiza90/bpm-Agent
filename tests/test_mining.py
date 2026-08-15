from agents.mining_agent import MiningAgent



agent = MiningAgent()


with open(
    "data/sample_event_log.csv",
    "rb"
) as file:


    result = agent.analyze(
        file
    )


print(result)