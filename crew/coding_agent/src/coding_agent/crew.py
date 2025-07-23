from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CodingAgent():
    """CodingAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    @agent
    def developer(self) -> Agent:
        return Agent(
            config=self.agents_config['developer'],
            allow_code_execution=True,
            code_execution_mode="safe",
            max_retry_limit=5, 
           
                )
    
    @task
    def solve_question(self) -> Task:
        return Task(config=self.tasks_config['solve_question'])
  
  

    @crew
    def crew(self) -> Crew:
        """Creates the CodingAgent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
