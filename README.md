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
TdR/
│
├── Config/
│   ├── Models/
│   │   └── model.txt
│   ├── Prompts/
│   │   ├── agent_secundari_1.txt
│   │   ├── agent_secundari_2.txt
│   │   ├── agent_secundari_3.txt
│   │   └── supervisor_agent.txt
│   ├── Temperatures/
│   │   └── temperatures.txt
│   └── mode.txt
│
├── Dataset/
│   └── QA.txt
│
├── Results/
├── Results_single/
├── Results_single_tools/
├── Results_consensus/
│
├── requirements.txt
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

**Nota**

- La llista final de models es decidirà en funció dels recursos disponibles.
- Per gestionar els models localment s'utilitza LM Studio.

---

# ⚙️ Configuració

## Prompts

Cada agent disposa d'un fitxer de configuració que defineix el seu comportament:

- `agent_secundari_1.txt`
- `agent_secundari_2.txt`
- `agent_secundari_3.txt`
- `supervisor_agent.txt`

## Temperatures

Cada agent disposa d'un valor de temperatura configurable al fitxer:

`Config/Temperatures/temperatures.txt`

Configuració actual:

- Agent Secundari 1: 0.2
- Agent Secundari 2: 0.4
- Agent Secundari 3: 0.7
- Agent Supervisor: 0.3

## Model

El model utilitzat es defineix a:

`Config/Models/model.txt`

## Dataset

Les preguntes es carreguen des de:

`Dataset/QA.txt`

## Resultats

Les respostes generades es desen automàticament a:

- `Results/`
- `Results_single/`
- `Results_single_tools/`
- `Results_consensus/`

---

# 🚀 Instal·lació

## 1. Clonar el repositori

```bash
git clone https://github.com/geniscarmonainmoov/Treball-de-Recerca.git
cd Treball-de-Recerca
```

## 2. Crear un entorn virtual (opcional però recomanat)

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instal·lar les dependències

```bash
pip install -r requirements.txt
```

---

# ▶️ Execució

## 1. Seleccionar el model

Edita el fitxer:

```
Config/Models/model.txt
```

Exemples:

```
openai/gpt-4.1-mini
```

o bé

```
lmstudio:qwen3-8b
```

## 2. Seleccionar el mode d'execució

Edita:

```
Config/mode.txt
```

Valors possibles:

- `single`
- `single_tools`
- `multi`
- `consensus`
- `all`

## 3. Afegir les preguntes

Edita:

```
Dataset/QA.txt
```

Format:

```
Q: Primera pregunta
Q: Segona pregunta
```

## 4. Executar el programa

```bash
python main.py
```

Els resultats es generaran automàticament a les carpetes corresponents.

---

# 🖥️ Utilitzar LM Studio

Per executar el sistema amb un model local:

1. Instal·la LM Studio.
2. Descarrega el model desitjat.
3. Inicia el servidor **OpenAI Compatible**.
4. Escriu el model a:

```
Config/Models/model.txt
```

Per exemple:

```
lmstudio:qwen3-8b
```

---

# ☁️ Utilitzar OpenAI

Configura la variable d'entorn amb la teva API Key.

### Windows

```bash
set OPENAI_API_KEY=LA_TEVA_API_KEY
```

### Linux / macOS

```bash
export OPENAI_API_KEY=LA_TEVA_API_KEY
```

Després selecciona el model a:

```
Config/Models/model.txt
```

---

# 📦 Dependències

El projecte utilitza les següents llibreries externes:

- pydantic-ai
- pydantic-ai-litellm
- litellm
- logfire
- nest_asyncio
- ddgs
- openai

Les llibreries estàndard de Python (`asyncio`, `pathlib`, `datetime`, `os`, `ast`, `operator` i `time`) no cal incloure-les al fitxer `requirements.txt`, ja que formen part de la instal·lació de Python.

---

# 📁 Portabilitat

El projecte utilitza rutes relatives mitjançant `pathlib`, de manera que es pot executar en qualsevol ordinador sense modificar el codi font.

Només és necessari mantenir la mateixa estructura de carpetes del projecte.
