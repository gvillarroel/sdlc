# POC: agentes dinámicos con GitHub Copilot SDK

Este POC genera agentes configurables, les asigna skills distintas y los ejecuta uno tras otro desde GitHub Copilot CLI. La prueba de aceptación real queda registrada como evidencia sanitizada en [copilot-skill-demo.latest.json](results/copilot-skill-demo.latest.json).

## Qué demuestra

- Un registro JSON crea o actualiza agentes en tiempo de ejecución.
- La extensión de proyecto usa `@github/copilot-sdk/extension` y expone herramientas y slash commands dentro de Copilot CLI.
- El runner usa `@github/copilot-sdk` con `customAgents`, `skills`, `skillDirectories` y selección explícita de agente.
- Cada paso abre una sesión SDK aislada con su propio handler de permisos; una cadena mixta no comparte ni eleva permisos.
- La demo reserva sus tres nombres, limpia cualquier resto de una ejecución interrumpida, los crea después de iniciar la extensión, ejecuta la cadena y elimina sus entradas temporales.
- La cadena pasa la salida de cada agente al siguiente y conserva este orden:

```text
Prompt en Copilot
  → dynamic_agents_skill_demo
  → requirements-specialist  [extract-requirements]
  → risk-challenger          [challenge-assumptions]
  → delivery-planner         [build-delivery-plan]
  → reporte JSON verificable
```

Cada skill exige un marcador distinto. El marcador no basta por sí solo: la aceptación también comprueba el agente devuelto por `agent.select/getCurrent`, las skills asignadas por el runtime, `skills.getInvoked()` y eventos `skill.invoked` con trigger `agent-invoked`.

| Paso | Agente | Skill | Evidencia |
|---:|---|---|---|
| 1 | `requirements-specialist` | `extract-requirements` | `SKILL_REQUIREMENTS_OK` |
| 2 | `risk-challenger` | `challenge-assumptions` | `SKILL_RISK_OK` |
| 3 | `delivery-planner` | `build-delivery-plan` | `SKILL_PLAN_OK` |

## Estructura

- `agents/registry.json`: configuraciones dinámicas compartidas por la CLI y la extensión.
- `skills/*/SKILL.md`: skills cargadas oficialmente mediante `skillDirectories`.
- `src/runner.mjs`: ejecución SDK standalone y cadena secuencial con una sesión por paso.
- `src/extension-runtime.mjs`: herramientas y comandos registrados en la sesión activa.
- `.github/extensions/dynamic-agents/extension.mjs`: entrypoint descubierto por Copilot CLI.
- `.github/agents/dynamic-agent-orchestrator.agent.md`: agente que opera la extensión.
- `results/copilot-skill-demo.latest.json`: evidencia sanitizada de la última aceptación dentro de Copilot.

## Requisitos

- Node.js `^20.19.0` o `>=22.12.0`, igual que el SDK fijado.
- GitHub Copilot CLI actualizado y autenticado.
- Acceso a GitHub Copilot, o una configuración BYOK compatible con el SDK.
- Extensiones experimentales habilitadas con `--experimental`.

La versión validada fue Copilot CLI `1.0.70` con `@github/copilot-sdk` `1.0.5`.

## Instalación y pruebas offline

Desde este directorio:

```powershell
npm ci
npm test
npm run validate
```

Las pruebas unitarias no consumen solicitudes de Copilot. Cubren validación, skills inexistentes, mutaciones serializadas del registro, alcance canónico de lecturas, aislamiento de permisos por paso, orden de la cadena, propagación de resultados y prueba del runtime.

Smoke directo del SDK:

```powershell
npm run smoke:sdk
npm run smoke:skills
```

## Prueba dentro de Copilot

La prueba reproducible recomendada usa un permiso mínimo para una sola herramienta de extensión:

```powershell
.\scripts\smoke-in-copilot.ps1
```

El script:

1. ejecuta `copilot --experimental` con el agente `dynamic-agent-orchestrator`;
2. autoriza únicamente `custom-tool(dynamic_agents_skill_demo)`;
3. exige tres nombres nuevos y genera agentes con skills distintas después de `joinSession`;
4. ejecuta cada paso en una sesión SDK independiente;
5. verifica selección, asignación e invocación real de cada skill, además de orden y marcadores;
6. correlaciona el reporte con un `runId` único y elimina los agentes temporales;
7. actualiza `results/copilot-skill-demo.latest.json` sin prompts, respuestas, rutas locales ni IDs de sesión.

También se puede probar interactivamente desde la raíz del repositorio:

```powershell
copilot --experimental
```

Comandos disponibles en la TUI:

```text
/dynamic-agents
/dynamic-agent-create {"name":"my-agent","description":"...","prompt":"...","tools":[],"skills":["extract-requirements"],"permissionMode":"deny-all"}
/dynamic-agent-run my-agent :: Ejecuta esta tarea
/dynamic-agent-chain requirements-specialist,risk-challenger,delivery-planner :: Diseña un POC seguro
/dynamic-agent-skill-demo Diseña un POC seguro
```

En modo prompt, las extensiones de proyecto requieren `GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS=true`; el script ya lo configura solo para su proceso.

## Seguridad del POC

- Los nombres y skills usan una allowlist `lowercase-kebab-case`; cada `SKILL.md` debe existir dentro de un directorio permitido y declarar el mismo nombre.
- Las escrituras del registro son atómicas y las mutaciones del proceso se serializan para evitar updates perdidos.
- Solo existen `deny-all` y `read-only`; no hay modo `approve-all` en agentes dinámicos.
- El valor predeterminado es `deny-all`, que exige `tools: []`.
- `read-only` solo acepta `glob`, `grep`, `read`, `search` y `view`; su handler aprueba únicamente lecturas cuya ruta canónica esté dentro del repositorio. Shell, red, MCP, escrituras y bypass del sandbox se rechazan.
- El modo autenticado reduce el entorno heredado a una allowlist operativa y elimina tokens u otras variables arbitrarias. `--auth inherited` existe solo para escenarios explícitos y confiables.
- Los agentes de la demo usan `tools: []`; sus skills transforman texto y no ejecutan comandos del sistema.
- El reporte publicable conserva hashes, longitudes y pruebas del runtime, pero no contenido generado, prompts, rutas de usuario ni IDs de sesión.
- Las extensiones de Copilot CLI son experimentales y ejecutan código local con los privilegios del usuario. Solo debe cargarse código de confianza.

Esto es un POC, no un sandbox de producción. La allowlist y los handlers reducen capacidades del SDK, pero no sustituyen aislamiento de proceso/VM, controles de egress, gestión de secretos ni políticas corporativas.

## Fuentes oficiales

- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)
- [Custom agents and sub-agent orchestration](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents)
- [Custom skills](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/skills)
- [Streaming events in the Copilot SDK](https://docs.github.com/en/copilot/how-tos/copilot-sdk/use-copilot-sdk/streaming-events)
- [Creating extensions for GitHub Copilot CLI](https://docs.github.com/en/copilot/tutorials/create-an-extension)
- [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)

Las antiguas Copilot Extensions basadas en GitHub Apps no se usan: GitHub las retiró en noviembre de 2025. Este POC usa las extensiones locales actuales de Copilot CLI.
