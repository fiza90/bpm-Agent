from services.tavily_service import TavilyService


service = TavilyService()


query = "Procure to Pay business process"


response = service.search(query)


print("\nSearch Query:")
print(query)

print("\nRaw Response:\n")
print(response)