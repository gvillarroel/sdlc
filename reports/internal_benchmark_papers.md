# Papers Para Benchmarks Internos De Harnesses

Fecha: 2026-07-07

## Lectura Prioritaria

Si el objetivo es construir benchmarks internos organizacionales para harnesses de agentes, estos son los papers que conviene leer primero:

| Prioridad | Paper | Por que importa |
|---:|---|---|
| 1 | [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) | Define el patron issue-to-patch con repos reales, tests y evaluacion por parche. Es el punto de partida natural para tareas internas de software. |
| 2 | [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) | Muestra que el harness/interfaz cambia el rendimiento, no solo el modelo. Directamente relevante para comparar harnesses. |
| 3 | [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741) | Describe una plataforma con sandbox, herramientas, agentes y benchmarks integrados. Util para disenar arquitectura de harness. |
| 4 | [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](https://arxiv.org/abs/2601.11868) | Buen modelo para tareas realistas en terminal, con entorno unico, solucion humana y tests amplios. |
| 5 | [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://arxiv.org/abs/2412.14161) | Muy cercano a benchmarks organizacionales: simula una empresa de software con sitios internos, datos y tareas de trabajo. |
| 6 | [WorkArena: How Capable are Web Agents at Solving Common Knowledge Work Tasks?](https://arxiv.org/abs/2403.07718) | Sirve para pensar tareas internas sobre software empresarial, workflows web y entornos de knowledge work. |
| 7 | [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854) | Buen ejemplo de entorno reproducible, self-hosted, realista y funcional para agentes web. |
| 8 | [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) | Marco general para evaluar agentes en varios entornos interactivos; util para taxonomia y comparabilidad. |
| 9 | [Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110) | Aporta el enfoque de escenarios + multiples metricas, no un unico score. Muy aplicable a benchmarks internos. |
| 10 | [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](https://arxiv.org/abs/2604.01437) | Enfatiza trazas Thought-Action-Result, datos de interaccion y reproducibilidad en evaluaciones de agentic SE. |
| 11 | [The SWE-Bench Illusion: When State-of-the-Art LLMs Remember](https://arxiv.org/abs/2506.12286) | Relevante para leakage/contaminacion: refuerza la necesidad de benchmarks privados y holdouts internos. |
| 12 | [Benchmark Data Contamination of Large Language Models: A Survey](https://arxiv.org/abs/2406.04244) | Survey para disenar controles contra contaminacion, leakage y sobreajuste a benchmarks publicos. |

## Coding Agents Y Software Engineering

| Paper | Ano | Idea reutilizable | Aplicacion para benchmark interno |
|---|---:|---|---|
| [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374) | 2021 | HumanEval populariza evaluacion por tests funcionales y pass@k. | Usar tests ejecutables como minimo, pero no quedarse en problemas toy ni single-file. |
| [RepoBench: Benchmarking Repository-Level Code Auto-Completion Systems](https://arxiv.org/abs/2306.03091) | 2023 | Evalua capacidades repository-level: retrieval, completion y pipeline. | Incluir tareas que obliguen a navegar multiples archivos y convenciones internas. |
| [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) | 2023 | Tareas desde issues y PRs reales; scoring por tests. | Convertir tickets/PRs internos en casos reproducibles con start commit, prompt y grader. |
| [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) | 2024 | La agent-computer interface afecta navegacion, edicion y test execution. | Evaluar harness + modelo + herramientas como sistema, no solo el modelo. |
| [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741) | 2024 | Plataforma abierta con agentes, CLI, web, sandbox y benchmarks. | Inspirar adapter lifecycle, sandboxing, logs y comparacion multi-harness. |
| [The OpenHands Software Agent SDK: A Composable and ...](https://arxiv.org/html/2511.03690v1) | 2025 | SDK para agentes de software con flexibilidad, ejecucion segura e interfaces. | Referencia para contratos de harness y componentes reutilizables. |
| [Benchmarking AI Coding Agents on End-to-End Project Development](https://arxiv.org/html/2602.01655v1) | 2026 | Propone evaluacion end-to-end con feedback diagnostico y code review. | Agregar revision de mantenibilidad y calidad de PR, no solo tests. |
| [Code Review Agent Benchmark](https://arxiv.org/html/2603.23448v3) | 2026 | Evalua agentes de code review comerciales y open-source. | Crear sub-suite para revisar PRs internos, detectar bugs y medir falsos positivos. |
| [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](https://arxiv.org/abs/2604.01437) | 2026 | Recomienda publicar o conservar trayectorias Thought-Action-Result e interacciones LLM. | Exigir trazas, comandos, tool calls, prompts, parches y resultados como artefactos. |

## Benchmarks De Agentes En Entornos Realistas

| Paper | Ano | Idea reutilizable | Aplicacion para benchmark interno |
|---|---:|---|---|
| [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854) | 2023 | Entorno web reproducible con sitios funcionales y datos realistas. | Crear entornos internos self-hosted que imiten herramientas corporativas. |
| [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) | 2023 | Ocho entornos interactivos para evaluar razonamiento y decision multi-turn. | Clasificar benchmarks internos por entorno: repo, CLI, web, API, ticketing, CI. |
| [GAIA: a benchmark for General AI Assistants](https://arxiv.org/abs/2311.12983) | 2023 | Preguntas simples para humanos pero dificiles para asistentes con herramientas. | Disenar tareas que midan robustez practica, no dificultad artificial. |
| [WorkArena: How Capable are Web Agents at Solving Common Knowledge Work Tasks?](https://arxiv.org/abs/2403.07718) | 2024 | Tareas de enterprise software sobre ServiceNow y BrowserGym. | Modelar workflows organizacionales reales: tickets, aprobaciones, listas, formularios. |
| [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](https://arxiv.org/abs/2404.07972) | 2024 | Tasks de escritorio reales con setup y evaluation scripts. | Si el harness controla GUI/desktop, usar inicializacion y verificacion por estado del sistema. |
| [AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents](https://arxiv.org/abs/2405.14573) | 2024 | Tareas dinamicas parametrizadas con init, success check y teardown. | Parametrizar tareas internas para reducir memorizacion y medir robustez por variaciones. |
| [$\\tau$-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | 2024 | Simula usuario + herramientas + politicas de dominio; mide estado final de DB. | Para agentes con usuarios, evaluar consistencia, policy-following y efectos en base de datos. |
| [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://arxiv.org/abs/2412.14161) | 2024 | Empresa simulada con web, codigo, programas y comunicacion entre coworkers. | Plantilla conceptual para un benchmark organizacional privado. |
| [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](https://arxiv.org/abs/2601.11868) | 2026 | Tareas CLI realistas con entornos unicos, solucion humana y tests. | Excelente referencia para harnesses que operan en shell, CI y repos. |

## Tool Use, Function Calling Y API Harnesses

| Paper/Recurso | Ano | Idea reutilizable | Aplicacion para benchmark interno |
|---|---:|---|---|
| [ToolBench](https://arxiv.org/abs/2305.16504) | 2023 | Evalua manipulacion de herramientas/API en tareas reales. | Medir seleccion de herramientas, argumentos correctos y composicion multi-tool. |
| [The Berkeley Function Calling Leaderboard: From Tool Use to Agentic Evaluation](https://openreview.net/forum?id=2GmDdhBdDk) | 2024 | Evalua AST accuracy, executable accuracy y relevancia de function calls. | Agregar metricas separadas para schema, seleccion, ejecucion y respuesta final. |
| [Benchmarking MCP Tool Invocation In Computer-Use Agents](https://arxiv.org/html/2510.24563v2) | 2025 | Evalua invocacion MCP + GUI en escenarios de computer use. | Si la organizacion usa MCP, crear tareas con herramientas internas, distractores y logs de invocation. |
| [MCPWorld: A Unified Benchmarking Testbed for API, GUI ...](https://arxiv.org/html/2506.07672v1) | 2025 | Testbed MCP para API, GUI e interacciones hibridas. | Relevante para benchmarks que mezclan APIs internas y UI. |
| [MCP-Atlas: A Large-Scale Benchmark for Tool-Use Competency](https://arxiv.org/html/2602.00933v1) | 2026 | Evalua coordinacion multi-tool y grounding en outputs de herramientas. | Separar score de tool selection, parameterization, sequencing y final answer. |

## Metodologia, Contaminacion Y Validez

| Paper/Recurso | Ano | Idea reutilizable | Aplicacion para benchmark interno |
|---|---:|---|---|
| [Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110) | 2022 | Escenarios + multiples metricas + transparencia de prompts/completions. | Reportar por escenario, familia de tarea, costo, seguridad, robustez y eficiencia. |
| [Benchmark Data Contamination of Large Language Models: A Survey](https://arxiv.org/abs/2406.04244) | 2024 | Revisa contaminacion de benchmarks y mitigaciones. | Mantener holdout privado, canaries, rotacion de tareas y control de acceso. |
| [On Leakage of Code Generation Evaluation Datasets](https://arxiv.org/html/2407.07565v1) | 2024 | Discute leakage en datasets de code generation. | No exponer soluciones, hidden tests ni prompts de holdout a sistemas externos. |
| [Benchmarking Large Language Models Under Data Contamination](https://arxiv.org/html/2502.17521v2) | 2025 | Analiza benchmarks estaticos vs dinamicos bajo contaminacion. | Usar variantes parametrizadas y generacion controlada de tareas nuevas. |
| [The SWE-Bench Illusion: When State-of-the-Art LLMs Remember](https://arxiv.org/abs/2506.12286) | 2025 | Evidencia de memorizacion/contaminacion en SWE-bench Verified. | Justifica benchmarks privados y no depender de leaderboards publicos para compra/adopcion. |
| [Towards More Standardized AI Evaluation: From Models to Agents](https://arxiv.org/html/2602.18029v1) | 2026 | Plantea evals como funcion de control para sistemas agenticos. | Convertir benchmarks en gates continuos de operacion, no evaluacion one-shot. |
| [LLM Benchmark Datasets Should Be Contamination-Resistant](https://arxiv.org/html/2605.19999v1) | 2026 | Argumenta por benchmarks resistentes a contaminacion. | Diseñar datos privados que sean utiles para inferencia pero dificiles de memorizar. |

## Seguridad, Confianza Y Revision Humana

| Paper/Recurso | Ano | Idea reutilizable | Aplicacion para benchmark interno |
|---|---:|---|---|
| [SecureAgentBench: Benchmarking Secure Code Generation ...](https://arxiv.org/html/2509.22097v1) | 2025 | Evalua codigo correcto y seguro, no solo funcional. | Agregar fixtures donde seguridad y correctness son requisitos simultaneos. |
| [Agentic AI Software Engineers: Programming with Trust](https://arxiv.org/abs/2502.13767) | 2025 | Enfatiza que el foco cambia de programar a establecer confianza. | Medir reviewer comprehension, provenance, trazas y capacidad de auditoria. |
| [Trustworthy AI Software Engineers](https://arxiv.org/html/2602.06310v1) | 2026 | Vision sobre que hace confiable a un agente de software. | Definir gates de confianza antes de permitir autonomia en PRs. |

## Como Usarlos En El Informe Principal

Mapeo directo a `reports/internal_benchmark_harnesses.md`:

| Seccion del informe | Papers mas utiles |
|---|---|
| Task selection | SWE-bench, Terminal-Bench, TheAgentCompany, WorkArena |
| Harness adapter contract | SWE-agent, OpenHands, OpenHands SDK, Terminal-Bench |
| Environment and reproducibility | WebArena, OSWorld, AndroidWorld, Terminal-Bench |
| Scoring model | HELM, SWE-bench, tau-bench, BFCL |
| Human review rubric | End-to-end project development benchmark, Code Review Agent Benchmark, Agentic AI Software Engineers |
| Safety fixtures | SecureAgentBench, OpenHands, Terminal-Bench |
| Leakage and holdout governance | SWE-Bench Illusion, Benchmark Data Contamination survey, OpenAI SWE-bench Verified analysis |
| Enterprise workflow simulation | TheAgentCompany, WorkArena, tau-bench |

## Recomendacion Practica

Para el benchmark interno organizacional, no copiaria un solo paper. Usaria una mezcla:

1. **SWE-bench** para el formato issue-to-patch.
2. **Terminal-Bench** para entornos CLI hermeticos y tests duros.
3. **TheAgentCompany/WorkArena** para simular organizacion, herramientas internas y workflows de knowledge work.
4. **SWE-agent/OpenHands** para disenar el harness y los adapters.
5. **HELM** para reportar escenarios y multiples metricas.
6. **SWE-Bench Illusion + contamination surveys** para gobernanza de holdout, rotacion y leakage.

La conclusion mas importante de la literatura es consistente: un benchmark interno util debe evaluar el sistema completo, no solo el modelo. El objeto evaluado real es `modelo + harness + herramientas + sandbox + prompts + politica + entorno + reviewer workflow`.
