from workflow.graph_engine.entities.workflow_graph import WorkflowGraph
from workflow.nodes.node_mapping import NODE_CLASS_TYPE_MAPPING
from workflow.graph_engine.entities.variable_pool import VariablePool
from workflow.graph_engine.entities.node_entities import NodeRunResult, NodeRunEvent, NodeRunStatus
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import queue
import traceback

class WorkflowRunner:
    def __init__(self, graph: WorkflowGraph, thread_pool: ThreadPoolExecutor):
        self.graph = graph
        self.thread_pool = thread_pool # 执行就绪节点实例
        self.node_states = {}  # 记录每个节点的运行状态
        self.variable_pool = VariablePool()  # 变量池
        self.output_queue = queue.Queue()  # 输出队列
        self.counter = len(self.graph.nodes)  # 计数器

    def run(self, start_node_id: str):
        """从起始节点开始运行工作流"""
        self._run_node(start_node_id)
        
        run_result = []
        while self.counter!=0 or not self.output_queue.empty():
            result = self.output_queue.get()
            run_result.append(result)
            print(f"返回响应: {result}")
            yield f"节点'{self.graph.data[result.node_run_id]["title"]}'执行完成, 结果: {result.output}"
        print("响应结束")
        
        # return run_result

    """运行单个节点"""
    def _run_node(self, node_id: str):
        
        """*检查当前节点就绪情况"""
        node_title = self.graph.data[node_id]["title"]
        print(f"*节点就绪检查: {node_title}_{node_id}->{[self.node_states.get(source) == NodeRunStatus.SUCCEEDED for source, _ in self.graph.edges if _ == node_id]}")
        if all([self.node_states.get(source) == NodeRunStatus.SUCCEEDED for source, _ in self.graph.edges if _ == node_id]):
        
            """获取输入变量值"""
            input_variables = [param["value"]["variables"] for param in self.graph.data[node_id].get("params") if param["type"]=="variable" and param["value"]["isInput"]]
            if input_variables != []:
                for variable in input_variables[0]:
                    
                    value = self.variable_pool.get(variable["value"].split("."))
                    
                    print(f"Variable: {node_title}_{variable["name"]}={value}")
                    
                    if value:
                        self.graph.data[node_id][variable["name"]] = value
                    else:
                        self.graph.data[node_id][variable["name"]] = ""
            
            """组装节点实例"""
            node_cls = NODE_CLASS_TYPE_MAPPING[self.graph.nodes[node_id]]
            node_instance = node_cls(
                node_id=node_id,
                config=self.graph.data[node_id],
                variable_pool=self.variable_pool,
                runtime_state=self.node_states,
                queue=self.output_queue
            )
            
            try:
            
                future = self.thread_pool.submit(node_instance.run)
        
                """*保证在当前节点执行完成后再检查后续节点就绪情况，防止提前检查"""
                wait([future])
                self.counter -= 1
                # yield future

                """*检查后续节点就绪情况"""
                next_nodes = self.graph.get_next_nodes(node_id)
                
                if(len(next_nodes) == 0):
                    """执行结束"""
                    pass
                    # print(self.variable_pool)
                
                # if(len(next_nodes) == 1):
                #     """执行下一个节点"""
                #     result = self.thread_pool.submit(self._run_node, next_nodes[0])
                #     for f in result.result():
                #         yield f
                
                if(len(next_nodes) >= 1):
                    future = []
                    for node in next_nodes:
                        future.append(self.thread_pool.submit(self._run_node, node))
                    
                    # yield future
                    # for f in as_completed(future):
                    #     for r in f.result():
                    #         yield r
                    
                    # wait(future)
                
                else:
                    return
                
            except Exception as e:
                print(f"Node {node_id} failed in _run_node: {traceback.format_exc()}")
                return NodeRunResult(node_run_id=f"node_run_{node_id}", status=NodeRunStatus.FAILED, output=None)
        