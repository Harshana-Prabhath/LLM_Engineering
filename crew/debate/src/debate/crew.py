from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class Debate():
    """Debate crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

   
    @agent
    def debeter(self) -> Agent:
        return Agent(
            config=self.agents_config['debeter'], # type: ignore[index]
            verbose=True
        )

    @agent
    def Judge(self) -> Agent:
        return Agent(
            config=self.agents_config['Judge'], # type: ignore[index]
            verbose=True
        )

   
    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config['propose'], # type: ignore[index]
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config['oppose'], # type: ignore[index]
            
        )
    @task
    def judging_task(self) -> Task:
        return Task(config=self.tasks_config['judging_task'])

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""
        

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
