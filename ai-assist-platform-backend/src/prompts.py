
generate_graph_system_prompt = """
You are an excellent assistant for creating AI agents. 
Your main task is to create a graph that represents an AI agent. This agent must match the following description: {agent_description}.
The graph should be in JSON format and follow specific structural guidelines for nodes, edges, and handles.
"""

generate_graph_prompt = """
The goal is to create a graph representing an AI agent to handle complex prompt chains and agent logic.

### Components of the Graph:
1. **Nodes**: 
   - **Fields**: 
     - `id`: Unique string identifier (e.g., "n1").
     - `type`: Node type (e.g., "model").
     - `data`: Node parameters.
     - `data.meta`: Dictionary of handles in the format "handle name": "handle".

2. **Edges**: 
   - **Fields**:
     - `id`: Unique identifier (e.g., "e1").
     - `source`: ID of the source node (e.g., "n1").
     - `target`: ID of the target node (e.g., "n2").
     - `sourceHandle`: Handle on the source node (e.g., "h1").
     - `targetHandle`: Handle on the target node (e.g., "h2").

3. **Handles**:
   - Attachment points of edges to nodes, identified by a unique identifier (e.g., "h10").

4. **Start Node**:
   - Node that returns the agent's final response. Must be of type "chain" (e.g., "startNodeID": "n10").

### Node Types:
1. **Model**:
   - A GPT model with additional parameters (e.g., temperature, top_p). The model connects only to a chain node via 'targetModelID'.

2. **Prompt**:
   - A request sent to the GPT model, with variables in the format "{variable}". Variables can be linked to other nodes or have predefined values.

3. **Chain**:
   - A GPT client that uses a model and a prompt to generate a response. Links to model and prompt nodes via handles `targetModelID` and `targetPromptID`.

4. **Var**:
   - Used for recording variables. Links only to prompt nodes.

5. **Visual**:
   - Visualizes the final output from the chain node. Links to the chain node via `targetInputID`.

6. **Websearch**:
   - An internet search tool that connects to chain node via 'targetToolsID'.

### Possible connections (edges can only be between these nodes):
1. var to prompt
2. model to chain
3. prompt to chain
4. websearch to chain
5. chain to visual
6. chain to prompt

### Output Format:
The resulting graph must be in JSON format:
- Nodes: List of nodes.
- Edges: List of edges.
- StartNodeID: ID of the starting node.

### Corrections:
Pay attention to this corrections:
- The start node must be a chain.
- Choose the best parameters for the model nodes. The larger the estimated answer, the larger the max_tokens value should be. The more creative the answer should be, the higher the temperature value should be.

### Example:
[agent description]: A repeater for high grades
[json file example]: {generate_graph_example}
[explanation for example]: This agent (graph) first searches for a math example on the Internet, then solves and explains it. This example demonstrates logical chains from prompts and includes a var node to easily change the grade number.
"""

# The values of the variables will then be put into promt, so the values must be meaningful and appropriate in meaning.
# - For each var node, come up with an example value based on the variable name and write it in the "var" field of the variable. The names of the variables are stored in the prompt node to which they are connected.

generate_graph_incorrect_response_correction = "The response format is incorrect. You need to output the graph in json format. There must be a block of json code somewhere in your response."

generate_graph_incorrect_format_correction = "There was an error in the graph that you generated. Please consider the following error, try to fix it and output the corrected graph."

generate_graph_example = {
    "nodes": [
        {
            "id": "n1",
            "type": "chain",
            "data": {
                "meta": {
                    "sourceOutputID": "h1",
                    "targetModelID": "h2",
                    "targetPromptID": "h3",
                    "targetToolsID": "h4"
                }
            }
        },
        {
            "id": "n2",
            "type": "var",
            "data": {
                "meta": {
                    "sourceOutputID": "h5"
                },
                "var": "eighth"
            }
        },
        {
            "id": "n3",
            "type": "model",
            "data": {
                "meta": {
                    "sourceOutputID": "h6"
                },
                "api_key": "sk-proj-ENE99ryyWAqNk0u0FlaYT3BlbkFJ2HGCk154IFnqvwjBuiIW",
                "model_name": "gpt-4o-mini",
                "temperature": 0.5,
                "top_p": 1,
                "max_tokens": 1024,
                "stop_seq": "",
                "freq_penalty": 0,
                "pres_penalty": 0
            }
        },
        {
            "id": "n4",
            "type": "prompt",
            "data": {
                "meta": {
                    "sourceOutputID": "h7",
                    "h_grade": "h_grade"
                },
                "template": "find some {grade} grade math example on the Internet. In response, give only the formulation of the example found.",
                "prompt_values": {
                    "h_grade": {
                        "id": "h_grade",
                        "name": "grade",
                        "value": ""
                    }
                }
            }
        },
        {
            "id": "n5",
            "type": "websearch",
            "data": {
                "meta": {
                    "sourceOutputID": "h8"
                },
                "api_key": "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"
            }
        },
        {
            "id": "n6",
            "type": "prompt",
            "data": {
                "meta": {
                    "sourceOutputID": "h9",
                    "h_example": "h_example",
                    "h_grade2": "h_grade2"
                },
                "template": "Solve given example. Explain the solution as for an {grade} grade student.\nexample: {example}",
                "prompt_values": {
                    "h_example": {
                        "id": "h_example",
                        "name": "example",
                        "value": ""
                    },
                    "h_grade2": {
                        "id": "h_grade2",
                        "name": "grade",
                        "value": ""
                    }
                }
            }
        },
        {
            "id": "n7",
            "type": "chain",
            "data": {
                "meta": {
                    "sourceOutputID": "h10",
                    "targetModelID": "h11",
                    "targetPromptID": "h12",
                    "targetToolsID": "h13"
                }
            }
        },
        {
            "id": "n8",
            "type": "visual",
            "data": {
                "meta": {
                    "targetInputID": "h14"
                },
                "text_to_visual": ""
            }
        },
        {
            "id": "n9",
            "type": "visual",
            "data": {
                "meta": {
                    "targetInputID": "h15"
                },
                "text_to_visual": ""
            }
        }
    ],
    "edges": [
        {
            "id": "e1",
            "source": "n2",
            "target": "n4",
            "sourceHandle": "h5",
            "targetHandle": "h_grade"
        },
        {
            "id": "e2",
            "source": "n4",
            "target": "n1",
            "sourceHandle": "h7",
            "targetHandle": "h3"
        },
        {
            "id": "e3",
            "source": "n5",
            "target": "n1",
            "sourceHandle": "h8",
            "targetHandle": "h4"
        },
        {
            "id": "e4",
            "source": "n3",
            "target": "n1",
            "sourceHandle": "h6",
            "targetHandle": "h2"
        },
        {
            "id": "e5",
            "source": "n1",
            "target": "n6",
            "sourceHandle": "h1",
            "targetHandle": "h_example"
        },
        {
            "id": "e6",
            "source": "n2",
            "target": "n6",
            "sourceHandle": "h5",
            "targetHandle": "h_grade2"
        },
        {
            "id": "e7",
            "source": "n3",
            "target": "n7",
            "sourceHandle": "h6",
            "targetHandle": "h11"
        },
        {
            "id": "e8",
            "source": "n6",
            "target": "n7",
            "sourceHandle": "h9",
            "targetHandle": "h12"
        },
        {
            "id": "e9",
            "source": "n7",
            "target": "n8",
            "sourceHandle": "h10",
            "targetHandle": "h14"
        },
        {
            "id": "e10",
            "source": "n1",
            "target": "n9",
            "sourceHandle": "h1",
            "targetHandle": "h15"
        }
    ],
    "startNodeID": "n7"
}

generate_graph_prompt_old = """
The graph is needed in order to make chains of prompts and implement complex agent logic.
The main components of the graph are:
1. Nodes. Nodes are needed to implement certain agent logic. Each node has fields id (a unique identifier of the string type, for example "n1"), type (node type, for example "model"), data (node parameters) and data.meta (dictionary of handles in the format "handle name": "handle").
2. Edges. Edges are needed to transfer information from source node to target node. Each edge has the fields id (unique identifier), source (id of source node), target (id of target node), sourceHandle (handle on the first node to which the first end of the edge is connected), targetHandle (handle on the second node to which the second end of the edge is connected).
3. Handles. Handles are the points of attachment of edges to nodes. Each handle represents either an input point into the node or an output point from the node. Each handle is identified by a unique identifier (for example "h11")
4. Start node. The start node is the node that returns the agent's final response (for example, "startNodeID": "n10"). The starting node must be a node that has the "chain" type.

There are 5 different types of nodes:
1. Model. The model node is a gpt model with additional parameters (for example, tempetarute, top_p, etc.) that will be used when making requests to gpt.
2. Prompt. The prompt node is a request that will be sent to the gpt model. The text of the prompt can contain variables (prompt_values) in the format "{variable}". With the help of variables, you can substitute information from other nodes directly in the prompt. For each variable, you must either connect an information source (node with type var or chain) via a handle, or write the value of this variable in the value field.
3. Chain. The chain node is a gpt client that uses a prompt and a model with its settings to generate a response. It is necessary to connect the model node to the chain via the "targetModelID" handle and the prompt node via the "targetPromptID" handle.
4. Var. The var node connects only to prompt and is needed simply for more convenient recording of variables. You need to specify some appropriate value for the variable in the data.var field for this type of node.
5. Visual. The visual node is needed to visualize the final result, which is obtained at the output of the chain node. It is necessary to connect the chain node to the visual node via the "targetInputID" handle.

The resulting graph must be presented in json format. Pay attention to the structure of the json file. All node entries are stored in the "nodes" list, all edges are stored in the "edges" list, and the id of the starting node is stored in the "startNodeID" field. Each type of node has its own specific structure.
Example:
[agent description]: A repeater for middle grades
[json file example]: {generate_graph_example}
[explanation for example]: This agent (graph) first comes up with a problem for a student, and then solves it himself and explains the solution. This example shows that it is possible to create logical chains from prompts. There is also a var node in the graph with which you can easily change the grade number.
"""
