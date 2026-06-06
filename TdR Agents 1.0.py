# -*- coding: utf-8 -*-
"""
Sistema multiagent
"""

import asyncio
import nest_asyncio
from pathlib import Path
from datetime import datetime
import os

from pydantic_ai import Agent
import logfire
from pydantic_ai_litellm import LiteLLMModel


# =====================================================
# PATHS
# =====================================================
CONFIG_PATH = Path(r"C:\Users\genis\Tdr\Tdr version inicial\Config")
DATASET_PATH = Path(r"C:\Users\genis\Tdr\Tdr version inicial\Dataset")
PROMPTS_PATH = CONFIG_PATH / "Prompts"
TEMPERATURES_PATH = CONFIG_PATH / "Temperatures"
MODELS_PATH = CONFIG_PATH / "Models"
RESULTS_PATH = Path(r"C:\Users\genis\Tdr\Tdr version inicial\Results")

RESULTS_PATH.mkdir(exist_ok=True)


# =====================================================
# LOGFIRE
# =====================================================
logfire.configure(token='YOUR_TOKEN')
logfire.instrument_pydantic_ai()

nest_asyncio.apply()


# =====================================================
# LOADERS
# =====================================================
def load_model() -> str:
    with open(MODELS_PATH / "model.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


def load_all_temperatures():
    file_path = TEMPERATURES_PATH / "temperatures.txt"

    temps = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                temps[k.strip()] = float(v.strip())

    return temps


def load_temperature(agent_name: str) -> float:
    temps = load_all_temperatures()
    return temps.get(agent_name, 0.2)


def load_prompt(filename: str) -> str:
    with open(PROMPTS_PATH / filename, "r", encoding="utf-8") as f:
        return f.read()


def load_questions(filename: str):
    questions = []
    with open(DATASET_PATH / filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Q:"):
                questions.append(line[2:].strip())
    return questions


# =====================================================
# MODEL
# =====================================================
def create_model():
    model_name = load_model()

    if model_name.startswith("lmstudio"):
        real_model = model_name.split(":", 1)[1]

        os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
        os.environ["OPENAI_API_KEY"] = "lm-studio"

        return LiteLLMModel("openai/" + real_model)

    return LiteLLMModel(model_name)


# =====================================================
# PROMPT + TEMPERATURE
# =====================================================
def prompt_with_temperature(prompt_file: str, agent_name: str) -> str:
    prompt = load_prompt(prompt_file)
    temp = load_temperature(agent_name)

    return f"""
[SYSTEM CONFIGURATION]
Temperature: {temp}

IMPORTANT:
- Lower = deterministic
- Higher = creative
- Adapt your behaviour accordingly

{prompt}
"""


# =====================================================
# RESULTS FILE
# =====================================================
def build_results_file():
    model_name = load_model().replace("/", "_").replace(":", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    temps = load_all_temperatures()

    temp_str = "_".join([f"{k}{v}" for k, v in temps.items()])

    path = RESULTS_PATH / f"results_{timestamp}_{model_name}_{temp_str}.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write("MULTIAGENT RUN\n")
        f.write("=" * 80 + "\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Timestamp: {timestamp}\n\n")

        f.write("TEMPERATURES:\n")
        for k, v in temps.items():
            f.write(f"  - {k}: {v}\n")

        f.write("=" * 80 + "\n\n")

    return path


RESULT_FILE = build_results_file()


# =====================================================
# TOOLS (AGENTS INTERNOS)
# =====================================================
async def agent_secundari_1_tool(question: str) -> str:
    agent = Agent(
        create_model(),
        system_prompt=prompt_with_temperature(
            "agent_secundari_1.txt",
            "agent_secundari_1"
        )
    )
    result = await agent.run(question)
    return result.output


async def agent_secundari_2_tool(question: str) -> str:
    agent = Agent(
        create_model(),
        system_prompt=prompt_with_temperature(
            "agent_secundari_2.txt",
            "agent_secundari_2"
        )
    )
    result = await agent.run(question)
    return result.output


async def agent_secundari_3_tool(question: str) -> str:
    agent = Agent(
        create_model(),
        system_prompt=prompt_with_temperature(
            "agent_secundari_3.txt",
            "agent_secundari_3"
        )
    )
    result = await agent.run(question)
    return result.output


# =====================================================
# SUPERVISOR
# =====================================================
supervisor = Agent(
    create_model(),
    system_prompt=prompt_with_temperature(
        "supervisor_agent.txt",
        "supervisor_agent"
    ),
    tools=[
        agent_secundari_1_tool,
        agent_secundari_2_tool,
        agent_secundari_3_tool
    ]
)


# =====================================================
# SAVE RESULTS
# =====================================================
def save_result(question: str, answer: str):
    with open(RESULT_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"PREGUNTA: {question}\n")
        f.write("-" * 80 + "\n")
        f.write(f"RESPUESTA:\n{answer}\n")
        f.write("=" * 80 + "\n")


# =====================================================
# MAIN LOOP
# =====================================================
async def main():
    print("\nSistema multiagente iniciado\n")

    questions = load_questions("QA.txt")

    for i, q in enumerate(questions, 1):

        if not q.strip():
            continue

        print("\n" + "=" * 80)
        print(f"PREGUNTA {i}: {q}")
        print("=" * 80)

        result = await supervisor.run(q)
        answer = result.output

        print("\nRESPUESTA FINAL")
        print("=" * 80)
        print(answer)
        print("=" * 80)

        save_result(q, answer)


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    asyncio.run(main())
