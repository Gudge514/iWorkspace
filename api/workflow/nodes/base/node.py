from abc import ABC, abstractmethod
from typing import Any, Generator, Dict, Optional
from workflow.graph_engine.entities.node_entities import NodeRunResult, NodeRunEvent, NodeRunStatus
from workflow.graph_engine.entities.variable_pool import VariablePool
from workflow.graph_engine.entities.variable import Variable
import time
import queue

class BaseNode(ABC):
    """节点基类"""
    node_type: str
    
    def __init__(self, 
                 node_id: str, 
                 config: Dict[str, Any], 
                 variable_pool: VariablePool,
                 runtime_state: Dict[str, Any],
                 queue: queue.Queue) -> None:
        """
        初始化节点
        :param node_id: 节点 ID
        :param config: 节点配置
        :param variable_pool: 可选的变量池，用于存储和共享节点之间的数据
        """
        self.node_id = node_id
        self.config = config
        self.variable_pool = variable_pool or {}
        # self.status = NodeRunStatus.PENDING
        self.runtime_state = runtime_state
        self.runtime_state[self.node_id] = NodeRunStatus.PENDING
        self.queue = queue
        
        self.retry_count = 0
        # self.max_retries = config.get("max_retries", 0)
        # self.retry_interval = config.get("retry_interval", 1)  # 默认重试间隔 1 秒
        self.max_retries = 0
        self.retry_interval = 1

    def run(self):
        """
        节点运行逻辑，子类必须实现此方法
        :return: 生成运行事件
        """
        self.status = NodeRunStatus.RUNNING

        while self.retry_count <= self.max_retries:
            try:
                # 执行节点逻辑
                print(f"Node {self.config["title"]}_{self.node_id} is running...")
                
                start = time.time()
                result = self._run()
                end = time.time()
                
                print(f"Node {self.config["title"]}_{self.node_id} finished in {end-start} seconds.")
                
                self.runtime_state[self.node_id] = NodeRunStatus.SUCCEEDED
                self.queue.put(result)
                
                return result
            except Exception as e:
                print(f"Node {self.node_id} failed: {e}")
                self.status = NodeRunStatus.RETRYING
                self.retry_count += 1
                if self.retry_count > self.max_retries:
                    # self.status = NodeRunStatus.FAILED
                    self.runtime_state[self.node_id] = NodeRunStatus.FAILED
                    return

    @abstractmethod
    def _run(self) -> NodeRunResult:
        """
        节点的具体执行逻辑，子类必须实现
        :return: 执行结果
        """
        pass

    def update_variable_pool(self, selector: list[str], value: Variable):
        self.variable_pool.add(selector, value)

    def get_variable(self, selector: list[str]) -> Optional[Variable]:
        return self.variable_pool.get(selector).value