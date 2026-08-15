from agents.knowledge_agent import KnowledgeAgent


agent = KnowledgeAgent()


result = agent.find_process(
    "Invoice-to-Cash"
)


print(result)