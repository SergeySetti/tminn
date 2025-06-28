# OpenAI Agents Python SDK - Complete Documentation

## Table of Contents
- [Overview](#overview)
- [Why Use the Agents SDK](#why-use-the-agents-sdk)
- [Main Features](#main-features)
- [Installation](#installation)
- [Hello World Example](#hello-world-example)
- [Quickstart Guide](#quickstart-guide)
  - [Create a Project and Virtual Environment](#1-create-a-project-and-virtual-environment)
  - [Activate the Virtual Environment](#2-activate-the-virtual-environment)
  - [Install the Agents SDK](#3-install-the-agents-sdk)
  - [Set an OpenAI API Key](#4-set-an-openai-api-key)
  - [Create Your First Agent](#5-create-your-first-agent)
  - [Add More Agents](#6-add-more-agents)
  - [Define Handoffs](#7-define-handoffs)
  - [Run the Agent Orchestration](#8-run-the-agent-orchestration)
  - [Add a Guardrail](#9-add-a-guardrail)
  - [Complete Example](#10-complete-example)
  - [View Your Traces](#11-view-your-traces)
- [Agents](#agents) 
  - [Agent Properties](#agent-properties)
  - [Dynamic Instructions](#dynamic-instructions)
- [Running Agents](#running-agents)
    - [Basic Usage](#basic-usage)
    - [Agent Execution Loop](#agent-execution-loop)
    - [Run Configuration](#run-configuration)
    - [Multi-turn Conversations](#multi-turn-conversations)
- [Tools](#tools)
  - [Hosted Tools](#1-hosted-tools)
  - [Function Tools](#2-function-tools)
  - [Agents as Tools](#3-agents-as-tools)
  - [Custom Function Tools](#custom-function-tools)
- [Handoffs](#handoffs) 
  - [Basic Handoffs](#basic-handoffs)
  - [Customized Handoffs](#customized-handoffs)
  - [Handoff Parameters](#handoff-parameters)
- [Guardrails](#guardrails)
- [Models](#models)
  - [OpenAI Models](#openai-models)
  - [Non-OpenAI Models via LiteLLM](#non-openai-models-via-litellm)
  - [Model Settings](#model-settings)
  - [Different Models per Agent](#different-models-per-agent)
- [Context Management](#context-management)
  - [Local Context](#local-context)
  - [Agent/LLM Context](#agentllm-context)
- [Model Context Protocol (MCP)](#model-context-protocol-mcp)
  - [MCP Server Types](#mcp-server-types)
  - [Using MCP Servers](#using-mcp-servers)
  - [Caching MCP Tools](#caching-mcp-tools)
- [Tracing](#tracing)
- [Multi-Agent Orchestration](#multi-agent-orchestration)
  - [LLM-Driven Orchestration](#llm-driven-orchestration)
  - [Code-Driven Orchestration](#code-driven-orchestration)
- [Agent Visualization](#agent-visualization)
- [Configuration](#configuration)
  - [Setting API Keys](#setting-api-keys)
  - [Environment Variables](#environment-variables)


## Overview

The OpenAI Agents SDK enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. It's a production-ready upgrade of OpenAI's previous experimentation for agents, Swarm. The Agents SDK has a very small set of primitives:

- **Agents**, which are LLMs equipped with instructions and tools
- **Handoffs**, which allow agents to delegate to other agents for specific tasks  
- **Guardrails**, which enable the inputs to agents to be validated

In combination with Python, these primitives are powerful enough to express complex relationships between tools and agents, and allow you to build real-world applications without a steep learning curve. The SDK comes with built-in tracing that lets you visualize and debug your agentic flows, as well as evaluate them and even fine-tune models for your application.

## Why Use the Agents SDK

The SDK has two driving design principles:

1. **Enough features to be worth using, but few enough primitives to make it quick to learn**
2. **Works great out of the box, but you can customize exactly what happens**

### Main Features

- **Agent loop**: Built-in agent loop that handles calling tools, sending results to the LLM, and looping until the LLM is done
- **Python-first**: Use built-in language features to orchestrate and chain agents, rather than needing to learn new abstractions
- **Handoffs**: A powerful feature to coordinate and delegate between multiple agents
- **Guardrails**: Run input validations and checks in parallel to your agents, breaking early if the checks fail
- **Function tools**: Turn any Python function into a tool, with automatic schema generation and Pydantic-powered validation
- **Tracing**: Built-in tracing that lets you visualize, debug and monitor your workflows, as well as use the OpenAI suite of evaluation, fine-tuning and distillation tools

## Installation

```bash
pip install openai-agents
```

## Hello World Example

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
```

*(If running this, ensure you set the `OPENAI_API_KEY` environment variable)*

---

## Quickstart Guide

### 1. Create a Project and Virtual Environment

You'll only need to do this once:

```bash
mkdir my-agent-project
cd my-agent-project
python -m venv venv
```

### 2. Activate the Virtual Environment

Do this every time you start a new terminal session:

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install the Agents SDK

```bash
pip install openai-agents
```

### 4. Set an OpenAI API Key

If you don't have one, follow [these instructions](https://platform.openai.com/docs/quickstart#create-and-export-an-api-key) to create an OpenAI API key.

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 5. Create Your First Agent

Agents are defined with instructions, a name, and optional config (such as `model_config`):

```python
from agents import Agent

agent = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)
```

### 6. Add More Agents

Additional agents can be defined in the same way. `handoff_descriptions` provide additional context for determining handoff routing:

```python
from agents import Agent

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)
```

### 7. Define Handoffs

On each agent, you can define an inventory of outgoing handoff options that the agent can choose from:

```python
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent]
)
```

### 8. Run the Agent Orchestration

Let's check that the workflow runs and the triage agent correctly routes between the two specialist agents:

```python
from agents import Runner

async def main():
    result = await Runner.run(triage_agent, "What is the capital of France?")
    print(result.final_output)
```

### 9. Add a Guardrail

You can define custom guardrails to run on the input or output:

```python
from agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )
```

### 10. Complete Example

```python
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)
    
    result = await Runner.run(triage_agent, "what is life")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### 11. View Your Traces

To review what happened during your agent run, navigate to the [Trace viewer in the OpenAI Dashboard](https://platform.openai.com/traces) to view traces of your agent runs.

---

## Agents

An agent is an AI model configured with instructions, tools, guardrails, handoffs and more. We strongly recommend passing instructions, which is the "system prompt" for the agent.

### Agent Properties

- **name**: The name of the agent
- **instructions**: The instructions for the agent (system prompt). Can be a string or a function that dynamically generates instructions
- **handoff_description**: A description used when the agent is used as a handoff
- **handoffs**: List of sub-agents that the agent can delegate to
- **tools**: List of tools the agent can use
- **input_guardrails**: List of checks that run in parallel to the agent's execution
- **output_guardrails**: List of checks that run on the final output
- **output_type**: The type of the output object (defaults to str)
- **model**: The model to use for this agent
- **model_config**: Configuration for the model
- **mcp_servers**: List of MCP servers to use with this agent

### Dynamic Instructions

Instructions can be dynamic functions that receive the context:

```python
from agents import Agent, RunContextWrapper

def dynamic_instructions(ctx: RunContextWrapper, agent: Agent) -> str:
    return f"You are helping user {ctx.context.username}. Current time: {ctx.context.current_time}"

agent = Agent(
    name="Dynamic Agent",
    instructions=dynamic_instructions
)
```

---

## Running Agents

You can run agents via the `Runner` class with three options:

1. **`Runner.run()`** - Runs async and returns a `RunResult`
2. **`Runner.run_sync()`** - Sync method that runs `.run()` under the hood
3. **`Runner.run_streamed()`** - Runs async and returns a `RunResultStreaming`

### Basic Usage

```python
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")
    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
```

### Agent Execution Loop

When you run an agent, the following loop executes:

1. Call the LLM for the current agent with the current input
2. The LLM produces its output
3. If the LLM returns a final_output, the loop ends and returns the result
4. If the LLM does a handoff, update the current agent and input, and re-run the loop
5. If the LLM produces tool calls, run those tool calls, append the results, and re-run the loop
6. If max_turns is exceeded, raise a `MaxTurnsExceeded` exception

### Run Configuration

The `run_config` parameter lets you configure global settings:

```python
from agents import RunConfig, Runner

run_config = RunConfig(
    model="gpt-4o",
    model_settings={"temperature": 0.7},
    max_turns=10,
    input_guardrails=[...],
    output_guardrails=[...],
    tracing_disabled=False,
    workflow_name="My Workflow"
)

result = await Runner.run(agent, input, run_config=run_config)
```

### Multi-turn Conversations

```python
async def main():
    agent = Agent(name="Assistant", instructions="Reply very concisely.")
    
    # First turn
    result = await Runner.run(agent, "What city is the Golden Gate Bridge in?")
    print(result.final_output)  # San Francisco
    
    # Second turn
    new_input = result.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
    result = await Runner.run(agent, new_input)
    print(result.final_output)  # California
```

---

## Tools

Tools let agents take actions: things like fetching data, running code, calling external APIs, and even using a computer. There are three classes of tools in the Agent SDK:

### 1. Hosted Tools

These run on LLM servers alongside the AI models. OpenAI offers retrieval, web search and computer use as hosted tools:

```python
from agents import Agent, FileSearchTool, Runner, WebSearchTool

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["VECTOR_STORE_ID"],
        ),
    ],
)
```

### 2. Function Tools

You can use any Python function as a tool with automatic schema generation:

```python
import json
from typing_extensions import TypedDict, Any
from agents import Agent, FunctionTool, RunContextWrapper, function_tool

class Location(TypedDict):
    lat: float
    long: float

@function_tool
async def fetch_weather(location: Location) -> str:
    """Fetch the weather for a given location.
    
    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "sunny"

@function_tool(name_override="fetch_data")
def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
    """Read the contents of a file.
    
    Args:
        path: The path to the file to read.
        directory: The directory to read the file from.
    """
    # In real life, we'd read the file from the file system
    return "<file contents>"

agent = Agent(
    name="Assistant",
    tools=[fetch_weather, read_file],
)
```

### 3. Agents as Tools

You can use agents as tools for orchestration without handoffs:

```python
from agents import Agent, Runner

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
)

french_agent = Agent(
    name="French agent", 
    instructions="You translate the user's message to French",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions="You are a translation agent. You use the tools given to you to translate.",
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french", 
            tool_description="Translate the user's message to French",
        ),
    ],
)
```

### Custom Function Tools

For advanced cases, you can create `FunctionTool` objects directly:

```python
from typing import Any
from pydantic import BaseModel
from agents import RunContextWrapper, FunctionTool

class FunctionArgs(BaseModel):
    username: str
    age: int

async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return f"{parsed.username} is {parsed.age} years old"

tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)
```

---

## Handoffs

Handoffs allow an agent to delegate tasks to another agent. This is particularly useful in scenarios where different agents specialize in distinct areas.

### Basic Handoffs

```python
from agents import Agent, handoff

billing_agent = Agent(name="Billing agent")
refund_agent = Agent(name="Refund agent")

triage_agent = Agent(
    name="Triage agent", 
    handoffs=[billing_agent, handoff(refund_agent)]
)
```

### Customized Handoffs

The `handoff()` function lets you customize the handoff behavior:

```python
from agents import Agent, handoff

billing_agent = Agent(name="Billing agent")

custom_handoff = handoff(
    agent=billing_agent,
    tool_name_override="handle_billing_query",
    tool_description_override="Handle billing and payment related questions",
    on_handoff=my_callback_function,
    input_type=BillingHandoffInput
)
```

### Handoff Parameters

- **agent**: The agent to hand off to
- **tool_name_override**: Custom tool name (default: `transfer_to_<agent_name>`)
- **tool_description_override**: Custom tool description  
- **on_handoff**: Callback function executed when handoff is invoked
- **input_type**: Controls the input data passed to the callback

---

## Guardrails

Guardrails are checks that run on inputs or outputs to validate and control agent behavior.

### Input Guardrails

Input guardrails run in parallel to the agent's execution and can halt execution if conditions aren't met:

```python
from agents import Agent, InputGuardrail, GuardrailFunctionOutput
from pydantic import BaseModel

class SafetyCheck(BaseModel):
    is_safe: bool
    reasoning: str

safety_agent = Agent(
    name="Safety Check",
    instructions="Check if the input is safe and appropriate.",
    output_type=SafetyCheck,
)

async def safety_guardrail(ctx, agent, input_data):
    result = await Runner.run(safety_agent, input_data, context=ctx.context)
    safety_output = result.final_output_as(SafetyCheck)
    
    return GuardrailFunctionOutput(
        output_info=safety_output,
        tripwire_triggered=not safety_output.is_safe,
    )

agent = Agent(
    name="Main Agent",
    instructions="You are a helpful assistant",
    input_guardrails=[
        InputGuardrail(guardrail_function=safety_guardrail)
    ]
)
```

### Output Guardrails

Output guardrails check the final output of an agent:

```python
from agents import OutputGuardrail

async def output_quality_check(ctx, agent, output):
    # Check output quality and return GuardrailFunctionOutput
    return GuardrailFunctionOutput(
        output_info={"quality_score": 0.95},
        tripwire_triggered=False,
    )

agent = Agent(
    name="Content Generator",
    output_guardrails=[
        OutputGuardrail(guardrail_function=output_quality_check)
    ]
)
```

### Guardrail Decorators

You can use decorators to create guardrails:

```python
from agents import input_guardrail, output_guardrail

@input_guardrail()
async def check_input_safety(ctx, agent, input_data):
    # Implementation here
    pass

@output_guardrail()
async def check_output_quality(ctx, agent, output):
    # Implementation here  
    pass
```

---

## Models

The Agents SDK supports multiple model providers and configurations.

### OpenAI Models

Two flavors of OpenAI model support:

1. **OpenAIResponsesModel** - Uses the Responses API (recommended)
2. **OpenAIChatCompletionsModel** - Uses the Chat Completions API

```python
from agents import Agent, OpenAIResponsesModel, OpenAIChatCompletionsModel

# Using model name directly
agent1 = Agent(model="gpt-4o", ...)

# Using specific model configuration
agent2 = Agent(
    model=OpenAIResponsesModel(model="gpt-4o"),
    ...
)
```

### Non-OpenAI Models via LiteLLM

Install the LiteLLM dependency:

```bash
pip install openai-agents[litellm]
```

Use other models:

```python
claude_agent = Agent(model="litellm/anthropic/claude-3-5-sonnet-20240620", ...)
gemini_agent = Agent(model="litellm/gemini/gemini-2.5-flash-preview-04-17", ...)
```

### Model Settings

Configure model parameters:

```python
from agents import Agent, ModelSettings

agent = Agent(
    name="Assistant",
    model="gpt-4o",
    model_config=ModelSettings(
        temperature=0.7,
        top_p=0.9,
        max_tokens=1000,
        frequency_penalty=0.1,
        presence_penalty=0.1
    )
)
```

### Different Models per Agent

```python
spanish_agent = Agent(
    name="Spanish agent",
    model="o3-mini",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    model=OpenAIChatCompletionsModel(model="gpt-4o"),
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    model="gpt-3.5-turbo",
    handoffs=[spanish_agent, english_agent],
)
```

---

## Context Management

Context refers to data available to your code and to LLMs during agent execution.

### Local Context

Local context is data available to your tool functions, callbacks, and lifecycle hooks:

```python
import asyncio
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    user_info = UserInfo(name="John", uid=123)
    
    agent = Agent[UserInfo](
        name="Assistant",
        tools=[fetch_user_age],
    )
    
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )
    print(result.final_output)  # The user John is 47 years old.
```

### Agent/LLM Context

To make data available to the LLM, you can:

1. **Add to Agent instructions** (system prompt):
   ```python
   def dynamic_instructions(ctx: RunContextWrapper, agent: Agent) -> str:
       return f"You are helping {ctx.context.username}. Current time: {datetime.now()}"
   
   agent = Agent(instructions=dynamic_instructions)
   ```

2. **Add to input when calling Runner.run**:
   ```python
   input_with_context = f"User context: {user_data}\n\nUser question: {user_question}"
   result = await Runner.run(agent, input_with_context)
   ```

3. **Expose via function tools** for on-demand context:
   ```python
   @function_tool
   async def get_user_preferences(ctx: RunContextWrapper) -> str:
       return f"User preferences: {ctx.context.preferences}"
   ```

4. **Use retrieval or web search tools** for grounding responses

---

## Model Context Protocol (MCP)

The Model Context Protocol (MCP) is a standardized way to provide tools and context to LLMs. Think of MCP like a USB-C port for AI applications.

### MCP Server Types

1. **stdio servers** - Run as subprocesses locally
2. **HTTP over SSE servers** - Run remotely via URL

### Using MCP Servers

```python
from agents import Agent, MCPServerStdio, MCPServerSse

# stdio server example
async with MCPServerStdio(
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    }
) as server:
    tools = await server.list_tools()
    
    agent = Agent(
        name="Assistant", 
        instructions="Use the tools to achieve the task",
        mcp_servers=[server]
    )
```

### Caching MCP Tools

For performance, you can cache the tool list:

```python
server = MCPServerStdio(
    params={...},
    cache_tools_list=True  # Cache tools for better performance
)

# Invalidate cache when needed
server.invalidate_tools_cache()
```

---

## Tracing

The Agents SDK includes built-in tracing that collects comprehensive records of events during agent runs: LLM generations, tool calls, handoffs, guardrails, and custom events.

### Default Tracing

Tracing is enabled by default. View traces in the [OpenAI Dashboard](https://platform.openai.com/traces).

### Disabling Tracing

Two ways to disable tracing:

1. **Globally**: Set environment variable `OPENAI_AGENTS_DISABLE_TRACING=1`
2. **Per run**: Set `RunConfig.tracing_disabled=True`

### Custom Tracing

```python
from agents import Agent, Runner, trace

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes.")
    
    with trace("Joke workflow"):
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}")
        
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")
```

### Trace Configuration

```python
from agents import RunConfig

run_config = RunConfig(
    workflow_name="My Custom Workflow",
    trace_id="unique-trace-id",
    group_id="conversation-group",
    trace_metadata={"user_id": "123", "session": "abc"},
    trace_include_sensitive_data=False
)
```

---

## Multi-Agent Orchestration

There are two main ways to orchestrate agents:

### 1. LLM-Driven Orchestration

Allow the LLM to make decisions about agent flow:

```python
# Agents can decide which other agents to call based on context
coordinator = Agent(
    name="Coordinator",
    instructions="Analyze the task and delegate to appropriate specialists",
    handoffs=[research_agent, analysis_agent, writing_agent]
)
```

**Best Practices:**
- Use specialized agents that excel in one task
- Allow agents to introspect and improve
- Invest in evaluations to train agents
- Provide clear handoff descriptions

### 2. Code-Driven Orchestration

Determine agent flow via your code for more deterministic behavior:

```python
# Sequential processing
research_result = await Runner.run(research_agent, task)
analysis_result = await Runner.run(analysis_agent, research_result.final_output)
final_result = await Runner.run(writing_agent, analysis_result.final_output)

# Parallel processing
import asyncio
results = await asyncio.gather(
    Runner.run(agent1, task),
    Runner.run(agent2, task),
    Runner.run(agent3, task)
)

# Conditional logic
if task_type == "research":
    result = await Runner.run(research_agent, task)
elif task_type == "analysis":
    result = await Runner.run(analysis_agent, task)
```

**Common Patterns:**
- Using structured outputs for classification
- Chaining agents by transforming outputs
- Feedback loops with evaluator agents
- Parallel execution for independent tasks

---

## Agent Visualization

Generate visual representations of agent relationships using Graphviz:

```python
from agents import Agent, function_tool
from agents.extensions.visualization import draw_graph

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

spanish_agent = Agent(name="Spanish agent", instructions="You only speak Spanish.")
english_agent = Agent(name="English agent", instructions="You only speak English")

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on language.",
    handoffs=[spanish_agent, english_agent],
    tools=[get_weather],
)

draw_graph(triage_agent)
```

This generates a graph showing:
- **Agents** as yellow rectangles
- **Tools** as green ellipses  
- **Handoffs** as directed edges
- **Start node** indicating entry point

---

## Configuration

### Setting API Keys

```python
from agents import set_default_openai_key, set_default_openai_client
from openai import AsyncOpenAI

# Method 1: Set API key directly
set_default_openai_key("your-api-key")

# Method 2: Set custom client
client = AsyncOpenAI(api_key="your-key", base_url="https://custom-endpoint")
set_default_openai_client(client)
```

### Environment Variables

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_AGENTS_DISABLE_TRACING=1  # Disable tracing globally
```

---

## Exceptions

The SDK raises specific exceptions for different error conditions:

- **`AgentsException`** - Base class for all SDK exceptions
- **`MaxTurnsExceeded`** - Raised when run exceeds max_turns
- **`ModelBehaviorError`** - Raised when model produces invalid outputs
- **`UserError`** - Raised when there's an error in SDK usage
- **`InputGuardrailTripwireTriggered`** - Raised when input guardrail fails
- **`OutputGuardrailTripwireTriggered`** - Raised when output guardrail fails

```python
from agents import Runner, MaxTurnsExceeded, ModelBehaviorError
from agents.exceptions import InputGuardrailTripwireTriggered

try:
    result = await Runner.run(agent, input, max_turns=5)
except MaxTurnsExceeded:
    print("Agent exceeded maximum turns")
except InputGuardrailTripwireTriggered as e:
    print(f"Input guardrail triggered: {e.guardrail_result}")
except ModelBehaviorError as e:
    print(f"Model behavior error: {e}")
```

---

## Examples and Resources

### Example Categories

The SDK includes comprehensive examples in the [examples section of the repo](https://github.com/openai/openai-agents-python/tree/main/examples):

- **agent_patterns**: Common agent design patterns
- **tool_examples**: OAI hosted tools like web search and file search integration
- **model_providers**: Using non-OpenAI models with the SDK
- **handoffs**: Practical examples of agent handoffs
- **mcp**: Model Context Protocol integration examples
- **customer_service** and **research_bot**: Real-world application examples

### Key Example Use Cases

#### Customer Service Bot
Multi-agent system with specialized agents for different support areas:
- Triage agent routes to appropriate specialists
- Order status agent handles shipping inquiries
- Refund agent processes return requests
- FAQ agent answers common questions

#### Research Assistant
Collaborative research workflow:
- Research agent gathers information
- Analysis agent processes findings
- Writing agent creates reports
- Review agent provides feedback and iteration

#### Multi-language Support
Language-aware routing system:
- Detection agent identifies user language
- Specialized agents for each language
- Translation tools for cross-language communication

---

## Advanced Features

### Structured Outputs

Use Pydantic models for structured agent outputs:

```python
from pydantic import BaseModel
from agents import Agent

class AnalysisResult(BaseModel):
    sentiment: str
    confidence: float
    key_topics: list[str]
    summary: str

analysis_agent = Agent(
    name="Text Analyzer",
    instructions="Analyze the given text for sentiment, topics, and provide a summary",
    output_type=AnalysisResult
)

result = await Runner.run(analysis_agent, "Your text here")
analysis = result.final_output_as(AnalysisResult)
print(f"Sentiment: {analysis.sentiment}")
print(f"Confidence: {analysis.confidence}")
```

### Streaming Responses

Get real-time streaming of agent responses:

```python
from agents import Runner

async def stream_example():
    agent = Agent(name="Writer", instructions="Write engaging content")
    
    async for chunk in Runner.run_streamed(agent, "Write a story about AI"):
        if chunk.final_output:
            print(chunk.final_output, end="", flush=True)
        elif chunk.tool_calls:
            print(f"\n[Tool call: {chunk.tool_calls[0].function.name}]")
```

### Custom Model Providers

Integrate any LLM provider:

```python
from agents import ModelProvider, Model

class CustomModelProvider(ModelProvider):
    def get_model(self, model_name: str) -> Model:
        if model_name == "my-custom-model":
            return MyCustomModel(...)
        raise ValueError(f"Unknown model: {model_name}")

# Use with RunConfig
run_config = RunConfig(model_provider=CustomModelProvider())
result = await Runner.run(agent, input, run_config=run_config)
```

### Lifecycle Hooks

Add custom behavior at different points in the agent lifecycle:

```python
from agents import Agent

class CustomAgent(Agent):
    async def on_before_llm_call(self, context, messages):
        # Custom logic before LLM call
        print(f"About to call LLM with {len(messages)} messages")
        return messages
    
    async def on_after_llm_call(self, context, response):
        # Custom logic after LLM call
        print(f"LLM returned: {response}")
        return response
```

### Error Handling and Retries

Implement robust error handling:

```python
import asyncio
from agents import Runner, ModelBehaviorError

async def run_with_retry(agent, input, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await Runner.run(agent, input)
        except ModelBehaviorError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Batch Processing

Process multiple inputs efficiently:

```python
import asyncio
from agents import Runner

async def batch_process(agent, inputs):
    tasks = [Runner.run(agent, input) for input in inputs]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful_results = []
    failed_results = []
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            failed_results.append((inputs[i], result))
        else:
            successful_results.append((inputs[i], result))
    
    return successful_results, failed_results
```

---

## Performance Optimization

### Best Practices

#### Model Selection
- Use smaller, faster models for simple tasks (triage, classification)
- Reserve larger models for complex reasoning tasks
- Consider cost vs. performance tradeoffs

#### Caching Strategies
```python
from functools import lru_cache

@lru_cache(maxsize=128)
@function_tool
def expensive_computation(data: str) -> str:
    # Cache results of expensive operations
    return perform_computation(data)
```

#### Parallel Execution
```python
import asyncio

# Run independent agents in parallel
async def parallel_workflow(task):
    research_task = Runner.run(research_agent, task)
    validation_task = Runner.run(validation_agent, task)
    
    research_result, validation_result = await asyncio.gather(
        research_task, validation_task
    )
    
    # Combine results
    final_input = f"Research: {research_result.final_output}\nValidation: {validation_result.final_output}"
    return await Runner.run(synthesis_agent, final_input)
```

#### Memory Management
```python
from agents import RunConfig

# Limit context window for long conversations
run_config = RunConfig(
    model_settings={
        "max_tokens": 4000,
        "truncation": "auto"  # Automatically truncate long contexts
    }
)
```

---

## Security Considerations

### Input Validation

Always validate inputs before processing:

```python
import re
from agents import InputGuardrail, GuardrailFunctionOutput

async def input_sanitization_guardrail(ctx, agent, input_data):
    # Check for potentially malicious patterns
    dangerous_patterns = [
        r"<script",
        r"javascript:",
        r"data:text/html",
        # Add more patterns as needed
    ]
    
    input_str = str(input_data)
    for pattern in dangerous_patterns:
        if re.search(pattern, input_str, re.IGNORECASE):
            return GuardrailFunctionOutput(
                output_info={"blocked_pattern": pattern},
                tripwire_triggered=True
            )
    
    return GuardrailFunctionOutput(tripwire_triggered=False)
```

### Output Filtering

Filter sensitive information from outputs:

```python
async def output_filter_guardrail(ctx, agent, output):
    # Remove sensitive patterns like emails, phone numbers, SSNs
    sensitive_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b\d{3}-\d{3}-\d{4}\b',  # Phone
    ]
    
    filtered_output = str(output)
    for pattern in sensitive_patterns:
        filtered_output = re.sub(pattern, "[REDACTED]", filtered_output)
    
    if filtered_output != str(output):
        return GuardrailFunctionOutput(
            output_info={"filtered": True},
            tripwire_triggered=False
        )
    
    return GuardrailFunctionOutput(tripwire_triggered=False)
```

### Rate Limiting

Implement rate limiting for production use:

```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        user_requests = self.requests[user_id]
        
        # Remove old requests
        user_requests[:] = [req_time for req_time in user_requests 
                           if now - req_time < self.window_seconds]
        
        if len(user_requests) >= self.max_requests:
            return False
        
        user_requests.append(now)
        return True

rate_limiter = RateLimiter()

async def rate_limited_guardrail(ctx, agent, input_data):
    user_id = ctx.context.user_id if hasattr(ctx.context, 'user_id') else "anonymous"
    
    if not rate_limiter.is_allowed(user_id):
        return GuardrailFunctionOutput(
            output_info={"reason": "rate_limit_exceeded"},
            tripwire_triggered=True
        )
    
    return GuardrailFunctionOutput(tripwire_triggered=False)
```

---

## Testing and Evaluation

### Unit Testing Agents

```python
import pytest
from agents import Agent, Runner

@pytest.mark.asyncio
async def test_math_agent():
    agent = Agent(
        name="Math Tutor",
        instructions="Solve math problems step by step"
    )
    
    result = await Runner.run(agent, "What is 2 + 2?")
    
    assert "4" in result.final_output
    assert result.final_output is not None

@pytest.mark.asyncio
async def test_agent_with_tools():
    @function_tool
    def calculator(expression: str) -> str:
        return str(eval(expression))  # Don't use eval in production!
    
    agent = Agent(
        name="Calculator Agent",
        tools=[calculator],
        instructions="Use the calculator tool for math"
    )
    
    result = await Runner.run(agent, "Calculate 15 * 23")
    assert "345" in result.final_output
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_multi_agent_workflow():
    research_agent = Agent(name="Researcher", instructions="Research topics")
    writer_agent = Agent(name="Writer", instructions="Write summaries")
    
    triage_agent = Agent(
        name="Coordinator",
        instructions="Coordinate research and writing",
        handoffs=[research_agent, writer_agent]
    )
    
    result = await Runner.run(triage_agent, "Research and write about AI")
    
    assert result.final_output is not None
    assert len(result.agent_runs) > 1  # Multiple agents ran
```

### Evaluation Metrics

```python
from agents import Runner, trace
import json

class AgentEvaluator:
    def __init__(self):
        self.results = []
    
    async def evaluate_response_quality(self, agent, test_cases):
        for case in test_cases:
            with trace(f"Evaluation-{case['id']}"):
                result = await Runner.run(agent, case['input'])
                
                evaluation = {
                    'case_id': case['id'],
                    'input': case['input'],
                    'expected': case['expected'],
                    'actual': result.final_output,
                    'score': self._calculate_score(case['expected'], result.final_output)
                }
                
                self.results.append(evaluation)
        
        return self.results
    
    def _calculate_score(self, expected, actual):
        # Implement your scoring logic
        # Could use semantic similarity, exact match, etc.
        return 0.85  # Placeholder
```

---

## Deployment Patterns

### Production Configuration

```python
from agents import Agent, Runner, RunConfig, set_default_openai_client
from openai import AsyncOpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Production client configuration
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0,
    max_retries=3
)
set_default_openai_client(client)

# Production run configuration
production_config = RunConfig(
    max_turns=10,
    tracing_disabled=False,  # Keep tracing for monitoring
    trace_include_sensitive_data=False,  # Exclude sensitive data
    workflow_name="production-workflow"
)

class ProductionAgentService:
    def __init__(self):
        self.agent = Agent(
            name="Production Assistant",
            instructions="You are a helpful production assistant",
            input_guardrails=[security_guardrail],
            output_guardrails=[content_filter_guardrail]
        )
    
    async def process_request(self, user_input: str, user_context: dict):
        try:
            result = await Runner.run(
                self.agent,
                user_input,
                context=user_context,
                run_config=production_config
            )
            
            logger.info(f"Successfully processed request for user {user_context.get('user_id')}")
            return result.final_output
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            raise
```

### Monitoring and Observability

```python
import time
from agents import trace

class AgentMonitor:
    def __init__(self):
        self.metrics = {
            'request_count': 0,
            'success_count': 0,
            'error_count': 0,
            'avg_response_time': 0
        }
    
    async def monitored_run(self, agent, input_data):
        start_time = time.time()
        self.metrics['request_count'] += 1
        
        try:
            with trace("monitored-agent-run", trace_metadata={"timestamp": start_time}):
                result = await Runner.run(agent, input_data)
                
            self.metrics['success_count'] += 1
            response_time = time.time() - start_time
            self._update_avg_response_time(response_time)
            
            return result
            
        except Exception as e:
            self.metrics['error_count'] += 1
            logger.error(f"Agent run failed: {e}")
            raise
    
    def _update_avg_response_time(self, new_time):
        # Simple moving average
        current_avg = self.metrics['avg_response_time']
        count = self.metrics['success_count']
        self.metrics['avg_response_time'] = ((current_avg * (count - 1)) + new_time) / count

monitor = AgentMonitor()
```

---

## Migration and Upgrade Guide

### From Swarm to Agents SDK

The Agents SDK is the production-ready successor to Swarm. Key differences:

#### Migration Checklist

1. **Update imports**:
   ```python
   # Old (Swarm)
   from swarm import Agent, Swarm
   
   # New (Agents SDK)
   from agents import Agent, Runner
   ```

2. **Update execution**:
   ```python
   # Old
   client = Swarm()
   response = client.run(agent, messages)
   
   # New
   result = await Runner.run(agent, input)
   ```

3. **Update tool definitions**:
   ```python
   # Old
   def my_tool():
       return "result"
   
   agent = Agent(functions=[my_tool])
   
   # New
   @function_tool
   def my_tool() -> str:
       return "result"
   
   agent = Agent(tools=[my_tool])
   ```

4. **Update handoffs**:
   ```python
   # Old
   def transfer_to_agent():
       return other_agent
   
   # New
   agent = Agent(handoffs=[other_agent])
   ```

#### New Features in Agents SDK

- **Guardrails**: Input/output validation
- **Structured outputs**: Pydantic model support
- **Enhanced tracing**: Built-in observability
- **MCP support**: Standardized tool protocol
- **Better error handling**: Specific exception types
- **Production features**: Rate limiting, monitoring hooks

---

## Troubleshooting

### Common Issues

#### Authentication Errors
```python
# Issue: OpenAI API key not set
# Solution: Set the environment variable or use set_default_openai_key()
import os
from agents import set_default_openai_key

if not os.getenv("OPENAI_API_KEY"):
    set_default_openai_key("your-api-key-here")
```

#### Tool Call Failures
```python
# Issue: Tools not being called correctly
# Solution: Check tool schema and error handling

@function_tool
def problematic_tool(data: dict) -> str:
    try:
        # Your tool logic here
        return "success"
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return f"Tool failed with error: {str(e)}"

# Or use custom error handling
@function_tool(failure_error_function=custom_error_handler)
def better_tool(data: dict) -> str:
    # Tool implementation
    pass
```

#### Memory Issues with Long Conversations
```python
# Issue: Context window exceeded
# Solution: Use truncation or context management

run_config = RunConfig(
    model_settings={
        "max_tokens": 4000,
        "truncation": "auto"
    }
)

# Or manually manage context
def truncate_conversation(messages, max_length=10):
    if len(messages) > max_length:
        # Keep system message and recent messages
        return [messages[0]] + messages[-(max_length-1):]
    return messages
```

#### Performance Issues
```python
# Issue: Slow response times
# Solutions:

# 1. Use parallel execution where possible
async def parallel_agents():
    tasks = [Runner.run(agent1, input1), Runner.run(agent2, input2)]
    results = await asyncio.gather(*tasks)

# 2. Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_function(param):
    # Expensive computation
    pass

# 3. Use smaller models for simple tasks
fast_agent = Agent(model="gpt-3.5-turbo", ...)
complex_agent = Agent(model="gpt-4o", ...)
```

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("agents")

# Add custom debug information
with trace("debug-session", trace_metadata={"debug_mode": True}):
    result = await Runner.run(agent, input)
```

---

## Appendix

### Complete API Reference

For detailed API documentation, refer to the [official documentation](https://openai.github.io/openai-agents-python/ref/).

### Supported Python Versions

- Python 3.8+
- AsyncIO support required
- Pydantic 2.0+ for model validation

### Dependencies

Core dependencies:
- `openai` - OpenAI API client
- `pydantic` - Data validation
- `typing-extensions` - Type hints

Optional dependencies:
- `litellm` - Non-OpenAI model support
- `graphviz` - Agent visualization
- `griffe` - Docstring parsing

### Community and Support

- **GitHub Repository**: [openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- **Documentation**: [openai.github.io/openai-agents-python](https://openai.github.io/openai-agents-python/)
- **OpenAI Platform**: [platform.openai.com](https://platform.openai.com/)
- **Trace Dashboard**: [platform.openai.com/traces](https://platform.openai.com/traces)

---

This comprehensive documentation covers all aspects of the OpenAI Agents Python SDK, from basic usage to advanced production patterns. The SDK's design philosophy of simplicity with power makes it suitable for both rapid prototyping and production deployments.
