# Reporte Final Global: Evaluacion De Orquestadores AI Para SDLC

Date: 2026-07-07

Este reporte consolida el material recopilado en el repositorio y lo convierte en una lectura ejecutiva y tecnica unica. La evidencia fuente sigue en `data/`, `results/`, `reports/`, `templates/` y `scripts/`; este documento explica como encaja todo y que decision practica habilita.

## Vista Global

La conclusion principal es que no existe un ganador universal. La eleccion depende del escenario de adopcion, del nivel de autonomia deseado, del control humano requerido, de la tolerancia al lock-in de proveedor, del modelo de sandbox y de la capacidad operativa del equipo.

El analisis filtra alternativas open source permisivas, las puntua con 14 criterios, ejecuta rankings deterministas y simulaciones Monte Carlo, revisa sensibilidad a pesos, estima esfuerzo y costo operativo, agrega un reporte dedicado de sandboxing, y termina en un plan de piloto con gates de seguridad y no-go conditions.

La recomendacion practica es hacer un piloto controlado de dos semanas con:

1. `OpenHands Software Agent SDK`
2. `Cline / Cline SDK`
3. `Deep Agents`
4. `Codex CLI` para PRs autonomos seguros, o `mini-SWE-agent` si el objetivo principal es benchmarking reproducible

La decision final debe depender de evidencia de piloto, no solo del ranking simulado.

## Que Se Evaluo

El universo inicial proviene de una conversacion compartida sobre frameworks y herramientas de orquestacion para agentes de codigo. El repositorio conserva solo alternativas open source permisivas bajo MIT o Apache-2.0, y excluye opciones cerradas o no compatibles con ese filtro.

La evaluacion cubre:

- 17 alternativas incluidas y 2 excluidas por licencia o modelo cerrado.
- 14 criterios de scoring con escala 0 a 5.
- 5 escenarios de decision.
- 5,000 trials Monte Carlo para rankings de alternativas.
- 4,000 trials Monte Carlo para sandboxing.
- Stress tests de supuestos deterministas e incertidumbre.
- Analisis de riesgos, evidencia, mantenimiento, mercado y confianza.
- Plantillas para ejecutar pilotos y capturar resultados comparables.

## Modelo Conceptual

El sistema se puede leer como una cadena de evidencia:

`data/*.json` define candidatos, criterios, escenarios, riesgos, tareas piloto y supuestos.
`scripts/*.py` transforma esos datos en resultados reproducibles.
`results/*.csv` conserva rankings, estabilidad, costos, gaps, riesgos y matrices de decision.
`reports/*.md` interpreta esos resultados para audiencias ejecutivas, tecnicas y de seguridad.
`templates/` y `examples/` convierten la simulacion en evidencia de piloto real.
`tests/` y `ci/` validan que los artefactos sigan consistentes.

Para una vista visual completa, ver `reports/system_diagrams.md`.

## Metodologia

La metodologia combina decision multicriterio y validacion reproducible:

1. Filtrar por licencia permisiva.
2. Puntuar alternativas contra 14 criterios.
3. Aplicar pesos por escenario.
4. Calcular ranking determinista.
5. Perturbar scores y pesos con Monte Carlo para medir estabilidad.
6. Revisar sensibilidad, regret, Pareto frontier y estabilidad cross-scenario.
7. Ajustar interpretacion con esfuerzo de implementacion, costo operativo, evidencia y riesgo.
8. Separar el problema de sandboxing en una evaluacion dedicada.
9. Traducir la shortlist a un protocolo de piloto y gates de seguridad.

Los resultados son utiles para reducir incertidumbre antes del piloto, pero no sustituyen pruebas con repositorios internos.

## Hallazgos Por Escenario

| Escenario | Lider simulado | Lectura practica |
|---|---|---|
| Custom orchestrator platform | `Cline / Cline SDK` por margen minimo sobre `OpenHands SDK` | Es una carrera cerrada; pilotear ambos contra `Deep Agents` antes de decidir. |
| Secure autonomous PRs | `Codex CLI` | Buena opcion si se acepta dependencia OpenAI y se prioriza sandboxing/PR automation; comparar con `OpenHands SDK` y `Cline`. |
| Quick local coding | `Cline / Cline SDK` | Es el candidato mas estable para productividad local; `OpenCode` y `Aider` sirven como benchmarks ligeros. |
| Research benchmarking | `mini-SWE-agent` | Es el mejor baseline reproducible; comparar con `SWE-agent` y `OpenHands SDK` si se necesitan flujos mas completos. |
| Enterprise control plane | `Cline / Cline SDK` | Lidera la simulacion, pero la decision depende de gobernanza multi-equipo, observabilidad y carga operacional. |

La estabilidad global muestra que `OpenHands Software Agent SDK` aparece top 3 en todos los escenarios, mientras que `Cline / Cline SDK` aparece top 3 en cuatro de cinco. Esa combinacion sugiere que el piloto principal debe comparar ambos.

## Lectura De Candidatos

### OpenHands Software Agent SDK

Es el candidato mas estable cross-scenario. Encaja bien si el objetivo es construir una plataforma propia, mantener flexibilidad y capturar artefactos operativos. No debe adoptarse sin validar integracion, runtime, credenciales, logs y ciclo de upgrades.

### Cline / Cline SDK

Tiene fuerte ajuste en flujos humanos, productividad local y control-plane ligero. Su fortaleza es el workflow de desarrollo y la adopcion por usuarios. El piloto debe medir si la supervision humana necesaria preserva la ganancia de productividad.

### Deep Agents

Funciona como candidato fuerte para orquestacion y multi-agent patterns, pero no lidera de forma dominante. Conviene como comparador tecnico cuando el equipo quiere construir una capa programable y no solo operar una CLI.

### Codex CLI

Destaca en PRs autonomos seguros y menor esfuerzo inicial. El tradeoff principal es la dependencia de proveedor y la necesidad de validar politicas, aprobaciones, secretos, red y sandbox real antes de automatizar cambios de codigo.

### mini-SWE-agent y SWE-agent

Son especialmente valiosos para investigacion, benchmarking y reproducibilidad. No son necesariamente el mejor producto operativo para equipos, pero son excelentes como baseline para medir si herramientas mas complejas realmente aportan valor.

## Seguridad Y Sandboxing

El reporte dedicado de sandboxing separa una pregunta critica: que aislamiento es adecuado para agentes que ejecutan codigo. La respuesta depende de si el trabajo es local, PR autonomo, codigo de usuarios no confiables, evaluaciones a escala o self-hosting enterprise.

| Escenario sandbox | Candidato lider | Implicacion |
|---|---|---|
| Local developer agents | `Flue virtual sandbox`, `Daytona`, `Kubernetes hardened pods` casi empatados | Para tareas locales, el contexto y la ergonomia pesan tanto como el aislamiento duro. |
| Autonomous PR security | `Daytona` | Los sandboxes administrados son fuertes si pasan revision de aislamiento, tenancy, secretos y costo. |
| Untrusted user code | `Daytona`, seguido por `E2B` y `Modal` | No ejecutar codigo no confiable sin una revision explicita de boundaries, red y secretos. |
| Evals and RL scale | `Daytona`, `Modal`, `E2B` | La escala administrada importa mas que la comodidad local. |
| Enterprise self-hosted | `Kubernetes hardened pods`, `Firecracker microVMs`, `Kata Containers` | Self-hosting exige capacidad de plataforma y observabilidad seria. |

La regla operativa: no confundir approvals o convenciones de workflow con aislamiento duro. Los gates de seguridad deben probar prompt injection, workspace boundary, secretos, red y calidad de diffs.

## Riesgos Principales

Los riesgos mas importantes no son solo tecnicos:

- Prompt injection desde issues, docs, paginas web o tool output.
- Escapes de sandbox o escritura fuera del workspace.
- Exposicion de secretos en logs, prompts o resultados.
- Politicas de red demasiado amplias.
- Benchmarks publicos que no transfieren a repositorios internos.
- Churn de APIs alpha/beta.
- Observabilidad insuficiente para reconstruir fallos.
- PRs autonomos con diffs grandes o de baja calidad.
- Lock-in de modelo o proveedor.
- Costos y latencia fuera del perfil operativo.

Cada riesgo tiene evidencia requerida y pass condition en `results/risk_validation_matrix.csv`.

## Mercado, Mantenimiento Y Confianza

Los addenda del repositorio muestran que AI-native creation reduce el costo de prototipado, pero desplaza la dificultad hacia distribucion, diferenciacion, soporte y confianza. Construir rapido no garantiza producto defendible.

La decision de adopcion debe pasar cuatro gates:

1. El framework mejora resultados frente a baselines simples.
2. El equipo puede operar y mantener el stack.
3. El modelo de seguridad soporta el nivel de autonomia deseado.
4. El producto o flujo resultante es defendible y revisable.

La matriz de confianza tambien advierte que leer codigo generado no escala si no hay provenance, tests, diffs enfocados y reconstruccion de decisiones.

## Plan De Piloto Recomendado

Ejecutar un piloto de dos semanas con tareas representativas y comparables:

1. Seleccionar 3 o 4 candidatos segun escenario.
2. Ejecutar tareas de `data/pilot_tasks.json`.
3. Registrar cada run en `templates/pilot_run_log.csv`.
4. Evaluar diffs con `templates/reviewer_scorecard.md`.
5. Aplicar gates de `templates/security_gate_checklist.md`.
6. Calcular decision post-piloto con `scripts/score_pilot_results.py`.
7. Documentar no-go conditions en `reports/adoption_decision_record.md`.

El criterio de exito no debe ser solo "la tarea paso". Debe incluir tiempo humano, calidad del diff, trazabilidad, seguridad, costo, latencia, reproducibilidad y facilidad de mantenimiento.

## Recomendacion Ejecutiva

Si el objetivo es elegir una base general para evolucionar un sistema de agentes de codigo, empezar con un piloto `OpenHands SDK` vs `Cline SDK` vs `Deep Agents`.
Si el objetivo inmediato es PR autonomo seguro, incluir `Codex CLI` y priorizar gates de sandbox, secretos, red y approvals.
Si el objetivo es investigacion reproducible, usar `mini-SWE-agent` y `SWE-agent` como baseline antes de adoptar herramientas mas amplias.
Si el objetivo es enterprise control plane, no adoptar por ranking: validar primero operacion multi-equipo, observabilidad, governance y costo de mantenimiento.

## Trazabilidad

| Necesidad | Artefacto fuente |
|---|---|
| Navegar todos los entregables | `reports/artifact_index.md` |
| Entender conexiones entre tools y conceptos | `reports/system_diagrams.md` |
| Revisar metodologia | `reports/methodology_appendix.md` |
| Revisar reporte principal | `reports/ai_orchestrator_frameworks_report.md` |
| Revisar sandboxing | `reports/sandbox_report.md` |
| Revisar market/maintenance/trust | `reports/market_maintenance_synthesis.md` |
| Revisar riesgos residuales | `reports/residual_risks.md` |
| Ejecutar mantenimiento | `reports/maintenance_guide.md` |
| Validar todo localmente | `python scripts/run_all_checks.py` |

## Estado De Publicacion

La version web de este reporte se publica desde `docs/index.html` mediante GitHub Pages con la fuente `main` / `docs`.
