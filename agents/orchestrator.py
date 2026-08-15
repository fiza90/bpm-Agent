from agents.planner import PlannerAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.response_agent import ResponseAgent

from memory.execution_context import ExecutionContext



class OrchestratorAgent:


    def __init__(self):

        self.planner = PlannerAgent()

        self.knowledge_agent = KnowledgeAgent()

        self.response_agent = ResponseAgent()

        self.context = ExecutionContext()



    def execute(self, user_request):


        self.context.user_request = user_request


        print("Creating execution plan...")


        plan = self.planner.create_plan(
            user_request
        )


        print(
            "Plan:",
            plan
        )


        process = plan.get(
            "process"
        )


        for step in plan.get("plan", []):


            print(
                "Executing:",
                step
            )


            result = self.execute_step(
                step,
                process
            )


            step_name = (

                step["task"]

                if isinstance(step, dict)

                else step

            )


            self.context.add(
                step_name,
                result
            )


        # Generate final AI response

        final_response = self.response_agent.generate_response(

            self.context.all()

        )


        return final_response




    def execute_step(self, step, process):


        if isinstance(step, dict):

            step_name = step["task"]

        else:

            step_name = step



        # Explain process

        if step_name == "Explain process":


            return self.knowledge_agent.explain_process(

                process

            )



        # Process search fallback

        elif step_name == "process_search":


            return self.knowledge_agent.find_process(

                self.context.user_request

            )



        # Bottleneck analysis

        elif step_name == "Identify bottlenecks":


            return {


                "status": "completed",


                "process":

                process.get("name")

                if process

                else None,


                "bottlenecks": [

                    "Manual activities",

                    "Approval delays",

                    "Process inefficiencies"

                ]

            }



        # Recommendations

        elif step_name == "Recommend improvements":


            return {


                "status": "completed",


                "process":

                process.get("name")

                if process

                else None,


                "recommendations": [

                    "Automate repetitive tasks",

                    "Improve workflow approvals",

                    "Increase process monitoring"

                ]

            }



        else:


            return {


                "status": "unknown_step",


                "message":

                f"No agent available for step: {step_name}"

            }