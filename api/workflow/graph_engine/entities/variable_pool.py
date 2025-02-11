from workflow.graph_engine.entities.variable import Variable
from collections import defaultdict
from pydantic import BaseModel, Field

# 全局变量池，被图引擎持有
class VariablePool(BaseModel):
    # 变量字典
    variable_dictionary: dict[str, dict[int, Variable]] = Field(
        description="Variables mapping",
        default=defaultdict(dict),
    )
    
    # 环境变量
    environment_variable: dict[str, Variable] = Field(
        description="Environment variables",
        default={},
    )
    
    # 输入参数
    input_variable: dict[str, Variable] = Field(
        description="Input variables",
        default={},
    )
    
    def __init__(self, environment_variable, input_variable):
        super().__init__()
        self.environment_variable = environment_variable
        self.input_variable = input_variable
        
    def __init__(self):
        super().__init__()
        pass
        
    def add(self, selector, value):
        self.variable_dictionary[selector[0]][hash(tuple(selector[1:]))] = value
        
    def get(self, selector):
        return self.variable_dictionary[selector[0]][hash(tuple(selector[1:]))]
    
    def remove(self, selector):
        if not selector:
            return
        if len(selector) == 1:
            self.variable_dictionary[selector[0]] = {}
            return
        self.variable_dictionary[selector[0]].pop(hash(tuple(selector[1:])))
        
    def __repr__(self):
        return f"VariablePool({self.variable_dictionary})"