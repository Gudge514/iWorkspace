from enum import StrEnum
from workflow.nodes.start.node import StartNode
from workflow.nodes.end.node import EndNode
from workflow.nodes.llm.node import LLMNode

class NodeType(StrEnum):
    START = "start"
    END = "end"
    # ANSWER = "answer"
    LLM = "llm"
    # KNOWLEDGE_RETRIEVAL = "knowledge-retrieval"
    # IF_ELSE = "if-else"
    # CODE = "code"
    # TEMPLATE_TRANSFORM = "template-transform"
    # QUESTION_CLASSIFIER = "question-classifier"
    # HTTP_REQUEST = "http-request"
    # TOOL = "tool"
    # VARIABLE_AGGREGATOR = "variable-aggregator"
    # LEGACY_VARIABLE_AGGREGATOR = "variable-assigner"  # TODO: Merge this into VARIABLE_AGGREGATOR in the database.
    # LOOP = "loop"
    # ITERATION = "iteration"
    # ITERATION_START = "iteration-start"  # Fake start node for iteration.
    # PARAMETER_EXTRACTOR = "parameter-extractor"
    # VARIABLE_ASSIGNER = "assigner"
    # DOCUMENT_EXTRACTOR = "document-extractor"
    # LIST_OPERATOR = "list-operator"
    
    
NODE_CLASS_TYPE_MAPPING = {
    NodeType.START: StartNode,
    NodeType.END: EndNode,
    NodeType.LLM: LLMNode,
}