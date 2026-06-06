# TdR

# 🧠 Multi-Agent LLM System

Sistema multiagent basat en models de llenguatge (LLMs) que utilitza agents especialitzats per generar respostes més completes, fiables i estructurades.

El sistema pot funcionar amb models locals (LM Studio) o models al núvol (OpenAI), i està completament configurable mitjançant fitxers externs.

---

# 🧱 Tecnologies utilitzades

- `pydantic_ai` → sistema d’agents
- `LiteLLM` → connexió amb LLMs
- `asyncio` → execució asíncrona
- `nest_asyncio` → compatibilitat en notebooks
- `logfire` → monitoratge del sistema
- `pathlib` → gestió de fitxers

---

# 🚀 Característiques

- 🤖 Arquitectura multiagent
- 🧠 Tres agents secundaris especialitzats
- 🎯 Agent supervisor que coordina tot el sistema
- ⚙️ Configuració externa (prompts, models i temperatures)
- 🖥️ Compatibilitat amb LM Studio (models locals)
- ☁️ Compatibilitat amb models cloud (OpenAI)
- 💾 Guardat automàtic de resultats
- 📂 Sistema modular i escalable

---

# 🧩 Arquitectura

El sistema està format per quatre agents principals:

## 🔹 Agent Secundari 1
- Genera informació base relacionada amb la pregunta.
- Proporciona respostes detallades i estructurades.

## 🔹 Agent Secundari 2
- Analitza la informació generada.
- Detecta possibles errors, incoherències o limitacions.

## 🔹 Agent Secundari 3
- Proposa aplicacions pràctiques, solucions o perspectives alternatives.
- Complementa la informació aportada pels altres agents.

## 🔹 Agent Supervisor
- Coordina els agents.
- Decideix quan utilitzar cada agent secundari.
- Integra les aportacions dels diferents agents.
- Genera la resposta final.

---

# ⚙️ Funcionament del sistema

1. Es carreguen les preguntes del dataset.
2. L'agent supervisor rep cada pregunta.
3. Pot utilitzar els agents secundaris:
   - Agent Secundari 1
   - Agent Secundari 2
   - Agent Secundari 3
4. Cada agent genera una resposta independent.
5. L'agent supervisor combina les diferents aportacions.
6. Es genera una resposta final.
7. El resultat es guarda automàticament en un fitxer.

---

# 📁 Estructura del projecte

```text
C:\Users\genis\Tdr\Tdr version inicial\
│
├── Config/
│   ├── Prompts/
│   │   ├── agent_secundari_1.txt
│   │   ├── agent_secundari_2.txt
│   │   ├── agent_secundari_3.txt
│   │   └── agent_supervisor.txt
│   │
│   ├── Temperatures/
│   │   └── temperatures.txt
│   │
│   └── Models/
│       └── model.txt
│
├── Dataset/
│   └── QA.txt
│
├── Results/
│   └── (auto-generated results)
│
└── main.py
```

---

# 🧠 Models compatibles

## ☁️ Cloud

- OpenAI GPT models

## 🖥️ Local

- Mistral
- Qwen
- Gemma

**Nota:**
- La llista final de models es decidirà en funció dels recursos disponibles.
- Per gestionar els models localment s'utilitza LM Studio.

---

# ⚙️ Configuració

### Prompts

Cada agent disposa d'un fitxer de configuració que defineix el seu comportament:

- `agent_secundari_1.txt`
- `agent_secundari_2.txt`
- `agent_secundari_3.txt`
- `agent_supervisor.txt`

### Temperatures

Cada agent disposa d'un valor de temperatura configurable al fitxer:

- `Temperatures/temperatures.txt`

Configuració actual:

- Agent Secundari 1: 0.2
- Agent Secundari 2: 0.4
- Agent Secundari 3: 0.7
- Agent Supervisor: 0.3

### Model

El model utilitzat es defineix a:

- `Models/model.txt`

### Dataset

Les preguntes es carreguen des de:

- `Dataset/QA.txt`

### Resultats

Les respostes generades es desen automàticament a:

- `Results/`

---
