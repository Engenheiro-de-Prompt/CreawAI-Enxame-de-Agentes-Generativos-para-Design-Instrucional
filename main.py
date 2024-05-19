import os
import shutil
import yaml
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Limpar variáveis de ambiente
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("SERPER_API_KEY", None)
os.environ.pop("OPENAI_MODEL", None)

# Redefinir variáveis de ambiente
os.environ["OPENAI_API_KEY"] = "API"
os.environ["SERPER_API_KEY"] = "API"
os.environ["OPENAI_MODEL"] = "gpt-4o"

# Remover __pycache__ e arquivos .pyc
for root, dirs, files in os.walk("."):
    for dir in dirs:
        if dir == "__pycache__":
            shutil.rmtree(os.path.join(root, dir))
    for file in files:
        if file.endswith(".pyc"):
            os.remove(os.path.join(root, file))

# Função para ler o arquivo YAML
def read_yaml(file_path):
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return {}
    with open(file_path, 'r') as file:
        return yaml.safe_load(file) or {}

# Caminhos dos arquivos YAML
agents_file_path = "/home/virtualis/Área de Trabalho/Assistent/CrewAI 1/CrewAI educacional/agentes.yaml"
tasks_file_path = "/home/virtualis/Área de Trabalho/Assistent/CrewAI 1/CrewAI educacional/tasks.yaml"

# Ler a configuração dos agentes e tarefas
agents_config = read_yaml(agents_file_path)
tasks_config = read_yaml(tasks_file_path)

# Inicializar a ferramenta de pesquisa
search_tool = SerperDevTool()

# Função para criar um agente a partir da configuração (sem ferramentas inicialmente)
def create_agent(agent_config):
    print(f"Criando agente com configuração: {agent_config}")
    try:
        agent = Agent(
            role=agent_config['role'],
            goal=agent_config['goal'],
            backstory=agent_config['backstory'],
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', False)
        )
        print(f"Agente criado: {agent}")
    except KeyError as e:
        print(f"Erro ao criar agente: {e}")
        raise
    return agent

# Verifique se a chave 'agents' existe
if 'agents' in agents_config:
    agents = [create_agent(agent) for agent in agents_config['agents']]
else:
    print("Chave 'agents' não encontrada em agents_config.")
    agents = []

# Adicionar as ferramentas manualmente
for agent in agents:
    if agent.role == "Gerente de Educação":
        agent.tools = [search_tool]
    elif agent.role == "Escritor de Artigos":
        agent.tools = [search_tool]
    elif agent.role == "Leitor de Arquivos":
        agent.tools = []
    elif agent.role == "Crítico de Aulas":
        agent.tools = [search_tool]
    elif agent.role == "Pedagogia Heutagógica":
        agent.tools = []
    elif agent.role == "Aplicador de Questões":
        agent.tools = []

# Função para criar uma tarefa a partir da configuração
def create_task(task_config, agents):
    agent_role = task_config['agent']
    agent = next((agent for agent in agents if agent.role == agent_role), None)
    if agent is None:
        print(f"Agente com role '{agent_role}' não encontrado.")
        return None
    print(f"Criando tarefa com configuração: {task_config}")
    task = Task(
        description=task_config['description'],
        expected_output=task_config['expected_output'],
        agent=agent,
        parameters=task_config.get('parameters', {})  # Adicionar os parâmetros
    )
    print(f"Tarefa criada: {task}")
    return task

# Verifique se a chave 'tarefas' existe
if 'tarefas' in tasks_config:
    tasks = [create_task(task, agents) for task in tasks_config['tarefas'] if create_task(task, agents) is not None]
else:
    print("Chave 'tarefas' não encontrada em tasks_config.")
    tasks = []

# Função para leitura de arquivos no diretório especificado
def read_files_in_directory(directory_path):
    try:
        files_content = ""
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    files_content += f"Conteúdo de {filename}:\n{file.read()}\n\n"
        return files_content
    except Exception as e:
        return str(e)



# Instanciar o crew com um processo sequencial
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=2  # Nível de logging
)

# Iniciar o trabalho do crew
result = crew.kickoff()

print("######################")
print(result)
