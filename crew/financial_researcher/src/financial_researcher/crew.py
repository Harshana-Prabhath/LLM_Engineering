from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool


@CrewBase
class FinancialResearcher():
    """FinancialResearcher crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

   
    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'],tools=[SerperDevTool()])
    
    @agent
    def analyst(self) -> Agent:
        return Agent(config=self.agents_config['analyst'])
    
    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])
    
    @task
    def reporting_task(self) -> Task:
        return Task(config=self.tasks_config['reporting_task'])
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            Process = Process.sequential,
            verbose = True,
        )
