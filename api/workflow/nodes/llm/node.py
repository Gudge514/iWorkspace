from openai import OpenAI
from workflow.nodes.base.node import BaseNode
from workflow.graph_engine.entities.node_entities import NodeRunResult, NodeRunStatus
from uuid import uuid4

import requests
from typing import Any

class LLMNode(BaseNode):
    """
    一个用于调用大型语言模型（LLM）的节点
    """
    node_type = "llm"
    
    def _run(self) -> Any:
        """
        调用 LLM 接口
        :return: 模型的响应数据
        """

        # 调用 LLM 接口
        try:
            base_url = [param["value"]["baseUrl"] for param in self.config.get("params") if param["type"]=="model"][0]
            api_key = [param["value"]["apiKey"] for param in self.config.get("params") if param["type"]=="model"][0]
            model_name = [param["value"]["modelName"] for param in self.config.get("params") if param["type"]=="model"][0]
            
            # prompt = self.get_variable([self.node_id, "prompt"])
            messages = [param["value"]["messages"] for param in self.config.get("params") if param["type"]=="prompt"][0]

            # 解析输入参数
            input_variables = [param["value"]["variables"] for param in self.config.get("params") if param["type"]=="variable" and param["value"]["isInput"]]
            if input_variables != []:
                for message in messages:
                    for variable in input_variables[0]:
                        message["content"] = message["content"].replace(f"{{{{ {variable['name']} }}}}", self.config[variable["name"]])
                            
            # if not api_url or not api_key:
            #     raise ValueError("LLM API URL 和 API Key 不能为空！")
            # if not prompt:
            #     raise ValueError("输入的 prompt 不能为空！")

            client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )
            
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
            )

            # 解析响应结果
            result = response.choices[0].message.content
            output = result.strip()

            # 将生成的文本存储到变量池
            output_variables = [param["value"]["variables"] for param in self.config.get("params") if param["type"]=="variable" and not param["value"]["isInput"]][0]
            self.update_variable_pool([self.node_id, output_variables[0]["id"]], output)
            # print(output)
            return NodeRunResult(node_run_id=self.node_id, status=NodeRunStatus.SUCCEEDED, output=output)

        except Exception as e:
            print(f"调用 LLM 接口失败: {str(e)}")
            raise RuntimeError(f"调用 LLM 接口失败: {str(e)}")
