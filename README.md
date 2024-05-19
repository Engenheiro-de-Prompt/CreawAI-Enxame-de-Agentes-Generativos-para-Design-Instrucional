# Enxame de Agentes Generativos para Design Instrucional

## Descrição

Este repositório apresenta um projeto inovador que utiliza um enxame de agentes generativos para substituir um setor completo de design instrucional. Usando o framework CrewAI, configuramos e coordenamos múltiplos agentes para criar um pacote educacional completo sobre energia renovável. Este projeto demonstra como a automação avançada pode ser aplicada para otimizar processos educacionais e produzir materiais de alta qualidade de forma eficiente.

## Funcionalidades

- **Configuração de Agentes**: Define agentes com diferentes papéis, incluindo Gerente de Educação, Escritor de Artigos, Crítico de Aulas, Pedagogia Heutagógica e Aplicador de Questões.
- **Delegação de Tarefas**: Permite ao Gerente de Educação delegar tarefas específicas aos agentes apropriados.
- **Execução Coordenada**: Utiliza o framework CrewAI para coordenar a execução das tarefas entre os agentes.
- **Criação de Conteúdo**: Produz artigos detalhados, roteiros de aula heutagógicos, atividades práticas e questões de avaliação.
- **Revisão e Aperfeiçoamento**: Inclui um processo de revisão para garantir a precisão e a qualidade dos conteúdos criados.

## Como Usar

1. **Instalação de Dependências**:
   Certifique-se de ter o Python instalado e instale as dependências necessárias utilizando `pip`:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configuração das Variáveis de Ambiente**:
   Defina as variáveis de ambiente necessárias para acessar as APIs do OpenAI e SerperDevTool.

   ```bash
   export OPENAI_API_KEY="sua-chave-api-openai"
   export SERPER_API_KEY="sua-chave-api-serper"
   export OPENAI_MODEL="gpt-4"
   ```

3. **Configuração de Agentes e Tarefas**:
   Edite os arquivos YAML `agentes.yaml` e `tasks.yaml` para configurar os agentes e suas respectivas tarefas.

4. **Execução do Projeto**:
   Execute o script principal para iniciar o enxame de agentes e produzir o material educacional:

   ```bash
   python main.py
   ```

## Estrutura do Projeto

- `main.py`: Script principal para execução do projeto.
- `agents.yaml`: Configuração dos agentes com seus papéis e metas.
- `tasks.yaml`: Configuração das tarefas a serem delegadas aos agentes.
- `requirements.txt`: Lista de dependências do projeto.
- `README.md`: Documentação do projeto.

## Exemplo de Código

Aqui está um exemplo de como configurar e iniciar o enxame de agentes usando o CrewAI:

```python
import os
import shutil
import yaml
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Configuração das variáveis de ambiente
os.environ["OPENAI_API_KEY"] = "sua-chave-api-openai"
os.environ["SERPER_API_KEY"] = "sua-chave-api-serper"
os.environ["OPENAI_MODEL"] = "gpt-4"

# Função para ler o arquivo YAML
def read_yaml(file_path):
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return {}
    with open(file_path, 'r') as file:
        return yaml.safe_load(file) or {}

# Caminhos dos arquivos YAML
agents_file_path = "agentes.yaml"
tasks_file_path = "tasks.yaml"

# Ler a configuração dos agentes e tarefas
agents_config = read_yaml(agents_file_path)
tasks_config = read_yaml(tasks_file_path)

# Inicializar a ferramenta de pesquisa
search_tool = SerperDevTool()

# Função para criar um agente a partir da configuração
def create_agent(agent_config):
    agent = Agent(
        role=agent_config['role'],
        goal=agent_config['goal'],
        backstory=agent_config['backstory'],
        verbose=agent_config.get('verbose', True),
        allow_delegation=agent_config.get('allow_delegation', False)
    )
    return agent

# Criação dos agentes
agents = [create_agent(agent) for agent in agents_config['agents']]

# Adicionar ferramentas aos agentes conforme necessário
for agent in agents:
    if agent.role in ["Gerente de Educação", "Escritor de Artigos", "Crítico de Aulas"]:
        agent.tools = [search_tool]

# Função para criar uma tarefa a partir da configuração
def create_task(task_config, agents):
    agent_role = task_config['agent']
    agent = next((agent for agent in agents if agent.role == agent_role), None)
    if agent is None:
        print(f"Agente com role '{agent_role}' não encontrado.")
        return None
    task = Task(
        description=task_config['description'],
        expected_output=task_config['expected_output'],
        agent=agent,
        parameters=task_config.get('parameters', {})
    )
    return task

# Criação das tarefas
tasks = [create_task(task, agents) for task in tasks_config['tarefas'] if create_task(task, agents) is not None]

# Instanciar o crew com um processo sequencial
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=2
)

# Iniciar o trabalho do crew
result = crew.kickoff()
print(result)
```

## Contribuição

Sinta-se à vontade para contribuir com este projeto! Abra uma issue para relatar bugs ou sugerir melhorias. Pull requests são bem-vindos.

---

Explore o poder dos agentes generativos e transforme a maneira como você cria materiais educacionais com o CrewAI!
