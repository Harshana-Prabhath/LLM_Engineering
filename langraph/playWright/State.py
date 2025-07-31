from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from pydantic import BaseModel



class State(TypedDict):
    messages: Annotated[list, add_messages]



class NavigationType(BaseModel):
    url: str

class ExtractType(BaseModel):
    pass
