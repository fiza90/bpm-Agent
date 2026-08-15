from agents.knowledge_agent import KnowledgeAgent


class PlannerAgent:


    def __init__(self):

        self.knowledge_agent = KnowledgeAgent()



    def create_plan(self, user_request):


        print(
            "Creating plan for:",
            user_request
        )


        # Find matching process

        process = self.knowledge_agent.find_process(
            user_request
        )


        print(
            "Process found by planner:",
            process
        )



        plan = []



        if process:


            plan.append(
                {
                    "task": "Explain process"
                }
            )


            plan.append(
                {
                    "task": "Identify bottlenecks"
                }
            )


            plan.append(
                {
                    "task": "Recommend improvements"
                }
            )


        else:


            plan.append(
                {
                    "task": "process_search"
                }
            )



        return {

            "process": process,

            "plan": plan

        }