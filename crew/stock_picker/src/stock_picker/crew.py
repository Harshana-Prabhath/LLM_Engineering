from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from crewai.memory import LongTermMemory,ShortTermMemory,EntityMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage


class Company(BaseModel):
    "Structure of the each company"
    name: str = Field(description="Name of the company")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company was choosen")

class CompanyList(BaseModel):
    "Structure of the list of companies"
    companies: List[Company] = Field(description=" A List of choosen companies")

class ResearchCompany(BaseModel):
    "Structure of the attributes of researched company"
    name: str = Field(description="Name of the comapny")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and frowth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class ResearchCompanyList(BaseModel):
    research_list : List[ResearchCompany] = Field(description="Comprehensive research on all trending companies")




@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

   
    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config= self.agents_config['trending_company_finder'], tools=[SerperDevTool()])
    
    @agent
    def financial_business_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_business_researcher'], tools=[SerperDevTool()])
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'])

    
    @task
    def find_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['find_trending_companies'], output_pydantic= CompanyList)
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['research_trending_companies'], output_pydantic= ResearchCompanyList)
    
    @task
    def pick_the_best_company(self) -> Task:
        return Task(config=self.tasks_config['pick_the_best_company'])

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager = Agent(config=self.agents_config['manager'], allow_delegation=True)
       

        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True,
            memory=True,
            long_term_memory= LongTermMemory(storage=LTMSQLiteStorage(
                db_path="./memory/long_term_memory_storage.db"
            )),
            short_term_memory= ShortTermMemory(
                storage=RAGStorage(
                    embedder_config={
                            "provider": "openai",
                            "config": {
                                "model": 'text-embedding-3-small'
                            }
                        },
                        type="short_term",
                        path="./memory/"

                )
                ),
            entity_memory=EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            )
            
        )
