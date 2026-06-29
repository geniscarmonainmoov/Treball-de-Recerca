# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:13:07 2026

@author: genis
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:00:44 2026

@author: genis
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:02:00 2026

@author: genis
"""

# -*- coding: utf-8 -*-
"""
Sistema multiagente optimizado (sin overflow de contexto)
"""

import asyncio
import nest_asyncio
from pathlib import Path
from datetime import datetime
import os
import ast
import operator as op
import math
import logfire

from pydantic_ai import Agent
from pydantic_ai_litellm import LiteLLMModel
from ddgs import DDGS

# =====================================================
# CONFIG
# =====================================================
BASE_DIR = Path(__file__).resolve().parent

CONFIG_PATH = BASE_DIR / "Config"
DATASET_PATH = BASE_DIR / "Dataset"
PROMPTS_PATH = CONFIG_PATH / "Prompts"
TEMPERATURES_PATH = CONFIG_PATH / "Temperatures"
MODELS_PATH = CONFIG_PATH / "Models"
RESULTS_PATH = BASE_DIR / "Results"
RESULTS_SINGLE_PATH = BASE_DIR / "Results_single"
RESULTS_PATH.mkdir(exist_ok=True)
RESULTS_SINGLE_PATH.mkdir(exist_ok=True)
RESULTS_PATH.mkdir(exist_ok=True)
RESULTS_SINGLE_TOOLS_PATH = BASE_DIR / "Results_single_tools"
RESULTS_SINGLE_TOOLS_PATH.mkdir(exist_ok=True)
RESULTS_CONSENSUS_PATH = BASE_DIR / "Results_consensus"
RESULTS_CONSENSUS_PATH.mkdir(exist_ok=True)

nest_asyncio.apply()

MAX_AGENT_OUTPUT = 400   # 🔥 FIX PRINCIPAL
# =====================================================
# LOGFIRE
# =====================================================
logfire.configure(token='pylf_v1_eu_WnN5NQRYzN64FRrnM5K1HFTJW4Fqkq8StfGfZnC30z8n')
logfire.instrument_pydantic_ai()
# =====================================================
# LOADERS
# =====================================================
def load_model():
    return (MODELS_PATH / "model.txt").read_text().strip()


def load_all_temperatures():
    temps = {}
    with open(TEMPERATURES_PATH / "temperatures.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.split("=", 1)
                temps[k.strip()] = float(v.strip())
    return temps


def load_temperature(agent_name: str):
    return load_all_temperatures().get(agent_name, 0.2)


def load_prompt(filename: str):
    return (PROMPTS_PATH / filename).read_text(encoding="utf-8")


def load_questions(filename: str):
    qs = []
    with open(DATASET_PATH / filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Q:"):
                qs.append(line[2:].strip())
    return qs

def save_single_result(q, a):
    with open(RESULT_SINGLE_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"PREGUNTA: {q}\n")
        f.write(f"RESPUESTA:\n{a}\n")
        
def save_single_tools_result(q, a):
    with open(RESULT_SINGLE_TOOLS_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"PREGUNTA: {q}\n")
        f.write(f"RESPUESTA:\n{a}\n")     
        
def save_consensus_result(q, report):

    with open(RESULT_CONSENSUS_FILE, "a", encoding="utf-8") as f:

        f.write("\n" + "="*80 + "\n")
        f.write(f"PREGUNTA: {q}\n\n")
        f.write(report)
        f.write("\n")
# =====================================================
# MODEL
# =====================================================
def build_single_results_file():
    model_name = load_model().replace("/", "_").replace(":", "_")
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = RESULTS_SINGLE_PATH / f"results_single_{ts}_{model_name}.txt"

    path.write_text(
        "SINGLE AGENT RUN\n" + "="*80 + "\n",
        encoding="utf-8"
    )
    return path
def build_single_tools_results_file():
    model_name = load_model().replace("/", "_").replace(":", "_")
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = RESULTS_SINGLE_TOOLS_PATH / f"results_single_tools_{ts}_{model_name}.txt"

    path.write_text(
        "SINGLE AGENT WITH TOOLS RUN\n" + "="*80 + "\n",
        encoding="utf-8"
    )
    return path

def build_consensus_results_file():
    model_name = load_model().replace("/", "_").replace(":", "_")
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    path = RESULTS_CONSENSUS_PATH / f"results_consensus_{ts}_{model_name}.txt"

    path.write_text(
        "CONSENSUS ANALYSIS\n" + "="*80 + "\n",
        encoding="utf-8"
    )

    return path


RESULT_CONSENSUS_FILE = build_consensus_results_file()

RESULT_SINGLE_TOOLS_FILE = build_single_tools_results_file()

RESULT_SINGLE_FILE = build_single_results_file()




# =====================================================
# ALMACENAR RESPUESTAS
# =====================================================

single_results = {}
single_tools_results = {}
multi_results = {}





def create_model():
    
    model_name = load_model()

    if model_name.startswith("lmstudio"):
        real_model = model_name.split(":", 1)[1]
        os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
        os.environ["OPENAI_API_KEY"] = "lm-studio"
        return LiteLLMModel("openai/" + real_model)

    return LiteLLMModel(model_name)

# =====================================================
# SAFE CALCULATOR (AGENTE 1)
# =====================================================
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}


def safe_eval(expr: str):
    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return _ALLOWED_OPERATORS[type(node.op)](
                _eval(node.left),
                _eval(node.right),
            )
        if isinstance(node, ast.UnaryOp):
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))
        raise TypeError(node)

    return _eval(ast.parse(expr, mode="eval").body)


async def calculadora_agente(expr: str):
    try:
        return str(safe_eval(expr))
    except Exception as e:
        return f"Error: {e}"

# =====================================================
# INTERNET TOOL (RECORTADO)
# =====================================================
async def buscar_en_internet(query: str):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=2):
                results.append(
                    f"{r.get('title','')}: {r.get('body','')[:120]}"
                )
        return "\n".join(results)[:600]   # 🔥 límite fuerte
    except Exception as e:
        return f"Error búsqueda: {e}"

# =====================================================
# PROMPTS
# =====================================================
def prompt_with_temperature(file, agent_name):
    return f"""
Temperature: {load_temperature(agent_name)}

{load_prompt(file)}
"""

# =====================================================
# RESULT FILE
# =====================================================
def build_results_file():
    model_name = load_model().replace("/", "_").replace(":", "_")
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = RESULTS_PATH / f"results_{ts}_{model_name}.txt"

    path.write_text("MULTIAGENT RUN\n" + "="*80 + "\n", encoding="utf-8")
    return path


RESULT_SINGLE_FILE = build_single_results_file()
RESULT_SINGLE_TOOLS_FILE = build_single_tools_results_file()
RESULT_MULTI_FILE = build_results_file()

# =====================================================
# MODEL INIT
# =====================================================
model = create_model()

# =====================================================
# AGENTES SECUNDARIOS (SIMPLIFICADOS)
# =====================================================


single_agent_tools = Agent(
    model,
    system_prompt=load_prompt("single_agent_tools.txt"),
    tools=[calculadora_agente, buscar_en_internet],
)
single_agent = Agent(
    model,
    system_prompt=load_prompt("single_agent.txt"),
    tools=[calculadora_agente, buscar_en_internet],
)
agent_1 = Agent(
    model,
    system_prompt=prompt_with_temperature("agent_secundari_1.txt", "agent_1"),
    tools=[calculadora_agente, buscar_en_internet],
)

agent_2 = Agent(
    model,
    system_prompt=prompt_with_temperature("agent_secundari_2.txt", "agent_2"),
    tools=[calculadora_agente, buscar_en_internet],
)

agent_3 = Agent(
    model,
    system_prompt=prompt_with_temperature("agent_secundari_3.txt", "agent_3"),
    tools=[calculadora_agente, buscar_en_internet],
)

consensus_agent = Agent(
    model,
    system_prompt="""
Eres un analista especializado en medir el consenso entre respuestas.

Dispones de tres respuestas para una misma pregunta:

1. Single Agent.
2. Single Agent con Tools.
3. Sistema Multiagente.

Debes generar un informe cuantitativo y cualitativo.

Calcula:

- Coincidencia léxica (%)
- Coincidencia sintáctica (%)
- Coincidencia semántica (%)

Clasifica el nivel de consenso:

90-100 % → Muy alto
75-89 % → Alto
50-74 % → Moderado
25-49 % → Bajo
0-24 % → Muy bajo

Genera además:

### Comparación por modelo

Single Agent:
- resumen

Single Agent + Tools:
- resumen

Multiagente:
- resumen

### Diferencias principales

### Conclusión

Devuelve un informe estructurado en Markdown.
"""
)

# =====================================================
# WRAPPERS (🔥 SIN RECURSIVIDAD)
# =====================================================

async def run_single_agent_tools(questions):
    print("\n==============================")
    print("MODO SINGLE AGENT CON TOOLS")
    print("==============================")

    for i, q in enumerate(questions, 1):

        print(f"\nPregunta {i}: {q}")

        try:
            result = await single_agent_tools.run(q)
            answer = str(result.output)

        except Exception as e:
            answer = f"ERROR: {e}"

        print(answer)

        print(answer)

        single_tools_results[q] = answer

        save_single_tools_result(q, answer)(q, answer)
        
async def run_multi_agent(questions):
    print("\n==============================")
    print("MODO MULTI AGENT")
    print("==============================")

    for i, q in enumerate(questions, 1):

        print(f"\nPregunta {i}: {q}")

        supervisor = create_supervisor()

        try:
            result = await supervisor.run(q)
            answer = str(result.output)

        except Exception as e:
            answer = f"ERROR SISTEMA: {e}"

        print(answer)

        print(answer)

        multi_results[q] = answer

        save_multi_result(q, answer)
        
        
async def run_single_agent(questions):
    print("\n==============================")
    print("MODO SINGLE AGENT")
    print("==============================")

    for i, q in enumerate(questions, 1):

        print(f"\nPregunta {i}: {q}")

        try:
            result = await single_agent.run(q)
            answer = str(result.output)

        except Exception as e:
            answer = f"ERROR: {e}"

        print(answer)
        single_results[q] = answer
        
        save_single_result(q, answer)
        save_single_result(q, answer)
        
async def safe_run(agent, question: str):
    """Evita overflow y recorta respuesta agresivamente"""
    r = await agent.run(question)
    text = str(r.output)

    if len(text) > MAX_AGENT_OUTPUT:
        text = text[:MAX_AGENT_OUTPUT] + "\n[TRUNCADO]"

    return text


async def agent_1_tool(q: str):
    return await safe_run(agent_1, q)


async def agent_2_tool(q: str):
    return await safe_run(agent_2, q)


async def agent_3_tool(q: str):
    return await safe_run(agent_3, q)

async def run_consensus_agent(question,
                              single_answer,
                              tools_answer,
                              multi_answer):

    prompt = f"""
PREGUNTA:

{question}


RESPUESTA SINGLE AGENT:

{single_answer}


RESPUESTA SINGLE AGENT + TOOLS:

{tools_answer}


RESPUESTA SISTEMA MULTIAGENTE:

{multi_answer}
"""

    result = await consensus_agent.run(prompt)

    report = str(result.output)

    save_consensus_result(question, report)

    return report

# =====================================================
# SUPERVISOR
# =====================================================
def create_supervisor():
    return Agent(
        model,
        system_prompt=prompt_with_temperature("supervisor_agent.txt", "supervisor"),
        tools=[agent_1_tool, agent_2_tool, agent_3_tool],
    )

# =====================================================
# SAVE
# =====================================================
def save_multi_result(q, a):
    with open(RESULT_MULTI_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"PREGUNTA: {q}\n")
        f.write(f"RESPUESTA:\n{a}\n")

# =====================================================
# MAIN
# =====================================================
async def main():

    print("\nSistema iniciado\n")

    questions = load_questions("QA.txt")

    # 1. Single sin tools
    await run_single_agent(questions)

    print("\n" + "="*80)
    print("FINALIZADO SINGLE AGENT")
    print("="*80)

    # 2. Single con tools (NUEVO)
    await run_single_agent_tools(questions)

    print("\n" + "="*80)
    print("FINALIZADO SINGLE AGENT CON TOOLS")
    print("="*80)

    # 3. Multi-agent
    await run_multi_agent(questions)
    print("\n==============================")
    print("ANÁLISIS DE CONSENSO")
    print("==============================")
    
    for q in questions:
    
        report = await run_consensus_agent(
            q,
            single_results[q],
            single_tools_results[q],
            multi_results[q]
        )
    
        print(report)

    print("\nTodos los experimentos han terminado.")
if __name__ == "__main__":
    asyncio.run(main())