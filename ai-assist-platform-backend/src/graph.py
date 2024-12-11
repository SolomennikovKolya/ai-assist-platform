from utils import warn, print_green_text
from schemas import schemas, is_valid_json
from prompts import *
import re
import os
from openai import OpenAI, AuthenticationError
import json
from tavily import TavilyClient, MissingAPIKeyError, InvalidAPIKeyError, UsageLimitExceededError
import copy


# Все возможные виды нод
possible_nodes = ["model", "prompt", "chain", "var", "visual", "websearch"]

# Все возможные виды соединений
# possible_connections = [("var", "prompt"), ("model", "chain"), ("prompt", "chain"), ("websearch", "chain"), ("chain", "visual"), ("chain", "prompt")]

class Graph:
    # Инициализация графа (без загрузки узлов, рёбер и т.д.)
    def __init__(self):
        self.nodes: list[Node] = [] # Список всех нод
        self.edges: list[Edge] = [] # Список всех рёбер 
        self.start_node: int        # Индекс ноды (обязательно chain-а), до которого надо просчитать граф
        self.id_to_index = {}       # Соответствие id ноды и её индекса в списке nodes (например "dndnode_3" <-> 1)
        self.valid: bool = False    # Граф становится валидным только после его успешной загрузки из json файла
    
    # Загружает граф из data (в формате json). Одновременно с этим проверяет корректность json-а и самого графа. 
    # Если произошла ошибка загрузки, то возвращает строку ошибки, иначе ничего не возвращает
    def load(self, const_data):
        data = copy.deepcopy(const_data)
        if (res := is_valid_json(data, schemas["external"])) != True:
            return warn(res)

        for node_data in data["nodes"]:
            if "type" not in node_data:
                return warn("Incorrect data format: 'type' is a required property; Double-check this part of the data: " + str(node_data))
            if node_data["type"] not in possible_nodes:
                node_data["type"] = "undefined"
            if (res := is_valid_json(node_data, schemas[node_data["type"]])) != True:
                return warn(res)
            
            match node_data["type"]:
                case "model":
                    self.nodes.append(Model(node_data))
                case "prompt":
                    self.nodes.append(Prompt(node_data))
                case "chain":
                    self.nodes.append(Chain(node_data))
                case "var":
                    self.nodes.append(Var(node_data))
                case "visual":
                    self.nodes.append(Visual(node_data))
                case "websearch":
                    try:
                        self.nodes.append(Websearch(node_data))
                    except MissingAPIKeyError:
                        return warn("API key is missing. Please provide a valid API key for websearch tool")
                    except InvalidAPIKeyError:
                        return warn("Invalid websearch API key provided")
                case _:
                    self.nodes.append(Node(node_data["id"], node_data["type"], node_data["data"]["meta"]))

        for index in range(0, len(self.nodes)):
            id = self.nodes[index].id
            self.id_to_index[id] = index

        for edge_data in data["edges"]:
            if (res := is_valid_json(edge_data, schemas["edge"])) != True:
                return warn(res)
            
            edge_data["source"] = self.id_to_index[edge_data["source"]]
            edge_data["target"] = self.id_to_index[edge_data["target"]]
            source_node: Node = self.nodes[edge_data["source"]]
            target_node: Node = self.nodes[edge_data["target"]]

            match (source_node.type, target_node.type):
                case ("model", "chain"):
                    if target_node.model != None:
                        return warn("Only one model can be connected to chain")
                    target_node.model = source_node
                    
                case ("prompt", "chain"):
                    if target_node.prompt != None:
                        return warn("Only one prompt can be connected to chain")
                    target_node.prompt = source_node

                case ("websearch", "chain"):
                    target_node.tools.append(source_node)

                case ("chain", "visual"):
                    if target_node.chain != None:
                        return warn("Only one chain can be connected to visual")
                    target_node.chain = source_node

                case ("var", "prompt") | ("chain", "prompt"):
                    for i in range(len(target_node.prompt_values)):
                        if target_node.prompt_values[i]["handle"] == edge_data["targetHandle"]:
                            if target_node.prompt_values[i]["var"] != None:
                                return warn("Only one variable or chain can be connected to a single prompt handle")
                            target_node.prompt_values[i]["var"] = source_node        
                            
                case _:
                    if source_node.type in possible_nodes and target_node.type in possible_nodes:
                        return warn(f"You cannot connect {source_node.type} to {target_node.type}")

            self.edges.append(Edge(edge_data))
        
        for node in self.nodes:
            if node.type == "chain" and (node.model == None or node.prompt == None):
                return warn("Prompt and Model must be connected to the Chain")
            
        if data["startNodeID"] not in self.id_to_index:
            return warn("Wrong startNodeID; there is no node with id = startNodeID")
        self.start_node = self.id_to_index[data["startNodeID"]]
        if self.nodes[self.start_node].type != "chain":
            return warn("The start node must be a chain")
        
        if self.has_cycle():
            return warn("The graph is incorrect, because it has a cycle")
            
        self.valid = True

    # Используется в DFS
    def has_cycle_util(self, matrix, visited, cur_nodes, n, start_node):
        visited[start_node] = True
        cur_nodes[start_node] = True

        for neighbour in range(n):
            if matrix[start_node][neighbour]:
                if not visited[neighbour]:
                    if self.has_cycle_util(matrix, visited, cur_nodes, n, neighbour):
                        return True
                elif cur_nodes[neighbour]:
                    return True

        cur_nodes[start_node] = False
        return False

    # Воозвращает True, если в графе есть цикл
    def has_cycle(self):
        n = len(self.nodes)
        matrix = [[0] * n for _ in range(n)]
        for edge in self.edges:
            matrix[edge.source][edge.target] = 1
        
        visited = [False] * n
        cur_nodes = [False] * n
        for start_node in range(n):
            if visited[start_node]:
                continue
            if self.has_cycle_util(matrix, visited, cur_nodes, n, start_node):
                return True
        return False

    # Просчитывает граф, от стартовой ноды
    def calculate(self):
        if not self.valid:
            return warn("The graph is not valid or it has not been loaded yet")

        self.nodes[self.start_node].get_output()
        
        res = {}
        for node in self.nodes:
            if node.type == "chain" and node.model_response != "":
                res[node.id] = node.model_response
        return res            

    # Рекурсивный вывод дерева
    def print_tree(self, cur_node: int, level: int) -> str:
        res = "    " * level + str(cur_node) + ". " + self.nodes[cur_node].type + "\n"
        for edge in self.edges:
            if edge.target == cur_node:
                res += self.print_tree(edge.source, level + 1)
        return res
        
    # Для вывода графа в читабельном для человека виде
    def __str__(self):
        res = "\nNodes:\n"
        for i in range(len(self.nodes)):
            res += "\t" + str(i) + ": " + str(self.nodes[i])
            if i == self.start_node:
                res += " <- start node\n"
            else:
                res += "\n"
        res += "Edges:\n"
        for edge in self.edges:
            res += "\t" + f"{edge.source}. {self.nodes[edge.source].type} \t-> {edge.target}. {self.nodes[edge.target].type}" + "\n"
        res += "Graph:\n"
        res += self.print_tree(self.start_node, 0)
        return res
    
    # Удалить граф (нужно, чтобы удалить неправильно сгенерированный граф)
    def clear(self):
        self.nodes.clear()
        self.edges.clear()
        self.start_node = None
        self.id_to_index.clear()
        self.valid = False

    # Генерирует граф, который соответствует описанию агента. Возвращает описание графа в формате json, либо None, если сгенерировать не получилось
    def generate(agent_description: str, api_key: str):
        base_url = os.getenv("BASE_URL")
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            response = client.models.list()
        except AuthenticationError:
            return warn("Invalid openai API key")
        except Exception as e:
            return warn(f"An error occurred: {e}")
        
        messages = []
        messages.append({"role": "system", "content": generate_graph_system_prompt.format(agent_description=agent_description)})
        messages.append({"role": "user", "content": generate_graph_prompt.format(generate_graph_example=generate_graph_example, variable="{variable}")})
        
        max_iterations = 3
        for iter in range(1, max_iterations + 1):
            completion = client.chat.completions.create(
                # model="gpt-4o-mini",
                model="gpt-4o",
                messages=messages,
            )
            response = completion.choices[0].message.content
            messages.append({"role": "assistant", "content": response})
            print(f"Iteration {iter}:")
            print_green_text(response)
            
            match = re.search(r"```json(.*?)```", response, re.DOTALL)
            if not match:
                messages.append({"role": "user", "content": generate_graph_incorrect_response_correction})
                continue
            
            data = json.loads(match.group(1))
            test_graph = Graph()
            if (warning := test_graph.load(data)) != None:
                messages.append({"role": "user", "content": generate_graph_incorrect_format_correction + " " + warning})
                continue
            return data
        
        return warn("Failed to generate a graph")
                

class Node:
    def __init__(self, id: str, type: str, handles: dict):
        self.id = id            # идентификатор ноды (например "dndnode_0")
        self.type = type        # тип ноды (например "model")
        self.handles = handles  # словарь хэндлов ("название хэндла" : "хэш хэндла")

    def __str__(self):
        return f"{self.id}\t {self.type}"


class Model(Node):
    def __init__(self, node_json):
        super().__init__(node_json["id"], node_json["type"], node_json["data"]["meta"])
        
        node_data = node_json["data"]
        self.api_key = node_data["api_key"]
        self.base_url = os.getenv("BASE_URL")
        self.model_name = node_data["model_name"]
        self.temperature = float(node_data["temperature"])
        self.top_p = float(node_data["top_p"])
        self.max_tokens = int(node_data["max_tokens"])
        self.stop = None if node_data["stop_seq"] == "" else node_data["stop_seq"]
        self.frequency_penalty = float(node_data["freq_penalty"])
        self.presence_penalty = float(node_data["pres_penalty"])
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def get_client(self):
        return self.client
    
    def get_completion(self, messages, tools=None):
        completion = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            stop=self.stop,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            messages=messages,
            tools=tools,
            )
        return completion

    def __str__(self):
        return super().__str__()


class Prompt(Node):
    def __init__(self, node_json):
        super().__init__(node_json["id"], node_json["type"], node_json["data"]["meta"])

        node_data = node_json["data"]
        self.prompt_template = node_data["template"]
        self.prompt_values = [
            {"name": item["name"], "value": item["value"], "handle": item["id"], "var": None}
            for _, item in node_data["prompt_values"].items()]

    # Возвращает отформатированный промпт
    def get_prompt(self) -> str:
        values = {}
        for item in self.prompt_values:
            if (item["var"] != None):
                values[item["name"]] = item["var"].get_output()
            else:
                values[item["name"]] = item["value"]

        def replace_match(match):
            return values.get(match.group(1), match.group(0))
        
        return re.sub(r"\{(\w+)\}", replace_match, self.prompt_template)

    def __str__(self):
        return super().__str__()


class Chain(Node):
    def __init__(self, node_json):
        super().__init__(node_json["id"], node_json["type"], node_json["data"]["meta"])
        
        self.model_response: str = "" # Посчитанный ответ модели
        # Ссылки на ноды, от которых зависит эта нода:
        self.model: Model = None
        self.prompt: Prompt = None
        self.tools: list = []

    def get_output(self) -> str:
        if self.model_response != "":
            return self.model_response
        
        try:
            _ = self.model.get_client().models.list()
        except AuthenticationError:
            self.model_response = "Invalid openai API key"
            return warn(self.model_response)
        except Exception as e:
            self.model_response = f"An error occurred: {e}"
            return warn(self.model_response)
        
        formatted_prompt = self.prompt.get_prompt()
        messages = [{"role": "user", "content": formatted_prompt}]
        
        if len(self.tools) == 0:
            completion = self.model.get_completion(messages)
            self.model_response = completion.choices[0].message.content
            return self.model_response

        else:
            tools = [i.description for i in self.tools]
            available_functions = {i.description["function"]["name"]: i.function for i in self.tools}
            
            completion = self.model.get_completion(messages=messages, tools=tools)
            response_message = completion.choices[0].message
            messages.append(response_message)
            
            tool_calls = response_message.tool_calls
            if not tool_calls:
                self.model_response = response_message.content
                return self.model_response
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(function_args)
                messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
            
            completion = self.model.get_completion(messages)
            self.model_response = completion.choices[0].message.content
            return self.model_response

    def __str__(self):
        return super().__str__()
    

class Var(Node):
    def __init__(self, node_json):
        super().__init__(node_json["id"], node_json["type"], node_json["data"]["meta"])

        self.value = node_json["data"]["var"]

    def get_output(self) -> str:
        return self.value

    def __str__(self):
        return super().__str__()


class Visual(Node):
    def __init__(self, node_json):
        super().__init__(node_json["id"], node_json["type"], node_json["data"]["meta"])
        
        # Ссылки на ноды, от которых зависит эта нода:
        self.chain: Chain = None

    def __str__(self):
        return super().__str__()


class Websearch(Node):
    def __init__(self, node_json):
        super().__init__(node_json["id"], node_json["type"], node_json["data"]["meta"])
        
        self.api_key = node_json["data"]["api_key"]
        self.tavily_client = TavilyClient(api_key=self.api_key)
        self.description = {
            "type": "function",
            "function": {
                "name": "internet_search",
                "description": "Performs an internet search using the Tavily API to retrieve relevant information based on the provided query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information on the internet.",
                        "minLength": 1
                    },
                    "search_depth": {
                        "type": "string",
                        "description": "The depth of the search.",
                        "enum": ["basic", "advanced"],
                        "default": "basic"
                    },
                    "topic": {
                        "type": "string",
                        "description": "The category of the search.",
                        "enum": ["general", "news"],
                        "default": "general"
                    }
                    },
                    "required": ["query"]
                }
            }
        }
    
    def function(self, args: dict):
        try:
            response = self.tavily_client.qna_search(query=args.get("query"), search_depth=args.get("search_depth", "basic"), topic=args.get("topic", "general"))
        except UsageLimitExceededError:
            response = "The limit of using the Internet search tool has been reached."
        except MissingAPIKeyError:
            response =  "API key is missing. Please provide a valid API key for websearch tool"
        except InvalidAPIKeyError:
            response = "Invalid websearch API key provided"
        return response

    def __str__(self):
        return super().__str__()
    

class Edge:
    def __init__(self, edge_data):
        self.source = edge_data["source"]              # Индекс ноды, которая является первым концом ребра (индекс != id)
        self.target = edge_data["target"]              # Индекс ноды, которая является вторым концом ребра
        self.source_handle = edge_data["sourceHandle"] # Хэш хэндла, который соединён с первым концом ребра (хэш != название)
        self.target_handle = edge_data["targetHandle"] # Хэш хэндла, который соединён со вторым концом ребра

    def __str__(self):
        return f"{self.source} -> {self.target}"
