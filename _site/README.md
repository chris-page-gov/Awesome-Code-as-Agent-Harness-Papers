# Awesome Code as Agent Harness Papers

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![arXiv](https://img.shields.io/badge/arXiv-2605.18747-b31b1b.svg)](https://arxiv.org/abs/2605.18747)
[![Website](https://img.shields.io/badge/Website-code--as--harness.github.io-1f6feb?logo=googlechrome&logoColor=white)](https://code-as-harness.github.io/code-as-harness-webpage/)
[![HF #1 Paper of the Day](https://img.shields.io/badge/%F0%9F%A4%97%20HF-%231%20Paper%20of%20the%20Day-FFD21E)](https://huggingface.co/papers/2605.18747)
[![@_akhaliq](https://img.shields.io/badge/%40__akhaliq-6366F1?logo=x&logoColor=white&labelColor=000000)](https://x.com/_akhaliq/status/2056900568921133565?s=20)
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=chris-page-gov.Awesome-Code-as-Agent-Harness-Papers)

This repository accompanies the survey [**Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems**](https://arxiv.org/abs/2605.18747).
We study the emerging role of code in agentic AI: code is no longer only a generated artifact, but increasingly serves as an executable, inspectable, and stateful harness through which agents reason, act, model environments, receive feedback, and coordinate. The repository organizes representative papers around three connected layers: **Harness Interface**, **Harness Mechanisms**, and **Scaling the Harness**, covering directions such as coding assistants, GUI/OS automation, scientific discovery, and embodied intelligence.

## Fork LLM-Wiki

This fork adds a source-backed Karpathy-style [LLM-Wiki](LLM-WIKI.md) for the
Code as Agent Harness paper and reference graph. Start at
[wiki/index.md](wiki/index.md) for the taxonomy map, source notes, reading
routes, and source-localization status.

> [!TIP]
> 👋 We welcome paper suggestions, pull requests, and collaborations on code as agent harness. Please contact us at `xuyingn2@illinois.edu`, `kt42@illinois.edu`, `twei10@illinois.edu`, `zihaoli5@illinois.edu`, and `bei4@illinois.edu`. We will keep updating this repository with recent work on code-centric agentic systems and harness engineering.

> [!NOTE]
> 📚 If you find this resource useful, please cite and [![Stars](https://img.shields.io/github/stars/chris-page-gov/Awesome-Code-as-Agent-Harness-Papers?style=social)](https://github.com/chris-page-gov/Awesome-Code-as-Agent-Harness-Papers) the repo:
>
>
> ```bibtex
> @article{ning2026codeasharness,
>   title   = {Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems},
>   author  = {Ning, Xuying and Tieu, Katherine and Fu, Dongqi and Wei, Tianxin and Li, Zihao and Bei, Yuanchen and others},
>   journal = {arXiv preprint arXiv:2605.18747},
>   year    = {2026}
> }
> ```

![Framework overview](figs/overview.png)

## 🔔 News

**[2026-05]** 🚀 Our survey ***Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*** is available on [arXiv](https://arxiv.org/abs/2605.18747). Slides and project page links will be added here once available.

## 📋 Table of Contents

- [🔔 News](#-news)
- [Fork LLM-Wiki](#fork-llm-wiki)
- [📋 Table of Contents](#-table-of-contents)
- [🧩 Harness Interface](#-harness-interface)
  - [💭 Code for Reasoning](#-code-for-reasoning)
  - [🤖 Code for Acting](#-code-for-acting)
  - [🌍 Code for Environment Modeling](#-code-for-environment-modeling)
- [🛠️ Harness Mechanisms](#%EF%B8%8F-harness-mechanisms)
  - [🗺️ Planning for Code Agents](#%EF%B8%8F-planning-for-code-agents)
  - [🧠 Memory and Context Engineering](#-memory-and-context-engineering)
  - [🔧 Tool Usage for Code Agents](#-tool-usage-for-code-agents)
  - [🧪 Feedback-Guided Iterative Debugging](#-feedback-guided-iterative-debugging)
- [👥 Scaling the Harness: Multi-Agent Code-Centric Systems](#-scaling-the-harness-multi-agent-code-centric-systems)
  - [🎭 Functional Role Specialization](#-functional-role-specialization)
  - [💬 Interaction Modes](#-interaction-modes)
  - [🕸️ Workflow Topology](#%EF%B8%8F-workflow-topology)
  - [⚡ Execution Feedback Integration](#-execution-feedback-integration)
  - [🔄 Shared-Harness Synchronization](#-shared-harness-synchronization)
  - [🏛️ Shared Harness Representation](#%EF%B8%8F-shared-harness-representation)
  - [🎯 Harness-State Convergence](#-harness-state-convergence)
- [🚀 Applications and Emerging Fields](#-applications-and-emerging-fields)
  - [💻 Code Assistants](#-code-assistants)
  - [🖥️ GUI / OS Agents](#%EF%B8%8F-gui--os-agents)
  - [🔬 Scientific Discovery Agents](#-scientific-discovery-agents)
  - [🤖 Autonomous Embodied Agents](#-autonomous-embodied-agents)

---

## 🧩 Harness Interface

Code as the basic interface between a model and its task environment. Programs convert model outputs into executable, inspectable, and stateful structures: code makes reasoning *executable*, action *programmable*, and environment state *inspectable*.

![Harness interface](figs/harness_interface.png)

### 💭 Code for Reasoning

Programs externalize internal logic into verifiable computation, allowing interpreters, symbolic solvers, execution traces, or process rewards to check and refine intermediate steps.

#### Program-Delegated Reasoning

| Paper | Venue |
| --- | --- |
| [Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks](wiki/papers/program-of-thoughts-prompting-disentangling-computation-from-reasoning-f-19ca2a5b.md) | TMLR 2023 |
| [MathCoder: Seamless Code Integration in LLMs for Enhanced Mathematical Reasoning](wiki/papers/mathcoder-seamless-code-integration-in-llms-for-enhanced-mathematical-re-1e3c58a8.md) | ICLR 2024 |
| [Chain of Code: Reasoning with a Language Model-Augmented Code Emulator](wiki/papers/chain-of-code-reasoning-with-a-language-model-augmented-code-emulator-7eae58c2.md) | ICML 2024 |
| [Method-Based Reasoning for Large Language Models: Extraction, Reuse, and Continuous Improvement](wiki/papers/method-based-reasoning-for-large-language-models-extraction-reuse-and-co-1e23178f.md) | arXiv 2025 |
| [Code-Enabled Language Models Can Outperform Reasoning Models on Diverse Tasks](wiki/papers/code-enabled-language-models-can-outperform-reasoning-models-on-diverse-8a2f13f2.md) | arXiv 2025 |
| [When Do Program-of-Thought Works for Reasoning?](wiki/papers/when-do-program-of-thought-works-for-reasoning-40f747f3.md) | AAAI 2024 |
| [PAL: Program-aided Language Models](wiki/papers/pal-program-aided-language-models-a557cd88.md) | ICML 2023 |
| [Show Your Work: Scratchpads for Intermediate Computation with Language Models](wiki/papers/show-your-work-scratchpads-for-intermediate-computation-with-language-mo-b47afb69.md) | arXiv 2021 |
| [Reasoning Like Program Executors](wiki/papers/reasoning-like-program-executors-4707ead4.md) | EMNLP 2022 |
| [Towards Better Understanding of Program-of-Thought Reasoning in Cross-Lingual and Multilingual Environments](wiki/papers/towards-better-understanding-of-program-of-thought-reasoning-in-cross-li-d09e4e83.md) | ACL 2025 Findings |
| [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](wiki/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models-f78bfa67.md) | NeurIPS 2022 |

#### Hybrid Symbolic–Neural Execution

| Paper | Venue |
| --- | --- |
| [Self-Verifying Reflection Helps Transformers with CoT Reasoning](wiki/papers/self-verifying-reflection-helps-transformers-with-cot-reasoning-00031e2b.md) | NeurIPS 2025 |
| [SSR: Socratic Self-Refine for Large Language Model Reasoning](wiki/papers/ssr-socratic-self-refine-for-large-language-model-reasoning-833e8f4e.md) | arXiv 2025 |
| [CodeSteer: Symbolic-Augmented Language Models via Code/Text Guidance](wiki/papers/codesteer-symbolic-augmented-language-models-via-code-text-guidance-691bb2b4.md) | ICML 2025 |
| [Graph of Thoughts: Solving Elaborate Problems with Large Language Models](wiki/papers/graph-of-thoughts-solving-elaborate-problems-with-large-language-models-1c841461.md) | AAAI 2024 |
| [Code-as-Symbolic-Planner: Foundation Model-Based Robot Planning via Symbolic Code Generation](wiki/papers/code-as-symbolic-planner-foundation-model-based-robot-planning-via-symbo-0ef8c8e2.md) | IROS 2025 |

#### Iterative Code-Grounded Reasoning

| Paper | Venue |
| --- | --- |
| [NExT: Teaching Large Language Models to Reason about Code Execution](wiki/papers/next-teaching-large-language-models-to-reason-about-code-execution-741e691c.md) | ICML 2024 |
| [What I cannot execute, I do not understand: Training and Evaluating LLMs on Program Execution Traces](wiki/papers/what-i-cannot-execute-i-do-not-understand-training-and-evaluating-llms-o-f2d43ec2.md) | arXiv 2025 |
| [Reasoning Through Execution: Unifying Process and Outcome Rewards for Code Generation](wiki/papers/reasoning-through-execution-unifying-process-and-outcome-rewards-for-cod-475408b7.md) | ICML 2025 |
| [CodeRL+: Improving Code Generation via Reinforcement with Execution Semantics Alignment](wiki/papers/coderl-improving-code-generation-via-reinforcement-with-execution-semant-0b0cc17f.md) | arXiv 2025 |
| [RLTF: Reinforcement Learning from Unit Test Feedback](wiki/papers/rltf-reinforcement-learning-from-unit-test-feedback-8415ece3.md) | TMLR 2023 |
| [RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning](wiki/papers/rlef-grounding-code-llms-in-execution-feedback-with-reinforcement-learni-cd375a09.md) | ICML 2025 |
| [Execution guided line-by-line code generation](wiki/papers/execution-guided-line-by-line-code-generation-81a6e31d.md) | NeurIPS 2025 |
| [R1-Code-Interpreter: LLMs Reason with Code via Supervised and Multi-stage Reinforcement Learning](wiki/papers/r1-code-interpreter-llms-reason-with-code-via-supervised-and-multi-stage-7b9d409d.md) | arXiv 2025 |
| [CYCLE: Learning to Self-Refine the Code Generation](wiki/papers/cycle-learning-to-self-refine-the-code-generation-42b9d63d.md) | OOPSLA 2024 |
| [StepCoder: Improve Code Generation with Reinforcement Learning from Compiler Feedback](wiki/papers/stepcoder-improve-code-generation-with-reinforcement-learning-from-compi-19519e0d.md) | ACL 2024 |
| [CodeRL: Mastering Code Generation through Pretrained Models and Deep Reinforcement Learning](wiki/papers/coderl-mastering-code-generation-through-pretrained-models-and-deep-rein-cdda5aba.md) | NeurIPS 2022 |
| [CodePRM: Execution Feedback-enhanced Process Reward Model for Code Generation](wiki/papers/codeprm-execution-feedback-enhanced-process-reward-model-for-code-genera-6f1b5476.md) | ACL 2025 Findings |
| [SatLM: Satisfiability-Aided Language Models Using Declarative Prompting](wiki/papers/satlm-satisfiability-aided-language-models-using-declarative-prompting-7cfd10ef.md) | NeurIPS 2023 |
| [Self-Edit: Fault-Aware Code Editor for Code Generation](wiki/papers/self-edit-fault-aware-code-editor-for-code-generation-7656c379.md) | ACL 2023 |

### 🤖 Code for Acting

Generated programs serve as policies, tool calls, behavior trees, or reusable skills for embodied, GUI, software, and tool-use environments.

#### Grounded Skill Selection

| Paper | Venue |
| --- | --- |
| [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](wiki/papers/do-as-i-can-not-as-i-say-grounding-language-in-robotic-affordances-a610b79a.md) | CoRL 2022 |
| [Robots That Ask for Help: Uncertainty Alignment for Large Language Model Planners](wiki/papers/robots-that-ask-for-help-uncertainty-alignment-for-large-language-model-c20455bc.md) | CoRL 2023 |
| [Bootstrap Your Own Skills: Learning to Solve New Tasks with Large Language Model Guidance](wiki/papers/bootstrap-your-own-skills-learning-to-solve-new-tasks-with-large-languag-6e0dd321.md) | CoRL 2023 |
| [SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse](wiki/papers/skillvla-tackling-combinatorial-diversity-in-dual-arm-manipulation-via-s-22c17d5e.md) | arXiv 2026 |
| [Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition](wiki/papers/scaling-up-and-distilling-down-language-guided-robot-skill-acquisition-22b4d98a.md) | CoRL 2023 |
| [Lifelong Robot Library Learning: Bootstrapping Composable and Generalizable Skills for Embodied Control with Language Models](wiki/papers/lifelong-robot-library-learning-bootstrapping-composable-and-generalizab-a115e6fb.md) | ICRA 2024 |

#### Programmatic Policy Generation

| Paper | Venue |
| --- | --- |
| [RoboCodeX: Multimodal Code Generation for Robotic Behavior Synthesis](wiki/papers/robocodex-multimodal-code-generation-for-robotic-behavior-synthesis-7e8876fb.md) | ICML 2024 |
| [CP-Agent: Agentic Constraint Programming](wiki/papers/cp-agent-agentic-constraint-programming-f117f2ca.md) | arXiv 2025 |
| [LLM-Driven Corrective Robot Operation Code Generation with Static Text-Based Simulation](wiki/papers/llm-driven-corrective-robot-operation-code-generation-with-static-text-b-582b9325.md) | ICRA 2026 |
| [NormCode: A Semi-Formal Language for Auditable AI Planning](wiki/papers/normcode-a-semi-formal-language-for-auditable-ai-planning-96b226f7.md) | arXiv 2025 |
| [ALRM: Agentic LLM for Robotic Manipulation](wiki/papers/alrm-agentic-llm-for-robotic-manipulation-10f7a82b.md) | arXiv 2026 |
| [RACAS: Controlling Diverse Robots With a Single Agentic System](wiki/papers/racas-controlling-diverse-robots-with-a-single-agentic-system-cdaaa413.md) | arXiv 2026 |
| [ReAct: Synergizing Reasoning and Acting in Language Models](wiki/papers/react-synergizing-reasoning-and-acting-in-language-models-99278094.md) | ICLR 2023 |
| [GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models](wiki/papers/genswarm-scalable-multi-robot-code-policy-generation-and-deployment-via-b4a3a391.md) | npj Robotics 2026 |
| [Code as Policies: Language Model Programs for Embodied Control](wiki/papers/code-as-policies-language-model-programs-for-embodied-control-b943849c.md) | ICRA 2023 |
| [Robotic Programmer: Video Instructed Policy Code Generation for Robotic Manipulation](wiki/papers/robotic-programmer-video-instructed-policy-code-generation-for-robotic-m-084591c8.md) | arXiv 2025 |
| [Code-BT: A Code-Driven Approach to Behavior Tree Generation for Robot Tasks Planning with Large Language Models](wiki/papers/code-bt-a-code-driven-approach-to-behavior-tree-generation-for-robot-tas-e57c984e.md) | IJCAI 2025 |

#### Lifelong Code-Based Agents

| Paper | Venue |
| --- | --- |
| [Growing with Your Embodied Agent: A Human-in-the-Loop Lifelong Code Generation Framework for Long-Horizon Manipulation Skills](wiki/papers/growing-with-your-embodied-agent-a-human-in-the-loop-lifelong-code-gener-7092156e.md) | arXiv 2025 |
| [ViReSkill: Vision-Grounded Replanning with Skill Memory for LLM-Based Planning in Lifelong Robot Learning](wiki/papers/vireskill-vision-grounded-replanning-with-skill-memory-for-llm-based-pla-5e0ae7fb.md) | arXiv 2025 |
| [UI-Voyager: A Self-Evolving GUI Agent Learning via Failed Experience](wiki/papers/ui-voyager-a-self-evolving-gui-agent-learning-via-failed-experience-21027868.md) | arXiv 2026 |
| [Voyager: An Open-Ended Embodied Agent with Large Language Models](wiki/papers/voyager-an-open-ended-embodied-agent-with-large-language-models-b3b8e559.md) | TMLR 2023 |
| [Lifelong Language-Conditioned Robotic Manipulation Learning](wiki/papers/lifelong-language-conditioned-robotic-manipulation-learning-a0e49c32.md) | arXiv 2026 |

### 🌍 Code for Environment Modeling

Program states, repositories, traces, simulators, and tests represent state, dynamics, and feedback signals for agent interaction.

#### Structured World Representations

| Paper | Venue |
| --- | --- |
| [From Programs to Poses: Factored Real-World Scene Generation via Learned Program Libraries](wiki/papers/from-programs-to-poses-factored-real-world-scene-generation-via-learned-348b0a74.md) | NeurIPS 2025 |
| [PoE-World: Compositional World Modeling with Products of Programmatic Experts](wiki/papers/poe-world-compositional-world-modeling-with-products-of-programmatic-exp-1d3860f4.md) | NeurIPS 2025 |
| [Code2World: A GUI World Model via Renderable Code Generation](wiki/papers/code2world-a-gui-world-model-via-renderable-code-generation-7301fde3.md) | arXiv 2026 |
| [Code2Worlds: Empowering Coding LLMs for 4D World Generation](wiki/papers/code2worlds-empowering-coding-llms-for-4d-world-generation-ecff7d79.md) | arXiv 2026 |
| [ViStruct: Visual Structural Knowledge Extraction via Curriculum Guided Code-Vision Representation](wiki/papers/vistruct-visual-structural-knowledge-extraction-via-curriculum-guided-co-63a9674d.md) | EMNLP 2023 |

#### Execution-Trace World Modeling

| Paper | Venue |
| --- | --- |
| [SemCoder: Training Code Language Models with Comprehensive Semantics Reasoning](wiki/papers/semcoder-training-code-language-models-with-comprehensive-semantics-reas-4b1a7d41.md) | NeurIPS 2024 |
| [CWM: An Open-Weights LLM for Research on Code Generation with World Models](wiki/papers/cwm-an-open-weights-llm-for-research-on-code-generation-with-world-model-f3c77c94.md) | arXiv 2025 |
| [Reinforcement World Model Learning for LLM-based Agents](wiki/papers/reinforcement-world-model-learning-for-llm-based-agents-b569b4d7.md) | arXiv 2026 |
| [Agent World Model: Infinity Synthetic Environments for Agentic Reinforcement Learning](wiki/papers/agent-world-model-infinity-synthetic-environments-for-agentic-reinforcem-a9d3ddcc.md) | arXiv 2026 |
| [Aligning Agentic World Models via Knowledgeable Experience Learning](wiki/papers/aligning-agentic-world-models-via-knowledgeable-experience-learning-979e70cd.md) | arXiv 2026 |
| [WorldCoder, a Model-Based LLM Agent: Building World Models by Writing Code and Interacting with the Environment](wiki/papers/worldcoder-a-model-based-llm-agent-building-world-models-by-writing-code-f1f4d068.md) | NeurIPS 2024 |

#### Code-Grounded Evaluation Environments

| Paper | Venue |
| --- | --- |
| [CRUXEval: A Benchmark for Code Reasoning, Understanding and Execution](wiki/papers/cruxeval-a-benchmark-for-code-reasoning-understanding-and-execution-f67bd9bf.md) | ICML 2024 |
| [LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code](wiki/papers/livecodebench-holistic-and-contamination-free-evaluation-of-large-langua-50cb60b3.md) | ICLR 2025 |
| [SWE-bench: Can Language Models Resolve Real-world Github Issues?](wiki/papers/swe-bench-can-language-models-resolve-real-world-github-issues-3deec234.md) | ICLR 2024 |
| [AgentBench: Evaluating LLMs as Agents](wiki/papers/agentbench-evaluating-llms-as-agents-8d39628a.md) | ICLR 2024 |
| [CoRe: Benchmarking LLMs' Code Reasoning Capabilities through Static Analysis Tasks](wiki/papers/core-benchmarking-llms-code-reasoning-capabilities-through-static-analys-f15ad316.md) | NeurIPS 2025 |
| [Geogrambench: Benchmarking the geometric program reasoning in modern llms](wiki/papers/geogrambench-benchmarking-the-geometric-program-reasoning-in-modern-llms-71655d37.md) | arXiv 2025 |
| [CodeGlance: Understanding Code Reasoning Challenges in LLMs through Multi-Dimensional Feature Analysis](wiki/papers/codeglance-understanding-code-reasoning-challenges-in-llms-through-multi-7f129bb5.md) | arXiv 2026 |
| [Endless Terminals: Scaling RL Environments for Terminal Agents](wiki/papers/endless-terminals-scaling-rl-environments-for-terminal-agents-76f2d638.md) | arXiv 2026 |
| [Reflexion: Language Agents with Verbal Reinforcement Learning](wiki/papers/reflexion-language-agents-with-verbal-reinforcement-learning-a336a163.md) | NeurIPS 2023 |
| [CRUXEval-X: A Benchmark for Multilingual Code Reasoning, Understanding and Execution](wiki/papers/cruxeval-x-a-benchmark-for-multilingual-code-reasoning-understanding-and-c7df6977.md) | ACL 2025 |
| [InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback](wiki/papers/intercode-standardizing-and-benchmarking-interactive-coding-with-executi-dd16472a.md) | NeurIPS 2023 |

## 🛠️ Harness Mechanisms

Once code is placed inside the agent loop, the harness must decide *what to execute next*, *preserve useful state*, *expose the right tools*, and *convert failures into corrective actions*.

![Harness mechanisms](figs/harness_mechanism.png)

### 🗺️ Planning for Code Agents

Planning is harness control: it structures how the agent externalizes intent into executable steps, schedules interactions with code artifacts and tools, and regulates the trajectory of reasoning, execution, and revision over time.

#### Linear Decomposition Planning

| Paper | Venue |
| --- | --- |
| [A Real-World WebAgent with Planning, Long Context Understanding, and Program Synthesis](wiki/papers/a-real-world-webagent-with-planning-long-context-understanding-and-progr-e7655cc5.md) | ICLR 2024 |
| [ReAct: Synergizing Reasoning and Acting in Language Models](wiki/papers/react-synergizing-reasoning-and-acting-in-language-models-99278094.md) | ICLR 2023 |
| [Self-planning Code Generation with Large Language Models](wiki/papers/self-planning-code-generation-with-large-language-models-a101bcd0.md) | TOSEM 2024 |
| [Knowledge-Aware Code Generation with Large Language Models](wiki/papers/knowledge-aware-code-generation-with-large-language-models-7a42e382.md) | arXiv 2024 |
| [PaT: Planning-after-Trial for Efficient Test-Time Code Generation](wiki/papers/pat-planning-after-trial-for-efficient-test-time-code-generation-c7001067.md) | 2025 |
| [A Little Help Goes a Long Way: Tutoring LLMs in Solving Competitive Programming through Hints](wiki/papers/a-little-help-goes-a-long-way-tutoring-llms-in-solving-competitive-progr-485292a2.md) | TSE 2025 |

#### Structure-Grounded Planning

| Paper | Venue |
| --- | --- |
| [RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation](wiki/papers/rpg-a-repository-planning-graph-for-unified-and-scalable-codebase-genera-e832599a.md) | ICLR 2026 |
| [Code Graph Model (CGM): A Graph-Integrated Large Language Model for Repository-Level Software Engineering Tasks](wiki/papers/code-graph-model-cgm-a-graph-integrated-large-language-model-for-reposit-fc8ba6e3.md) | arXiv 2025 |
| [DomAgent: Leveraging Knowledge Graphs and Case-Based Reasoning for Domain-Specific Code Generation](wiki/papers/domagent-leveraging-knowledge-graphs-and-case-based-reasoning-for-domain-354f2e9a.md) | AAMAS 2026 |
| [CodePlan: Repository-Level Coding Using LLMs and Planning](wiki/papers/codeplan-repository-level-coding-using-llms-and-planning-5eaa08c2.md) | FSE 2024 |
| [LocAgent: Graph-Guided LLM Agents for Code Localization](wiki/papers/locagent-graph-guided-llm-agents-for-code-localization-b228ca3a.md) | ACL 2025 |
| [VerilogCoder: Autonomous Verilog Coding Agents with Graph-based Planning and Abstract Syntax Tree (AST)-based Waveform Tracing Tool](wiki/papers/verilogcoder-autonomous-verilog-coding-agents-with-graph-based-planning-98b26fa1.md) | AAAI 2025 |

#### Search-Based Planning

| Paper | Venue |
| --- | --- |
| [Planning in Natural Language Improves LLM Search for Code Generation](wiki/papers/planning-in-natural-language-improves-llm-search-for-code-generation-1db11e25.md) | ICLR 2025 |
| [Tree-of-Code: A Self-Growing Tree Framework for End-to-End Code Generation and Execution in Complex Tasks](wiki/papers/tree-of-code-a-self-growing-tree-framework-for-end-to-end-code-generatio-3267c41e.md) | ACL 2025 Findings |
| [Let's Revise Step-by-Step: A Unified Local Search Framework for Code Generation with LLMs](wiki/papers/let-s-revise-step-by-step-a-unified-local-search-framework-for-code-gene-76848ad2.md) | NeurIPS 2025 |
| [Meta-Harness: End-to-End Optimization of Model Harnesses](wiki/papers/meta-harness-end-to-end-optimization-of-model-harnesses-b6972253.md) | arXiv 2026 |
| [DARS: Dynamic Action Re-Sampling to Enhance Coding Agent Performance by Adaptive Tree Traversal](wiki/papers/dars-dynamic-action-re-sampling-to-enhance-coding-agent-performance-by-a-a3cc9f74.md) | ACL 2025 |
| [Generating Code World Models with Large Language Models Guided by Monte Carlo Tree Search](wiki/papers/generating-code-world-models-with-large-language-models-guided-by-monte-cd46fb8a.md) | NeurIPS 2024 |
| [CodeTree: Agent-guided Tree Search for Code Generation with Large Language Models](wiki/papers/codetree-agent-guided-tree-search-for-code-generation-with-large-languag-8f601498.md) | NAACL 2025 |
| [RethinkMCTS: Refining Erroneous Thoughts in Monte Carlo Tree Search for Code Generation](wiki/papers/rethinkmcts-refining-erroneous-thoughts-in-monte-carlo-tree-search-for-c-590517d9.md) | EMNLP 2025 |
| [SFS: Smarter Code Space Search Improves LLM Inference Scaling](wiki/papers/sfs-smarter-code-space-search-improves-llm-inference-scaling-6098e9dd.md) | ICLR 2025 |

#### Orchestration-Based Planning

| Paper | Venue |
| --- | --- |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [AutoSafeCoder: A Multi-Agent Framework for Securing LLM Code Generation through Static Analysis and Fuzz Testing](wiki/papers/autosafecoder-a-multi-agent-framework-for-securing-llm-code-generation-t-7f525db3.md) | arXiv 2024 |
| [CodeCoR: An LLM-based self-reflective multi-agent framework for code generation](wiki/papers/codecor-an-llm-based-self-reflective-multi-agent-framework-for-code-gene-6534041a.md) | arXiv 2025 |
| [Multi-Agent Code-Orchestrated Generation for Reliable Infrastructure-as-Code](wiki/papers/multi-agent-code-orchestrated-generation-for-reliable-infrastructure-as-0731bf8d.md) | arXiv 2025 |
| [SGAgent: Suggestion-Guided LLM-Based Multi-Agent Framework for Repository-Level Software Repair](wiki/papers/sgagent-suggestion-guided-llm-based-multi-agent-framework-for-repository-afa4565f.md) | arXiv 2026 |
| [Requirements Development and Formalization for Reliable Code Generation: A Multi-Agent Vision](wiki/papers/requirements-development-and-formalization-for-reliable-code-generation-21117dfd.md) | ASE 2025 |
| [AlgoForge: Specializing Code Generation Agents through Collaborative Reinforcement Learning](wiki/papers/algoforge-specializing-code-generation-agents-through-collaborative-rein-d8199d35.md) | 2025 |
| [MapCoder: Multi-Agent Code Generation for Competitive Problem Solving](wiki/papers/mapcoder-multi-agent-code-generation-for-competitive-problem-solving-93d3b041.md) | ACL 2024 |
| [Blueprint2Code: a multi-agent pipeline for reliable code generation via blueprint planning and repair](wiki/papers/blueprint2code-a-multi-agent-pipeline-for-reliable-code-generation-via-b-dcaf0320.md) | Frontiers in AI 2025 |
| [AdaCoder: Adaptive Prompt Compression for Programmatic Visual Question Answering](wiki/papers/adacoder-adaptive-prompt-compression-for-programmatic-visual-question-an-f92d8a3f.md) | ACM MM 2024 |
### 🧠 Memory and Context Engineering

Memory in code-as-agent-harness systems is a state-management layer: which information stays in the active context, which is compacted, and which is offloaded to durable external storage.

#### Working Memory

| Paper | Venue |
| --- | --- |
| [On the Failure of Latent State Persistence in Large Language Models](wiki/papers/on-the-failure-of-latent-state-persistence-in-large-language-models-4d76db90.md) | arXiv 2025 |
| [Live-SWE-agent: Can Software Engineering Agents Self-Evolve on the Fly?](wiki/papers/live-swe-agent-can-software-engineering-agents-self-evolve-on-the-fly-22ad6116.md) | arXiv 2025 |
| [CodeMem: Architecting Reproducible Agents via Dynamic MCP and Procedural Memory](wiki/papers/codemem-architecting-reproducible-agents-via-dynamic-mcp-and-procedural-51c5353a.md) | arXiv 2025 |
| [RepairAgent: An Autonomous, LLM-Based Agent for Program Repair](wiki/papers/repairagent-an-autonomous-llm-based-agent-for-program-repair-209c4f7c.md) | ICSE 2025 |
| [Agentless: Demystifying LLM-based Software Engineering Agents](wiki/papers/agentless-demystifying-llm-based-software-engineering-agents-c52036c5.md) | FSE 2025 |
| [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](wiki/papers/swe-agent-agent-computer-interfaces-enable-automated-software-engineerin-cec5f092.md) | NeurIPS 2024 |

#### Semantic Memory

| Paper | Venue |
| --- | --- |
| [From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs](wiki/papers/from-human-memory-to-ai-memory-a-survey-on-memory-mechanisms-in-the-era-e6282751.md) | arXiv 2025 |
| [Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey](wiki/papers/rethinking-memory-mechanisms-of-foundation-agents-in-the-second-half-a-s-0d186302.md) | arXiv 2026 |
| [AgentSM: Semantic Memory for Agentic Text-to-SQL](wiki/papers/agentsm-semantic-memory-for-agentic-text-to-sql-f4f1c8a4.md) | arXiv 2026 |
| [A Survey on Large Language Models for Code Generation](wiki/papers/a-survey-on-large-language-models-for-code-generation-28453085.md) | TOSEM 2026 |
| [RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation](wiki/papers/repocoder-repository-level-code-completion-through-iterative-retrieval-a-ec3dd909.md) | EMNLP 2023 |
| [AutoCodeRover: Autonomous Program Improvement](wiki/papers/autocoderover-autonomous-program-improvement-ae9813ae.md) | ISSTA 2024 |
| [CodeAgent: Enhancing Code Generation with Tool-Integrated Agent Systems for Real-World Repo-level Coding Challenges](wiki/papers/codeagent-enhancing-code-generation-with-tool-integrated-agent-systems-f-00f877e6.md) | ACL 2024 |
| [A Survey on the Memory Mechanism of Large Language Model-Based Agents](wiki/papers/a-survey-on-the-memory-mechanism-of-large-language-model-based-agents-85c8a24d.md) | TOIS 2025 |
#### Experiential Memory

| Paper | Venue |
| --- | --- |
| [Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory](wiki/papers/evo-memory-benchmarking-llm-agent-test-time-learning-with-self-evolving-63ad13df.md) | arXiv 2025 |
| [MemGovern: Enhancing Code Agents through Learning from Governed Human Experiences](wiki/papers/memgovern-enhancing-code-agents-through-learning-from-governed-human-exp-acb2227b.md) | arXiv 2026 |
| [Leveraging Prior Experience: An Expandable Auxiliary Knowledge Base for Text-to-SQL](wiki/papers/leveraging-prior-experience-an-expandable-auxiliary-knowledge-base-for-t-f8878327.md) | arXiv 2024 |
| [Towards Large Language Models with Human-Like Episodic Memory](wiki/papers/towards-large-language-models-with-human-like-episodic-memory-d4057701.md) | Trends in Cognitive Sciences 2025 |
| [Episodic Memories Generation and Evaluation Benchmark for Large Language Models](wiki/papers/episodic-memories-generation-and-evaluation-benchmark-for-large-language-0f9be0d5.md) | ICLR 2025 |
| [ExpeL: LLM Agents Are Experiential Learners](wiki/papers/expel-llm-agents-are-experiential-learners-ddcdf54b.md) | AAAI 2024 |

#### Long-Term Memory

| Paper | Venue |
| --- | --- |
| [Memex(RL): Scaling Long-Horizon LLM Agents via Indexed Experience Memory](wiki/papers/memex-rl-scaling-long-horizon-llm-agents-via-indexed-experience-memory-5d1af80e.md) | arXiv 2026 |
| [Mem-Gallery: Benchmarking Multimodal Long-Term Conversational Memory for MLLM Agents](wiki/papers/mem-gallery-benchmarking-multimodal-long-term-conversational-memory-for-fa3a819e.md) | arXiv 2026 |
| [MemGPT: Towards LLMs as Operating Systems](wiki/papers/memgpt-towards-llms-as-operating-systems-78d62a8d.md) | arXiv 2023 |
| [Your Code Agent Can Grow Alongside You with Structured Memory](wiki/papers/your-code-agent-can-grow-alongside-you-with-structured-memory-641509f7.md) | arXiv 2026 |
| [TALM: Dynamic Tree-Structured Multi-Agent Framework with Long-Term Memory for Scalable Code Generation](wiki/papers/talm-dynamic-tree-structured-multi-agent-framework-with-long-term-memory-803e8032.md) | arXiv 2025 |
| [Memory OS of AI Agent](wiki/papers/memory-os-of-ai-agent-24598978.md) | EMNLP 2025 |
| [Evaluating Very Long-Term Conversational Memory of LLM Agents](wiki/papers/evaluating-very-long-term-conversational-memory-of-llm-agents-016e4f9e.md) | ACL 2024 |

#### Multi-Agent Memory

| Paper | Venue |
| --- | --- |
| [SWE-Debate: Competitive Multi-Agent Debate for Software Issue Resolution](wiki/papers/swe-debate-competitive-multi-agent-debate-for-software-issue-resolution-9ca4b59e.md) | ICSE 2026 |
| [GameGPT: Multi-agent Collaborative Framework for Game Development](wiki/papers/gamegpt-multi-agent-collaborative-framework-for-game-development-d268798a.md) | arXiv 2023 |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [MIRIX: Multi-Agent Memory System for LLM-Based Agents](wiki/papers/mirix-multi-agent-memory-system-for-llm-based-agents-da5964e8.md) | arXiv 2025 |
| [Self-Organized Agents: A LLM Multi-Agent Framework toward Ultra Large-Scale Code Generation and Optimization](wiki/papers/self-organized-agents-a-llm-multi-agent-framework-toward-ultra-large-sca-db30a15e.md) | arXiv 2024 |
| [Compressing Code Context for LLM-based Issue Resolution](wiki/papers/compressing-code-context-for-llm-based-issue-resolution-f6e7f2b6.md) | arXiv 2026 |
| [Scaling Long-Horizon LLM Agent via Context-Folding](wiki/papers/scaling-long-horizon-llm-agent-via-context-folding-309169cb.md) | arXiv 2025 |
| [LongCLI-Bench: A Preliminary Benchmark and Study for Long-horizon Agentic Programming in Command-Line Interfaces](wiki/papers/longcli-bench-a-preliminary-benchmark-and-study-for-long-horizon-agentic-87630a87.md) | arXiv 2026 |
| [SWE-Bench: Can Language Models Resolve Real-World GitHub Issues?](wiki/papers/swe-bench-can-language-models-resolve-real-world-github-issues-3deec234.md) | ICLR 2024 |
| [G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems](wiki/papers/g-memory-tracing-hierarchical-memory-for-multi-agent-systems-cebec3f0.md) | NeurIPS 2025 |

### 🔧 Tool Usage for Code Agents

Tool usage is the action and observation layer of the code-agent harness: agents search repositories, inspect files, edit code, run commands, execute tests, call APIs, and verify intermediate results — all under typed schemas, sandboxes, and lifecycle hooks.

#### Function-Oriented Tool Use

| Paper | Venue |
| --- | --- |
| [ToolCoder: Teach Code Generation Models to use API search tools](wiki/papers/toolcoder-teach-code-generation-models-to-use-api-search-tools-fd0de352.md) | arXiv 2023 |
| [CodeQA: Advanced Programming Question-Answering Using LLM Agent and RAG](wiki/papers/codeqa-advanced-programming-question-answering-using-llm-agent-and-rag-1d7fa345.md) | IEEE TENCON 2024 |
| [RAG-Based AI Agents for Enterprise Software Development: Implementation Patterns and Production Deployment](wiki/papers/rag-based-ai-agents-for-enterprise-software-development-implementation-p-10713266.md) | 2025 |
| [The Devil Is in the Tails: How Long-Tailed Code Distributions Impact Large Language Models](wiki/papers/the-devil-is-in-the-tails-how-long-tailed-code-distributions-impact-larg-baff9109.md) | ASE 2023 |

#### Environment-Interaction Tool Use

| Paper | Venue |
| --- | --- |
| [Environment-in-the-Loop: Rethinking Code Migration with LLM-based Agents](wiki/papers/environment-in-the-loop-rethinking-code-migration-with-llm-based-agents-8cf718b7.md) | arXiv 2026 |
| [Test-Time Adaptation for LLM Agents via Environment Interaction](wiki/papers/test-time-adaptation-for-llm-agents-via-environment-interaction-6d7e2156.md) | ICLR 2026 |

#### Verification-Driven Tool Use

| Paper | Venue |
| --- | --- |
| [VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation](wiki/papers/veriguard-enhancing-llm-agent-safety-via-verified-code-generation-a5861f4a.md) | arXiv 2025 |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [Agents4PLC: Automating Closed-loop PLC Code Generation and Verification in Industrial Control Systems using LLM-based Agents](wiki/papers/agents4plc-automating-closed-loop-plc-code-generation-and-verification-i-7f843ef1.md) | arXiv 2025 |

#### Workflow-Orchestration Tool Use

| Paper | Venue |
| --- | --- |
| [ToolNet: Connecting Large Language Models with Massive Tools via Tool Graph](wiki/papers/toolnet-connecting-large-language-models-with-massive-tools-via-tool-gra-3ea5c7f3.md) | arXiv 2024 |
| [ControlLLM: Augment Language Models with Tools by Searching on Graphs](wiki/papers/controlllm-augment-language-models-with-tools-by-searching-on-graphs-8e530226.md) | ECCV 2024 |
| [Agent Harness for Large Language Model Agents: A Survey](wiki/papers/agent-harness-for-large-language-model-agents-a-survey-1aa3cdd9.md) | Preprints 2026 |
| [Executable Code Actions Elicit Better LLM Agents](wiki/papers/executable-code-actions-elicit-better-llm-agents-31b16f13.md) | ICML 2024 |
| [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](wiki/papers/openhands-an-open-platform-for-ai-software-developers-as-generalist-agen-75300600.md) | ICLR 2025 |
| [On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub](wiki/papers/on-the-use-of-agentic-coding-an-empirical-study-of-pull-requests-on-gith-f8dcf311.md) | TOSEM 2025 |

### 🧪 Feedback-Guided Iterative Debugging

Iterative debugging closes the harness loop: development environments expose feedback (compiler diagnostics, runtime errors, tests, critique), and the agent transforms these signals into diagnosis, revision, and progressively better debugging behavior.

#### Development Environments for Agentic Coding

##### Contextual Environments for Repository-Aware Generation

| Paper | Venue |
| --- | --- |
| [On the Impacts of Contexts on Repository-Level Code Generation](wiki/papers/on-the-impacts-of-contexts-on-repository-level-code-generation-09ffc66e.md) | NAACL 2025 Findings |
| [A Survey on Model Context Protocol: Architecture, State-of-the-art, Challenges and Future Directions](wiki/papers/a-survey-on-model-context-protocol-architecture-state-of-the-art-challen-51ec4866.md) | TechRxiv 2025 |
| [CodexGraph: Bridging Large Language Models and Code Repositories via Code Graph Databases](wiki/papers/codexgraph-bridging-large-language-models-and-code-repositories-via-code-997803fa.md) | NAACL 2025 |
| [RepoAgent: An LLM-Powered Open-Source Framework for Repository-level Code Documentation Generation](wiki/papers/repoagent-an-llm-powered-open-source-framework-for-repository-level-code-3398bf12.md) | EMNLP 2024 (Demo) |
| [Knowledge Graph Based Repository-Level Code Generation](wiki/papers/knowledge-graph-based-repository-level-code-generation-95ecf625.md) | LLM4Code@ICSE 2025 |
| [From Glue-Code to Protocols: A Critical Analysis of A2A and MCP Integration for Scalable Agent Systems](wiki/papers/from-glue-code-to-protocols-a-critical-analysis-of-a2a-and-mcp-integrati-6c83ea89.md) | arXiv 2025 |
| [Retrieval-Augmented Code Generation: A Survey with Focus on Repository-Level Approaches](wiki/papers/retrieval-augmented-code-generation-a-survey-with-focus-on-repository-le-1fc7d7d7.md) | arXiv 2026 |
| [A³-CodGen: A Repository-Level Code Generation Framework for Code Reuse with Local-Aware, Global-Aware, and Third-Party-Library-Aware](wiki/papers/a3-codgen-a-repository-level-code-generation-framework-for-code-reuse-wi-87d642f1.md) | TSE 2024 |

##### Interactive Environments for Human–LLM Collaboration

| Paper | Venue |
| --- | --- |
| [Conversational AI as a Coding Assistant: Understanding Programmers' Interactions with and Expectations from Large Language Models for Coding](wiki/papers/conversational-ai-as-a-coding-assistant-understanding-programmers-intera-3f99131f.md) | arXiv 2025 |
| [The Design Space of LLM-Based AI Coding Assistants: An Analysis of 90 Systems in Academia and Industry](wiki/papers/the-design-space-of-llm-based-ai-coding-assistants-an-analysis-of-90-sys-be6d37bd.md) | VL/HCC 2025 |
| [Language Server Protocol: Defines a Common Protocol for Language Servers](wiki/papers/language-server-protocol-defines-a-common-protocol-for-language-servers-0bbbcbdf.md) \[Spec\] | — |
| [Deductive Verification via the Debug Adapter Protocol](wiki/papers/deductive-verification-via-the-debug-adapter-protocol-ff625d05.md) | arXiv 2021 |
| [Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions](wiki/papers/model-context-protocol-mcp-landscape-security-threats-and-future-researc-a33b66a1.md) | TOSEM 2025 |
| [The Programmer's Assistant: Conversational Interaction with a Large Language Model for Software Development](wiki/papers/the-programmer-s-assistant-conversational-interaction-with-a-large-langu-aae4ddb1.md) | IUI 2023 |
| [Human-AI Experience in Integrated Development Environments: A Systematic Literature Review](wiki/papers/human-ai-experience-in-integrated-development-environments-a-systematic-5a126d05.md) | Empirical Software Engineering 2026 |

##### Execution and Validation Environments

| Paper | Venue |
| --- | --- |
| [RepoST: Scalable Repository-Level Coding Environment Construction with Sandbox Testing](wiki/papers/repost-scalable-repository-level-coding-environment-construction-with-sa-4560b879.md) | arXiv 2025 |
| [Klear-CodeTest: Scalable Test Case Generation for Code Reinforcement Learning](wiki/papers/klear-codetest-scalable-test-case-generation-for-code-reinforcement-lear-7e249900.md) | arXiv 2025 |
| [FeedbackEval: A Benchmark for Evaluating Large Language Models in Feedback-Driven Code Repair Tasks](wiki/papers/feedbackeval-a-benchmark-for-evaluating-large-language-models-in-feedbac-b0a563d7.md) | arXiv 2026 |
| [LLMLOOP: Improving LLM-Generated Code and Tests Through Automated Iterative Feedback Loops](wiki/papers/llmloop-improving-llm-generated-code-and-tests-through-automated-iterati-96916cfd.md) | ICSME 2025 |
| [Openagentsafety: A comprehensive framework for evaluating real-world ai agent safety](wiki/papers/openagentsafety-a-comprehensive-framework-for-evaluating-real-world-ai-a-d60c0cfd.md) | ICLR 2026 |
| [Kubeintellect: A modular llm-orchestrated agent framework for end-to-end kubernetes management](wiki/papers/kubeintellect-a-modular-llm-orchestrated-agent-framework-for-end-to-end-91b09c8c.md) | arXiv 2025 |
| [MLDebugging: Towards Benchmarking Code Debugging Across Multi-Library Scenarios](wiki/papers/mldebugging-towards-benchmarking-code-debugging-across-multi-library-sce-7b5216a6.md) | ACL 2025 Findings |
| [ECCO: Can We Improve Model-Generated Code Efficiency Without Sacrificing Functional Correctness?](wiki/papers/ecco-can-we-improve-model-generated-code-efficiency-without-sacrificing-79640c67.md) | EMNLP 2024 |

##### Engineering Platforms for Deployment and Workflow Integration

| Paper | Venue |
| --- | --- |
| [LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision, and the Road Ahead](wiki/papers/llm-based-multi-agent-systems-for-software-engineering-literature-review-c0991972.md) | TOSEM 2024 |
| [AgentMesh: A Cooperative Multi-Agent Generative AI Framework for Software Development Automation](wiki/papers/agentmesh-a-cooperative-multi-agent-generative-ai-framework-for-software-dfaf87f2.md) | arXiv 2025 |
| [ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework](wiki/papers/almas-an-autonomous-llm-based-multi-agent-software-engineering-framework-dbf12723.md) | arXiv 2025 |
| [From challenges to metrics: An LLM-driven DevOps recommendation system grounded in evidence-based mappings](wiki/papers/from-challenges-to-metrics-an-llm-driven-devops-recommendation-system-gr-ca321407.md) | Array 2025 |
| [AI Augmented CI/CD Pipelines: From Code Commit to Production with Autonomous Decisions](wiki/papers/ai-augmented-ci-cd-pipelines-from-code-commit-to-production-with-autonom-2fd5abcb.md) | IEEE FLLM 2025 |
| [A Multi-Agent Coding Assistant for Cloud-Native Development: From Requirements to Deployable Microservices](wiki/papers/a-multi-agent-coding-assistant-for-cloud-native-development-from-require-65f216a5.md) | Preprints 2025 |
| [Continuous QoS-compliant Orchestration in the Cloud-Edge Continuum](wiki/papers/continuous-qos-compliant-orchestration-in-the-cloud-edge-continuum-b71e31c1.md) | Software: Practice and Experience 2024 |
| [From Code Generation to AI Collaboration: The Role of Multi-Agent Systems in Software Engineering](wiki/papers/from-code-generation-to-ai-collaboration-the-role-of-multi-agent-systems-3dc761e2.md) | 2025 |
| [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversations](wiki/papers/autogen-enabling-next-gen-llm-applications-via-multi-agent-conversations-368dedbe.md) | COLM 2024 |
#### Feedback Mechanisms for Iterative Debugging

##### Compilation and Static-Analysis Feedback

| Paper | Venue |
| --- | --- |
| [The Debugging Decay Index: Rethinking Debugging Strategies for Code LLMs](wiki/papers/the-debugging-decay-index-rethinking-debugging-strategies-for-code-llms-fe8e8f40.md) | arXiv 2025 |
| [Helping LLMs Improve Code Generation Using Feedback from Testing and Static Analysis](wiki/papers/helping-llms-improve-code-generation-using-feedback-from-testing-and-sta-d854c7bb.md) | Discover Artificial Intelligence 2024 |
| [Enhancing LLM Code Generation: A Systematic Evaluation of Multi-Agent Collaboration and Runtime Debugging for Improved Accuracy, Reliability, and Latency](wiki/papers/enhancing-llm-code-generation-a-systematic-evaluation-of-multi-agent-col-e340c491.md) | arXiv 2025 |
| [Iterative Refinement of Project-Level Code Context for Precise Code Generation with Compiler Feedback](wiki/papers/iterative-refinement-of-project-level-code-context-for-precise-code-gene-88f11f11.md) | ACL 2024 Findings |
| [Static Analysis as a Feedback Loop: Enhancing LLM-Generated Code Beyond Correctness](wiki/papers/static-analysis-as-a-feedback-loop-enhancing-llm-generated-code-beyond-c-dac7eeb9.md) | arXiv 2025 |

##### Runtime Error and Exception Feedback

| Paper | Venue |
| --- | --- |
| [Towards Agentic Runtime Healing](wiki/papers/towards-agentic-runtime-healing-1b6382b2.md) | arXiv 2024 |
| [Large Language Model Guided Self-Debugging Code Generation](wiki/papers/large-language-model-guided-self-debugging-code-generation-eee322a7.md) | arXiv 2025 |
| [Code Repair with LLMs gives an Exploration-Exploitation Tradeoff](wiki/papers/code-repair-with-llms-gives-an-exploration-exploitation-tradeoff-915c1296.md) | NeurIPS 2024 |
| [Debug like a Human: A Large Language Model Debugger via Verifying Runtime Execution Step by Step](wiki/papers/debug-like-a-human-a-large-language-model-debugger-via-verifying-runtime-6a2d11cf.md) | ACL 2024 Findings |

##### Test-Based Execution Feedback

| Paper | Venue |
| --- | --- |
| [Teaching Large Language Models to Self-Debug](wiki/papers/teaching-large-language-models-to-self-debug-6597977d.md) | arXiv 2023 |
| [Learning to generate unit tests for automated debugging](wiki/papers/learning-to-generate-unit-tests-for-automated-debugging-bfce1bef.md) | COLM 2025 |
| [TestART: Improving LLM-Based Unit Testing via Co-Evolution of Automated Generation and Repair Iteration](wiki/papers/testart-improving-llm-based-unit-testing-via-co-evolution-of-automated-g-f71d7f91.md) | arXiv 2024 |
| [From Code to Correctness: Closing the Last Mile of Code Generation with Hierarchical Debugging](wiki/papers/from-code-to-correctness-closing-the-last-mile-of-code-generation-with-h-fefea8fa.md) | ICSE 2026 |
| [Revisit Self-Debugging with Self-Generated Tests for Code Generation](wiki/papers/revisit-self-debugging-with-self-generated-tests-for-code-generation-148d474f.md) | ACL 2025 |
| [LLM-Based Test-Driven Interactive Code Generation: User Study and Empirical Evaluation](wiki/papers/llm-based-test-driven-interactive-code-generation-user-study-and-empiric-81264c4e.md) | TSE 2024 |

##### Critique-Driven Feedback (Human or Auxiliary Agents)

| Paper | Venue |
| --- | --- |
| [Interactive Debugging and Steering of Multi-Agent AI Systems](wiki/papers/interactive-debugging-and-steering-of-multi-agent-ai-systems-7e120797.md) | CHI 2025 |
| [RGD: Multi-LLM Based Agent Debugger via Refinement and Generation Guidance](wiki/papers/rgd-multi-llm-based-agent-debugger-via-refinement-and-generation-guidanc-1085bd43.md) | International Conference on Agents 2024 |

##### Feedback-Driven Debugging and Self-Improvement

| Paper | Venue |
| --- | --- |
| [Teaching Your Models to Understand Code via Focal Preference Alignment](wiki/papers/teaching-your-models-to-understand-code-via-focal-preference-alignment-6e13c3ba.md) | arXiv 2025 |
| [ReVeal: Self-Evolving Code Agents via Reliable Self-Verification](wiki/papers/reveal-self-evolving-code-agents-via-reliable-self-verification-bde03aaa.md) | NeurIPS 2025 |

## 👥 Scaling the Harness: Multi-Agent Code-Centric Systems

When multiple agents operate over code, the harness must coordinate roles, share intermediate artifacts, maintain common state, and verify collective progress through repositories, tests, traces, and structured workflows.

![Scaling the harness](figs/scaling_harness.png)

### 🎭 Functional Role Specialization

Distinct agents own slices of the shared code harness — synthesis, understanding, verification, execution, and planning.

#### Program Synthesis Agents

| Paper | Venue |
| --- | --- |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](wiki/papers/metagpt-meta-programming-for-a-multi-agent-collaborative-framework-39846716.md) | ICLR 2024 |
| [ChatDev: Communicative Agents for Software Development](wiki/papers/chatdev-communicative-agents-for-software-development-204be492.md) | ACL 2024 |
| [MAGE: A multi-agent engine for automated RTL code generation](wiki/papers/mage-a-multi-agent-engine-for-automated-rtl-code-generation-408dbf3c.md) | DAC 2025 |
| [Self-collaboration Code Generation via ChatGPT](wiki/papers/self-collaboration-code-generation-via-chatgpt-65908e00.md) | TOSEM 2024 |

#### Program Understanding Agents

| Paper | Venue |
| --- | --- |
| [HyperAgent: Generalist software engineering agents to solve coding tasks at scale](wiki/papers/hyperagent-generalist-software-engineering-agents-to-solve-coding-tasks-73f787cd.md) | arXiv 2024 |
| [Lingma SWE-GPT: An Open Development-Process-Centric Language Model for Automated Software Improvement](wiki/papers/lingma-swe-gpt-an-open-development-process-centric-language-model-for-au-41a1427b.md) | ISSTA 2025 |
| [CleanAgent: Automating data standardization with LLM-based agents](wiki/papers/cleanagent-automating-data-standardization-with-llm-based-agents-d311ae7b.md) | arXiv 2024 |
| [MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution](wiki/papers/magis-llm-based-multi-agent-framework-for-github-issue-resolution-16bb79d4.md) | NeurIPS 2024 |

#### Verification Agents

| Paper | Venue |
| --- | --- |
| [QualityFlow: An agentic workflow for program synthesis controlled by LLM quality checks](wiki/papers/qualityflow-an-agentic-workflow-for-program-synthesis-controlled-by-llm-e28c069c.md) | arXiv 2025 |
| [AutoSafeCoder: A Multi-Agent Framework for Securing LLM Code Generation through Static Analysis and Fuzz Testing](wiki/papers/autosafecoder-a-multi-agent-framework-for-securing-llm-code-generation-t-7f525db3.md) | arXiv 2024 |
| [Hallucination to Consensus: Multi-Agent LLMs for End-to-End JUnit Test Generation](wiki/papers/hallucination-to-consensus-multi-agent-llms-for-end-to-end-junit-test-ge-4f02da22.md) | arXiv 2025 |

#### Execution Agents

| Paper | Venue |
| --- | --- |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [HyperAgent: Generalist software engineering agents to solve coding tasks at scale](wiki/papers/hyperagent-generalist-software-engineering-agents-to-solve-coding-tasks-73f787cd.md) | arXiv 2024 |
| [MAGE: A multi-agent engine for automated RTL code generation](wiki/papers/mage-a-multi-agent-engine-for-automated-rtl-code-generation-408dbf3c.md) | DAC 2025 |

#### Planning Agents

| Paper | Venue |
| --- | --- |
| [Self-Organized Agents: A LLM Multi-Agent Framework toward Ultra Large-Scale Code Generation and Optimization](wiki/papers/self-organized-agents-a-llm-multi-agent-framework-toward-ultra-large-sca-db30a15e.md) | arXiv 2024 |
| [Self-Evolving Multi-Agent Collaboration Networks for Software Development](wiki/papers/self-evolving-multi-agent-collaboration-networks-for-software-developmen-5db1ddb8.md) | ICLR 2025 |
| [SOEN-101: Code Generation by Emulating Software Process Models Using Large Language Model Agents](wiki/papers/soen-101-code-generation-by-emulating-software-process-models-using-larg-7914f86c.md) | ICSE 2025 |

### 💬 Interaction Modes

Code-centric multi-agent interaction is artifact-mediated: agents observe and modify shared code, and grounding comes from the objective state exposed by execution.

#### Collaborative Synthesis

| Paper | Venue |
| --- | --- |
| [CodePori: Large-Scale System for Autonomous Software Development Using Multi-Agent Technology](wiki/papers/codepori-large-scale-system-for-autonomous-software-development-using-mu-4604dadc.md) | arXiv 2024 |
| [A Pair Programming Framework for Code Generation via Multi-Plan Exploration and Feedback-Driven Refinement](wiki/papers/a-pair-programming-framework-for-code-generation-via-multi-plan-explorat-41a711e2.md) | ASE 2024 |

#### Critique and Repair

| Paper | Venue |
| --- | --- |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [SEW: Self-evolving agentic workflows for automated code generation](wiki/papers/sew-self-evolving-agentic-workflows-for-automated-code-generation-db9d578a.md) | arXiv 2025 |

#### Adversarial Validation

| Paper | Venue |
| --- | --- |
| [AutoSafeCoder: A Multi-Agent Framework for Securing LLM Code Generation through Static Analysis and Fuzz Testing](wiki/papers/autosafecoder-a-multi-agent-framework-for-securing-llm-code-generation-t-7f525db3.md) | arXiv 2024 |
| [MAGE: A multi-agent engine for automated RTL code generation](wiki/papers/mage-a-multi-agent-engine-for-automated-rtl-code-generation-408dbf3c.md) | DAC 2025 |

#### Reasoning Debate

| Paper | Venue |
| --- | --- |
| [ChatDev: Communicative Agents for Software Development](wiki/papers/chatdev-communicative-agents-for-software-development-204be492.md) | ACL 2024 |
| [Hallucination to Consensus: Multi-Agent LLMs for End-to-End JUnit Test Generation](wiki/papers/hallucination-to-consensus-multi-agent-llms-for-end-to-end-junit-test-ge-4f02da22.md) | arXiv 2025 |

### 🕸️ Workflow Topology

Topology of agent interaction (chain, cyclic, hierarchical, star, adaptive) is one of the most consequential design decisions in multi-agent code generation.

#### Pre-Defined Heuristic Topologies (Waterfall / Iterative / Hierarchical / Star)

| Paper | Venue |
| --- | --- |
| [ChatDev: Communicative Agents for Software Development](wiki/papers/chatdev-communicative-agents-for-software-development-204be492.md) | ACL 2024 |
| [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](wiki/papers/metagpt-meta-programming-for-a-multi-agent-collaborative-framework-39846716.md) | ICLR 2024 |
| [L2MAC: Large language model automatic computer for extensive code generation](wiki/papers/l2mac-large-language-model-automatic-computer-for-extensive-code-generat-4f91c91d.md) | ICLR 2024 |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [MAGE: A multi-agent engine for automated RTL code generation](wiki/papers/mage-a-multi-agent-engine-for-automated-rtl-code-generation-408dbf3c.md) | DAC 2025 |
| [HyperAgent: Generalist software engineering agents to solve coding tasks at scale](wiki/papers/hyperagent-generalist-software-engineering-agents-to-solve-coding-tasks-73f787cd.md) | arXiv 2024 |
| [Self-Organized Agents: A LLM Multi-Agent Framework toward Ultra Large-Scale Code Generation and Optimization](wiki/papers/self-organized-agents-a-llm-multi-agent-framework-toward-ultra-large-sca-db30a15e.md) | arXiv 2024 |
| [Hallucination to Consensus: Multi-Agent LLMs for End-to-End JUnit Test Generation](wiki/papers/hallucination-to-consensus-multi-agent-llms-for-end-to-end-junit-test-ge-4f02da22.md) | arXiv 2025 |

#### Objective-Driven and Adaptive Topologies

| Paper | Venue |
| --- | --- |
| [FlowReasoner: Reinforcing Query-Level Meta-Agents](wiki/papers/flowreasoner-reinforcing-query-level-meta-agents-53cd98dd.md) | arXiv 2025 |
| [BOAD: Discovering Hierarchical Software Engineering Agents via Bandit Optimization](wiki/papers/boad-discovering-hierarchical-software-engineering-agents-via-bandit-opt-58fffdc3.md) | arXiv 2025 |
| [SEW: Self-evolving agentic workflows for automated code generation](wiki/papers/sew-self-evolving-agentic-workflows-for-automated-code-generation-db9d578a.md) | arXiv 2025 |

### ⚡ Execution Feedback Integration

Code is uniquely executable, producing objective oracle signals that anchor multi-agent coordination.

#### Compiler and Syntax Feedback

| Paper | Venue |
| --- | --- |
| [ChatDev: Communicative Agents for Software Development](wiki/papers/chatdev-communicative-agents-for-software-development-204be492.md) | ACL 2024 |
| [L2MAC: Large language model automatic computer for extensive code generation](wiki/papers/l2mac-large-language-model-automatic-computer-for-extensive-code-generat-4f91c91d.md) | ICLR 2024 |

#### Test Pass/Fail Signals

| Paper | Venue |
| --- | --- |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [QualityFlow: An agentic workflow for program synthesis controlled by LLM quality checks](wiki/papers/qualityflow-an-agentic-workflow-for-program-synthesis-controlled-by-llm-e28c069c.md) | arXiv 2025 |

#### Fuzzer Crash Traces

| Paper | Venue |
| --- | --- |
| [AutoSafeCoder: A Multi-Agent Framework for Securing LLM Code Generation through Static Analysis and Fuzz Testing](wiki/papers/autosafecoder-a-multi-agent-framework-for-securing-llm-code-generation-t-7f525db3.md) | arXiv 2024 |

#### Static Analysis Warnings

| Paper | Venue |
| --- | --- |
| [AutoSafeCoder: A Multi-Agent Framework for Securing LLM Code Generation through Static Analysis and Fuzz Testing](wiki/papers/autosafecoder-a-multi-agent-framework-for-securing-llm-code-generation-t-7f525db3.md) | arXiv 2024 |

#### Performance Profiling Results

| Paper | Venue |
| --- | --- |
| [MARCO: Multi-Agent Code Optimization with Real-Time Knowledge Integration for High-Performance Computing](wiki/papers/marco-multi-agent-code-optimization-with-real-time-knowledge-integration-250f4a42.md) | arXiv 2025 |

#### Fine-Grained Simulation Feedback

| Paper | Venue |
| --- | --- |
| [MAGE: A multi-agent engine for automated RTL code generation](wiki/papers/mage-a-multi-agent-engine-for-automated-rtl-code-generation-408dbf3c.md) | DAC 2025 |

### 🔄 Shared-Harness Synchronization

How multi-agent systems maintain a consistent shared view of program state.

#### Shared Blackboard

| Paper | Venue |
| --- | --- |
| [L2MAC: Large language model automatic computer for extensive code generation](wiki/papers/l2mac-large-language-model-automatic-computer-for-extensive-code-generat-4f91c91d.md) | ICLR 2024 |

#### Parallel Branches with Merge

| Paper | Venue |
| --- | --- |
| [HyperAgent: Generalist software engineering agents to solve coding tasks at scale](wiki/papers/hyperagent-generalist-software-engineering-agents-to-solve-coding-tasks-73f787cd.md) | arXiv 2024 |

#### Structured Context Scheduling

| Paper | Venue |
| --- | --- |
| [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](wiki/papers/metagpt-meta-programming-for-a-multi-agent-collaborative-framework-39846716.md) | ICLR 2024 |

#### Hierarchical Memory

| Paper | Venue |
| --- | --- |
| [ChatDev: Communicative Agents for Software Development](wiki/papers/chatdev-communicative-agents-for-software-development-204be492.md) | ACL 2024 |
| [Cogito, ergo sum: A Neurobiologically-Inspired Cognition-Memory-Growth System for Code Generation](wiki/papers/cogito-ergo-sum-a-neurobiologically-inspired-cognition-memory-growth-sys-5cc73587.md) | arXiv 2025 |

#### Agent Pool Scaling

| Paper | Venue |
| --- | --- |
| [Self-Organized Agents: A LLM Multi-Agent Framework toward Ultra Large-Scale Code Generation and Optimization](wiki/papers/self-organized-agents-a-llm-multi-agent-framework-toward-ultra-large-sca-db30a15e.md) | arXiv 2024 |

### 🏛️ Shared Harness Representation

Four levels of formalization for the shared substrate: implicit/file-only, repository-based, execution-based, and blackboard.

#### Implicit / File-Only Representation

| Paper | Venue |
| --- | --- |
| [ChatDev: Communicative Agents for Software Development](wiki/papers/chatdev-communicative-agents-for-software-development-204be492.md) | ACL 2024 |
| [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](wiki/papers/metagpt-meta-programming-for-a-multi-agent-collaborative-framework-39846716.md) | ICLR 2024 |
| [CodeCoR: An LLM-based self-reflective multi-agent framework for code generation](wiki/papers/codecor-an-llm-based-self-reflective-multi-agent-framework-for-code-gene-6534041a.md) | arXiv 2025 |
| [SEW: Self-evolving agentic workflows for automated code generation](wiki/papers/sew-self-evolving-agentic-workflows-for-automated-code-generation-db9d578a.md) | arXiv 2025 |
| [CodePori: Large-Scale System for Autonomous Software Development Using Multi-Agent Technology](wiki/papers/codepori-large-scale-system-for-autonomous-software-development-using-mu-4604dadc.md) | arXiv 2024 |
| [SyncMind: Measuring Agent Out-of-Sync Recovery in Collaborative Software Engineering](wiki/papers/syncmind-measuring-agent-out-of-sync-recovery-in-collaborative-software-add1b25e.md) | ICML 2025 |

#### Repository-Based Representation

| Paper | Venue |
| --- | --- |
| [HyperAgent: Generalist software engineering agents to solve coding tasks at scale](wiki/papers/hyperagent-generalist-software-engineering-agents-to-solve-coding-tasks-73f787cd.md) | arXiv 2024 |
| [Lingma SWE-GPT: An Open Development-Process-Centric Language Model for Automated Software Improvement](wiki/papers/lingma-swe-gpt-an-open-development-process-centric-language-model-for-au-41a1427b.md) | ISSTA 2025 |
#### Execution-Based Representation

| Paper | Venue |
| --- | --- |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [AutoSafeCoder: A Multi-Agent Framework for Securing LLM Code Generation through Static Analysis and Fuzz Testing](wiki/papers/autosafecoder-a-multi-agent-framework-for-securing-llm-code-generation-t-7f525db3.md) | arXiv 2024 |
| [QualityFlow: An agentic workflow for program synthesis controlled by LLM quality checks](wiki/papers/qualityflow-an-agentic-workflow-for-program-synthesis-controlled-by-llm-e28c069c.md) | arXiv 2025 |
| [MARCO: Multi-Agent Code Optimization with Real-Time Knowledge Integration for High-Performance Computing](wiki/papers/marco-multi-agent-code-optimization-with-real-time-knowledge-integration-250f4a42.md) | arXiv 2025 |
| [Hallucination to Consensus: Multi-Agent LLMs for End-to-End JUnit Test Generation](wiki/papers/hallucination-to-consensus-multi-agent-llms-for-end-to-end-junit-test-ge-4f02da22.md) | arXiv 2025 |
| [MAGE: A multi-agent engine for automated RTL code generation](wiki/papers/mage-a-multi-agent-engine-for-automated-rtl-code-generation-408dbf3c.md) | DAC 2025 |

#### Blackboard / Shared-State Representation

| Paper | Venue |
| --- | --- |
| [L2MAC: Large language model automatic computer for extensive code generation](wiki/papers/l2mac-large-language-model-automatic-computer-for-extensive-code-generat-4f91c91d.md) | ICLR 2024 |
| [GameGPT: Multi-agent Collaborative Framework for Game Development](wiki/papers/gamegpt-multi-agent-collaborative-framework-for-game-development-d268798a.md) | arXiv 2023 |
| [Cogito, ergo sum: A Neurobiologically-Inspired Cognition-Memory-Growth System for Code Generation](wiki/papers/cogito-ergo-sum-a-neurobiologically-inspired-cognition-memory-growth-sys-5cc73587.md) | arXiv 2025 |
<!-- | [The Hearsay-II Speech-Understanding System: Integrating Knowledge to Resolve Uncertainty](https://doi.org/10.1145/356810.356816) | CSUR 1980 | -->

### 🎯 Harness-State Convergence

How a multi-agent code system decides the shared harness has reached an acceptable final state.

#### Correctness Convergence (Test-Gated)

| Paper | Venue |
| --- | --- |
| [AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation](wiki/papers/agentcoder-multi-agent-based-code-generation-with-iterative-testing-and-b39082ad.md) | arXiv 2023 |
| [L2MAC: Large language model automatic computer for extensive code generation](wiki/papers/l2mac-large-language-model-automatic-computer-for-extensive-code-generat-4f91c91d.md) | ICLR 2024 |
| [Hallucination to Consensus: Multi-Agent LLMs for End-to-End JUnit Test Generation](wiki/papers/hallucination-to-consensus-multi-agent-llms-for-end-to-end-junit-test-ge-4f02da22.md) | arXiv 2025 |

#### Security Convergence

| Paper | Venue |
| --- | --- |
| [AutoSafeCoder: A Multi-Agent Framework for Securing LLM Code Generation through Static Analysis and Fuzz Testing](wiki/papers/autosafecoder-a-multi-agent-framework-for-securing-llm-code-generation-t-7f525db3.md) | arXiv 2024 |

#### Performance Convergence

| Paper | Venue |
| --- | --- |
| [MARCO: Multi-Agent Code Optimization with Real-Time Knowledge Integration for High-Performance Computing](wiki/papers/marco-multi-agent-code-optimization-with-real-time-knowledge-integration-250f4a42.md) | arXiv 2025 |

#### Score-Based Convergence

| Paper | Venue |
| --- | --- |
| [MAGE: A multi-agent engine for automated RTL code generation](wiki/papers/mage-a-multi-agent-engine-for-automated-rtl-code-generation-408dbf3c.md) | DAC 2025 |
| [CodeCoR: An LLM-based self-reflective multi-agent framework for code generation](wiki/papers/codecor-an-llm-based-self-reflective-multi-agent-framework-for-code-gene-6534041a.md) | arXiv 2025 |
| [Trae Agent: An LLM-based Agent for Software Engineering with Test-time Scaling](wiki/papers/trae-agent-an-llm-based-agent-for-software-engineering-with-test-time-sc-23744e51.md) | arXiv 2025 |

#### Consensus Convergence

| Paper | Venue |
| --- | --- |
| [QualityFlow: An agentic workflow for program synthesis controlled by LLM quality checks](wiki/papers/qualityflow-an-agentic-workflow-for-program-synthesis-controlled-by-llm-e28c069c.md) | arXiv 2025 |

#### Implicit Convergence

| Paper | Venue |
| --- | --- |
| [ChatDev: Communicative Agents for Software Development](wiki/papers/chatdev-communicative-agents-for-software-development-204be492.md) | ACL 2024 |
| [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](wiki/papers/metagpt-meta-programming-for-a-multi-agent-collaborative-framework-39846716.md) | ICLR 2024 |

## 🚀 Applications and Emerging Fields

Code-centric agentic systems become operational in tangible domains where code defines observable state, executable actions, persistent memory, and feedback signals.

![Applications](figs/applications.png)

### 💻 Code Assistants

Repositories, tests, issue threads, and development tools form a persistent program world; assistants act over it as code-centric agents.

#### The Repository as a Persistent Program World

| Paper | Venue |
| --- | --- |
| [RepoCoder: Repository-Level Code Completion through Iterative Retrieval and Generation](wiki/papers/repocoder-repository-level-code-completion-through-iterative-retrieval-a-ec3dd909.md) | EMNLP 2023 |
| [CodexGraph: Bridging Large Language Models and Code Repositories via Code Graph Databases](wiki/papers/codexgraph-bridging-large-language-models-and-code-repositories-via-code-997803fa.md) | NAACL 2025 |
| [AutoCodeRover: Autonomous Program Improvement](wiki/papers/autocoderover-autonomous-program-improvement-ae9813ae.md) | ISSTA 2024 |

#### Agent Harnesses as Executable Development Interfaces

| Paper | Venue |
| --- | --- |
| [Claude Code](wiki/papers/claude-code-7cb0222a.md) \[Blog\] | 2025 |
| [Introducing Codex](wiki/papers/introducing-codex-3452b7f5.md) \[Blog\] | 2025 |
| [About GitHub Copilot Cloud Agent](wiki/papers/about-github-copilot-cloud-agent-a4d6dd96.md) \[Blog\] | 2025 |
| [DeepAgents](wiki/papers/deepagents-40a2320c.md) \[GitHub\] | 2025 |
| [Model Context Protocol](wiki/papers/model-context-protocol-5929925a.md) \[Docs\] | 2024 |
| [Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions](wiki/papers/model-context-protocol-mcp-landscape-security-threats-and-future-researc-a33b66a1.md) | ACM TOSEM 2025 |
| [The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents](wiki/papers/the-openhands-software-agent-sdk-a-composable-and-extensible-foundation-bd61b42b.md) | arXiv 2025 |
| [AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness](wiki/papers/autoharness-improving-llm-agents-by-automatically-synthesizing-a-code-ha-b5805024.md) | arXiv 2026 |
| [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](wiki/papers/agentic-harness-engineering-observability-driven-automatic-evolution-of-32a741f4.md) | arXiv 2026 |
| [Meta-Harness: End-to-End Optimization of Model Harnesses](wiki/papers/meta-harness-end-to-end-optimization-of-model-harnesses-b6972253.md) | arXiv 2026 |
| [Natural-Language Agent Harnesses](wiki/papers/natural-language-agent-harnesses-afdf2016.md) | arXiv 2026 |

#### Execution Feedback as Grounded Verification

| Paper | Venue |
| --- | --- |
| [Agentless: Demystifying LLM-based Software Engineering Agents](wiki/papers/agentless-demystifying-llm-based-software-engineering-agents-c52036c5.md) | arXiv 2024 |
| [RepairAgent: An Autonomous, LLM-Based Agent for Program Repair](wiki/papers/repairagent-an-autonomous-llm-based-agent-for-program-repair-209c4f7c.md) | ICSE 2025 |
| [Live-SWE-agent: Can Software Engineering Agents Self-Evolve on the Fly?](wiki/papers/live-swe-agent-can-software-engineering-agents-self-evolve-on-the-fly-22ad6116.md) | arXiv 2025 |
| [Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering](wiki/papers/code-generation-with-alphacodium-from-prompt-engineering-to-flow-enginee-15b7c04f.md) | arXiv 2024 |

#### Memory and Context Management at Repository Scale

| Paper | Venue |
| --- | --- |
| [RepoAgent: An LLM-Powered Open-Source Framework for Repository-level Code Documentation Generation](wiki/papers/repoagent-an-llm-powered-open-source-framework-for-repository-level-code-3398bf12.md) | EMNLP 2024 (Demo) |
| [ContextBench: A Benchmark for Context Retrieval in Coding Agents](wiki/papers/contextbench-a-benchmark-for-context-retrieval-in-coding-agents-0f2f361a.md) | arXiv 2026 |
| [CodeMem: Architecting Reproducible Agents via Dynamic MCP and Procedural Memory](wiki/papers/codemem-architecting-reproducible-agents-via-dynamic-mcp-and-procedural-51c5353a.md) | arXiv 2025 |
| [MemGovern: Enhancing Code Agents through Learning from Governed Human Experiences](wiki/papers/memgovern-enhancing-code-agents-through-learning-from-governed-human-exp-acb2227b.md) | arXiv 2026 |

#### Developer Intent and Project Conventions as Latent State

| Paper | Venue |
| --- | --- |
| [Learning to Commit: Generating Organic Pull Requests via Online Repository Memory](wiki/papers/learning-to-commit-generating-organic-pull-requests-via-online-repositor-bf97688d.md) | arXiv 2026 |
| [CodeTaste: Can LLMs Generate Human-Level Code Refactorings?](wiki/papers/codetaste-can-llms-generate-human-level-code-refactorings-5858f760.md) | arXiv 2026 |
| [SWE-bench+: Enhanced Coding Benchmark for LLMs](wiki/papers/swe-bench-enhanced-coding-benchmark-for-llms-f411037c.md) | ICSE Companion 2025 |

#### From Inline Completion to Autonomous SWE Agents

| Paper | Venue |
| --- | --- |
| [Evaluating Large Language Models Trained on Code](wiki/papers/evaluating-large-language-models-trained-on-code-eaa16e87.md) | arXiv 2021 |
| [The Impact of AI on Developer Productivity: Evidence from GitHub Copilot](wiki/papers/the-impact-of-ai-on-developer-productivity-evidence-from-github-copilot-752fb49d.md) | arXiv 2023 |
| [Expectation vs.\ Experience: Evaluating the Usability of Code Generation Tools Powered by Large Language Models](wiki/papers/expectation-vs-experience-evaluating-the-usability-of-code-generation-to-ba30097e.md) | CHI Extended Abstracts 2022 |
| [Reading Between the Lines: Modeling User Behavior and Costs in AI-Assisted Programming](wiki/papers/reading-between-the-lines-modeling-user-behavior-and-costs-in-ai-assiste-1f4d9998.md) | CHI 2024 |

#### From Patch Generation to Software Lifecycle Participation

| Paper | Venue |
| --- | --- |
| [SWE-bench: Can Language Models Resolve Real-world Github Issues?](wiki/papers/swe-bench-can-language-models-resolve-real-world-github-issues-3deec234.md) | ICLR 2024 |
| [SWE-lancer: Can frontier LLMs earn \$1 million from real-world freelance software engineering?](wiki/papers/swe-lancer-can-frontier-llms-earn-1-million-from-real-world-freelance-so-46a09e5b.md) | ICML 2025 |
| [SWE-bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?](wiki/papers/swe-bench-pro-can-ai-agents-solve-long-horizon-software-engineering-task-a35cd518.md) | arXiv 2025 |
| [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](wiki/papers/terminal-bench-benchmarking-agents-on-hard-realistic-tasks-in-command-li-f510afcd.md) | arXiv 2026 |
| [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](wiki/papers/appworld-a-controllable-world-of-apps-and-people-for-benchmarking-intera-112f7b43.md) | ACL 2024 |
| [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](wiki/papers/bench-a-benchmark-for-tool-agent-user-interaction-in-real-world-domains-9a9389db.md) | ICLR 2025 |
| [AI Augmented CI/CD Pipelines: From Code Commit to Production with Autonomous Decisions](wiki/papers/ai-augmented-ci-cd-pipelines-from-code-commit-to-production-with-autonom-2fd5abcb.md) | IEEE FLLM 2025 |
| [Advances and Frontiers of LLM-based Issue Resolution in Software Engineering: A Comprehensive Survey](wiki/papers/advances-and-frontiers-of-llm-based-issue-resolution-in-software-enginee-c74217fb.md) | arXiv 2026 |
| [Alibaba LingmaAgent: Improving Automated Issue Resolution via Comprehensive Repository Exploration](wiki/papers/alibaba-lingmaagent-improving-automated-issue-resolution-via-comprehensi-5d60564d.md) | FSE 2025 |
| [CodeAgent: Autonomous Communicative Agents for Code Review](wiki/papers/codeagent-autonomous-communicative-agents-for-code-review-29cac8ec.md) | EMNLP 2024 |

#### Multi-Agent Code Assistance and Shared Repositories

| Paper | Venue |
| --- | --- |
| [ChatDev: Communicative Agents for Software Development](wiki/papers/chatdev-communicative-agents-for-software-development-204be492.md) | ACL 2024 |
| [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](wiki/papers/metagpt-meta-programming-for-a-multi-agent-collaborative-framework-39846716.md) | ICLR 2024 |
| [CodeAgent: Enhancing Code Generation with Tool-Integrated Agent Systems for Real-World Repo-Level Coding Challenges](wiki/papers/codeagent-enhancing-code-generation-with-tool-integrated-agent-systems-f-00f877e6.md) | ACL 2024 |
| [METAL: A Multi-Agent Framework for Chart Generation with Test-Time Scaling](wiki/papers/metal-a-multi-agent-framework-for-chart-generation-with-test-time-scalin-ce33946c.md) | ACL 2025 |

#### The Harness as a Distillation Surface

| Paper | Venue |
| --- | --- |
| [Composer: Building a fast frontier model with reinforcement learning](wiki/papers/composer-building-a-fast-frontier-model-with-reinforcement-learning-9d8c0590.md) \[Blog\] | 2025 |
| [Improving Composer through real-time reinforcement learning](wiki/papers/improving-composer-through-real-time-reinforcement-learning-6da0c2bb.md) \[Blog\] | 2025 |
| [Addendum to GPT-5 system card: GPT-5-Codex](wiki/papers/addendum-to-gpt-5-system-card-gpt-5-codex-7e882bd7.md) \[Report\] | 2025 |
| [Building more with GPT-5.1-Codex-Max](wiki/papers/building-more-with-gpt-5-1-codex-max-4ff7e209.md) \[Blog\] | 2025 |
| [How Anthropic teams use Claude Code](wiki/papers/how-anthropic-teams-use-claude-code-e7cd9f45.md) \[Report\] | 2025 |

#### Open Challenges for Code-Assistant Harnesses

| Paper | Venue |
| --- | --- |
| [Are "Solved Issues" in SWE-bench Really Solved Correctly? An Empirical Study](wiki/papers/are-solved-issues-in-swe-bench-really-solved-correctly-an-empirical-stud-1b439190.md) | arXiv 2025 |
| [SWE-Bench++: A Framework for the Scalable Generation of Software Engineering Benchmarks](wiki/papers/swe-bench-a-framework-for-the-scalable-generation-of-software-engineerin-d96de304.md) | arXiv 2025 |
| [Introducing Aardvark: OpenAI's Agentic Security Researcher](wiki/papers/introducing-aardvark-openai-s-agentic-security-researcher-4f6b5d20.md) \[Blog\] | 2025 |
| [Codex Security: Now in Research Preview](wiki/papers/codex-security-now-in-research-preview-45e5887e.md) \[Blog\] | 2026 |
| [Why Do Multi-Agent LLM Systems Fail?](wiki/papers/why-do-multi-agent-llm-systems-fail-84a2c129.md) | arXiv 2025 |
| [Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems](wiki/papers/which-agent-causes-task-failures-and-when-on-automated-failure-attributi-48b6ec4f.md) | arXiv 2025 |
| [AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?](wiki/papers/agentracer-who-is-inducing-failure-in-the-llm-agentic-systems-e747c976.md) | arXiv 2025 |
| [Where LLM Agents Fail and How They Can Learn from Failures](wiki/papers/where-llm-agents-fail-and-how-they-can-learn-from-failures-d05296df.md) | arXiv 2025 |
| [Beyond Static Sandboxing: Learned Capability Governance for Autonomous AI Agents](wiki/papers/beyond-static-sandboxing-learned-capability-governance-for-autonomous-ai-a8b8b443.md) | arXiv 2026 |
| [Fault-Tolerant Sandboxing for AI Coding Agents: A Transactional Approach to Safe Autonomous Execution](wiki/papers/fault-tolerant-sandboxing-for-ai-coding-agents-a-transactional-approach-260e82ac.md) | arXiv 2025 |
| [Introducing the Agent Governance Toolkit: Open-Source Runtime Security for AI Agents](wiki/papers/introducing-the-agent-governance-toolkit-open-source-runtime-security-fo-24b2c1ff.md) \[Blog\] | 2026 |

### 🖥️ GUI / OS Agents

GUI/OS environments are program worlds in the most literal sense: every observation is rendered code, and every action is a call into another piece of code.

#### GUI/OS as a Partially Observable Program World

| Paper | Venue |
| --- | --- |
| [WebArena: A Realistic Web Environment for Building Autonomous Agents](wiki/papers/webarena-a-realistic-web-environment-for-building-autonomous-agents-4b11676f.md) | ICLR 2024 |
| [Mind2Web: Towards a Generalist Agent for the Web](wiki/papers/mind2web-towards-a-generalist-agent-for-the-web-ceffc74e.md) | NeurIPS 2023 |
| [AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents](wiki/papers/androidworld-a-dynamic-benchmarking-environment-for-autonomous-agents-30cc7f92.md) | ICLR 2025 |
| [Windows Agent Arena: Evaluating Multi-Modal OS Agents at Scale](wiki/papers/windows-agent-arena-evaluating-multi-modal-os-agents-at-scale-e546e545.md) | ICML 2025 |
| [AgentOccam: A Simple Yet Strong Baseline for LLM-Based Web Agents](wiki/papers/agentoccam-a-simple-yet-strong-baseline-for-llm-based-web-agents-488c7db3.md) | ICLR 2025 |
| [GPT-4V(ision) is a Generalist Web Agent, if Grounded](wiki/papers/gpt-4v-ision-is-a-generalist-web-agent-if-grounded-9798695d.md) | ICML 2024 |
| [WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models](wiki/papers/webvoyager-building-an-end-to-end-web-agent-with-large-multimodal-models-3808815b.md) | ACL 2024 |
| [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](wiki/papers/osworld-benchmarking-multimodal-agents-for-open-ended-tasks-in-real-comp-2a4a6e0a.md) | NeurIPS 2024 |
| [Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V](wiki/papers/set-of-mark-prompting-unleashes-extraordinary-visual-grounding-in-gpt-4v-b0ceb324.md) | arXiv 2023 |
| [WorkArena: How Capable are Web Agents at Solving Common Knowledge Work Tasks?](wiki/papers/workarena-how-capable-are-web-agents-at-solving-common-knowledge-work-ta-a32eabd8.md) | ICML 2024 |
| [CogAgent: A Visual Language Model for GUI Agents](wiki/papers/cogagent-a-visual-language-model-for-gui-agents-83d717d9.md) | CVPR 2024 |
#### Unifying Perception, Action, and Evaluation Through Code

| Paper | Venue |
| --- | --- |
| [Executable Code Actions Elicit Better LLM Agents](wiki/papers/executable-code-actions-elicit-better-llm-agents-31b16f13.md) | ICML 2024 |
| [Cradle: Empowering Foundation Agents towards General Computer Control](wiki/papers/cradle-empowering-foundation-agents-towards-general-computer-control-4da17469.md) | ICML 2025 |
| [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](wiki/papers/theagentcompany-benchmarking-llm-agents-on-consequential-real-world-task-7a7d553e.md) | NeurIPS 2025 |
| [SeeClick: Harnessing GUI Grounding for Advanced Visual GUI Agents](wiki/papers/seeclick-harnessing-gui-grounding-for-advanced-visual-gui-agents-374f0e85.md) | ACL 2024 |
| [Ferret-UI: Grounded Mobile UI Understanding with Multimodal LLMs](wiki/papers/ferret-ui-grounded-mobile-ui-understanding-with-multimodal-llms-6b11bec1.md) | ECCV 2024 |
| [OS-ATLAS: Foundation Action Model for Generalist GUI Agents](wiki/papers/os-atlas-foundation-action-model-for-generalist-gui-agents-ad69f88c.md) | ICLR 2025 |
| [ShowUI: One Vision-Language-Action Model for GUI Visual Agent](wiki/papers/showui-one-vision-language-action-model-for-gui-visual-agent-ba4fe9f6.md) | CVPR 2025 |
| [Aria-UI: Visual Grounding for GUI Instructions](wiki/papers/aria-ui-visual-grounding-for-gui-instructions-b6366c01.md) | ACL 2025 Findings |
| [Navigating the Digital World as Humans Do: Universal Visual Grounding for GUI Agents](wiki/papers/navigating-the-digital-world-as-humans-do-universal-visual-grounding-for-2b299bb2.md) | ICLR 2025 |
| [UI-TARS: Pioneering Automated GUI Interaction with Native Agents](wiki/papers/ui-tars-pioneering-automated-gui-interaction-with-native-agents-a4b3da87.md) | arXiv 2025 |
| [GUI-Libra: Training Native GUI Agents to Reason and Act with Action-aware Supervision and Partially Verifiable RL](wiki/papers/gui-libra-training-native-gui-agents-to-reason-and-act-with-action-aware-03f1c459.md) | arXiv 2026 |
| [Spider2-V: How Far Are Multimodal Agents From Automating Data Science and Engineering Workflows?](wiki/papers/spider2-v-how-far-are-multimodal-agents-from-automating-data-science-and-d1abb370.md) | NeurIPS 2024 |
#### Memory as Persistent Program State

| Paper | Venue |
| --- | --- |
| [Synapse: Trajectory-as-Exemplar Prompting with Memory for Computer Control](wiki/papers/synapse-trajectory-as-exemplar-prompting-with-memory-for-computer-contro-080f386e.md) | ICLR 2024 |
| [AppAgent: Multimodal Agents as Smartphone Users](wiki/papers/appagent-multimodal-agents-as-smartphone-users-9abb5e3a.md) | CHI 2025 |
| [Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration](wiki/papers/mobile-agent-v2-mobile-device-operation-assistant-with-effective-navigat-a7095268.md) | NeurIPS 2024 |
| [UI-Voyager: A Self-Evolving GUI Agent Learning via Failed Experience](wiki/papers/ui-voyager-a-self-evolving-gui-agent-learning-via-failed-experience-21027868.md) | arXiv 2026 |
| [AutoGLM: Autonomous Foundation Agents for GUIs](wiki/papers/autoglm-autonomous-foundation-agents-for-guis-37e341b3.md) | arXiv 2024 |
| [OS-Genesis: Automating GUI Agent Trajectory Construction via Reverse Task Synthesis](wiki/papers/os-genesis-automating-gui-agent-trajectory-construction-via-reverse-task-d97f8b26.md) | ACL 2025 |
| [PlugMem: A Task-Agnostic Plugin Memory Module for LLM Agents](wiki/papers/plugmem-a-task-agnostic-plugin-memory-module-for-llm-agents-7f709de6.md) | arXiv 2026 |
#### UI Simulators and Sandboxes as Executable Dynamics

| Paper | Venue |
| --- | --- |
| [Reinforcement Learning on Web Interfaces Using Workflow-Guided Exploration](wiki/papers/reinforcement-learning-on-web-interfaces-using-workflow-guided-explorati-ca6ed993.md) | ICLR 2018 |
| [WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents](wiki/papers/webshop-towards-scalable-real-world-web-interaction-with-grounded-langua-43799165.md) | NeurIPS 2022 |
| [VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks](wiki/papers/visualwebarena-evaluating-multimodal-agents-on-realistic-visual-web-task-e2950952.md) | ACL 2024 |
| [Understanding the Weakness of Large Language Model Agents within a Complex Android Environment](wiki/papers/understanding-the-weakness-of-large-language-model-agents-within-a-compl-7ccf8ddb.md) | KDD 2024 |
| [AndroidLab: Training and Systematic Benchmarking of Android Autonomous Agents](wiki/papers/androidlab-training-and-systematic-benchmarking-of-android-autonomous-ag-18425c00.md) | ACL 2025 |
| [AgentBench: Evaluating LLMs as Agents](wiki/papers/agentbench-evaluating-llms-as-agents-8d39628a.md) | ICLR 2024 |
| [Code2World: A GUI World Model via Renderable Code Generation](wiki/papers/code2world-a-gui-world-model-via-renderable-code-generation-7301fde3.md) | arXiv 2026 |

#### From Simulation to Production: Executable Feedback Loops

| Paper | Venue |
| --- | --- |
| [3.5 Models and Computer Use](wiki/papers/3-5-models-and-computer-use-b7106ed3.md) \[Blog\] | 2024 |
| [Introducing Operator](wiki/papers/introducing-operator-55380981.md) \[Blog\] | 2025 |
| [Project Mariner](wiki/papers/project-mariner-c0065213.md) \[Blog\] | 2025 |
| [AutoWebGLM: A Large Language Model-based Web Navigating Agent](wiki/papers/autowebglm-a-large-language-model-based-web-navigating-agent-a0c48b83.md) | KDD 2024 |

### 🤖 Autonomous Embodied Agents

Code grounds embodied actions in physical feasibility, accumulates reusable skills as memory, and supports auditable real-world deployment.

#### Agent Harness for Grounded and Verifiable Embodied Actions

| Paper | Venue |
| --- | --- |
| [Code as Policies: Language Model Programs for Embodied Control](wiki/papers/code-as-policies-language-model-programs-for-embodied-control-b943849c.md) | ICRA 2023 |
| [ChatGPT for Robotics: Design Principles and Model Abilities](wiki/papers/chatgpt-for-robotics-design-principles-and-model-abilities-8a189373.md) | IEEE Access 2024 |
| [Inner Monologue: Embodied Reasoning through Planning with Language Models](wiki/papers/inner-monologue-embodied-reasoning-through-planning-with-language-models-16fafae3.md) | CoRL 2022 |
| [VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](wiki/papers/voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-35b6001a.md) | CoRL 2023 |
| [The Marathon 2: A Navigation System](wiki/papers/the-marathon-2-a-navigation-system-b7868da6.md) | IROS 2020 |
| [PaLM-E: An Embodied Multimodal Language Model](wiki/papers/palm-e-an-embodied-multimodal-language-model-691c0be0.md) | ICML 2023 |
| [Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning](wiki/papers/gemini-robotics-1-5-pushing-the-frontier-of-generalist-robots-with-advan-3de8b222.md) | arXiv 2025 |
| [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](wiki/papers/do-as-i-can-not-as-i-say-grounding-language-in-robotic-affordances-a610b79a.md) | CoRL 2022 |
| [Robots That Ask for Help: Uncertainty Alignment for Large Language Model Planners](wiki/papers/robots-that-ask-for-help-uncertainty-alignment-for-large-language-model-c20455bc.md) | CoRL 2023 |
| [SkillVLA: Tackling Combinatorial Diversity in Dual-Arm Manipulation via Skill Reuse](wiki/papers/skillvla-tackling-combinatorial-diversity-in-dual-arm-manipulation-via-s-22c17d5e.md) | arXiv 2026 |
| [Bootstrap Your Own Skills: Learning to Solve New Tasks with Large Language Model Guidance](wiki/papers/bootstrap-your-own-skills-learning-to-solve-new-tasks-with-large-languag-6e0dd321.md) | CoRL 2023 |
| [RoboCodeX: Multimodal Code Generation for Robotic Behavior Synthesis](wiki/papers/robocodex-multimodal-code-generation-for-robotic-behavior-synthesis-7e8876fb.md) | ICML 2024 |
| [Robotic Programmer: Video Instructed Policy Code Generation for Robotic Manipulation](wiki/papers/robotic-programmer-video-instructed-policy-code-generation-for-robotic-m-084591c8.md) | IROS 2025 |
| [Code-BT: A Code-Driven Approach to Behavior Tree Generation for Robot Tasks Planning with Large Language Models](wiki/papers/code-bt-a-code-driven-approach-to-behavior-tree-generation-for-robot-tas-e57c984e.md) | IJCAI 2025 |
| [LLM-Driven Corrective Robot Operation Code Generation with Static Text-Based Simulation](wiki/papers/llm-driven-corrective-robot-operation-code-generation-with-static-text-b-582b9325.md) | ICRA 2026 |
| [NormCode: A Semi-Formal Language for Auditable AI Planning](wiki/papers/normcode-a-semi-formal-language-for-auditable-ai-planning-96b226f7.md) | arXiv 2025 |
| [CP-Agent: Agentic Constraint Programming](wiki/papers/cp-agent-agentic-constraint-programming-f117f2ca.md) | arXiv 2025 |
| [VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation](wiki/papers/veriguard-enhancing-llm-agent-safety-via-verified-code-generation-a5861f4a.md) | arXiv 2025 |

#### Reusable Skills as Embodied Memory

| Paper | Venue |
| --- | --- |
| [Voyager: An Open-Ended Embodied Agent with Large Language Models](wiki/papers/voyager-an-open-ended-embodied-agent-with-large-language-models-b3b8e559.md) | NeurIPS 2023 |
| [Lifelong Robot Library Learning: Bootstrapping Composable and Generalizable Skills for Embodied Control with Language Models](wiki/papers/lifelong-robot-library-learning-bootstrapping-composable-and-generalizab-a115e6fb.md) | ICRA 2024 |
| [Growing with Your Embodied Agent: A Human-in-the-Loop Lifelong Code Generation Framework for Long-Horizon Manipulation Skills](wiki/papers/growing-with-your-embodied-agent-a-human-in-the-loop-lifelong-code-gener-7092156e.md) | arXiv 2025 |
| [ViReSkill: Vision-Grounded Replanning with Skill Memory for LLM-Based Planning in Lifelong Robot Learning](wiki/papers/vireskill-vision-grounded-replanning-with-skill-memory-for-llm-based-pla-5e0ae7fb.md) | arXiv 2025 |
| [Lifelong Language-Conditioned Robotic Manipulation Learning](wiki/papers/lifelong-language-conditioned-robotic-manipulation-learning-a0e49c32.md) | AAAI 2026 |
| [UI-Voyager: A Self-Evolving GUI Agent Learning via Failed Experience](wiki/papers/ui-voyager-a-self-evolving-gui-agent-learning-via-failed-experience-21027868.md) | arXiv 2026 |

#### Coordinated and Auditable Real-World Deployment

| Paper | Venue |
| --- | --- |
| [GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models](wiki/papers/genswarm-scalable-multi-robot-code-policy-generation-and-deployment-via-b4a3a391.md) | npj Robotics 2026 |
| [Agents4PLC: Automating Closed-Loop PLC Code Generation and Verification in Industrial Control Systems](wiki/papers/agents4plc-automating-closed-loop-plc-code-generation-and-verification-i-b728768f.md) | IEEE TSE 2026 |
| [RACAS: Controlling Diverse Robots With a Single Agentic System](wiki/papers/racas-controlling-diverse-robots-with-a-single-agentic-system-cdaaa413.md) | arXiv 2026 |
| [ALRM: Agentic LLM for Robotic Manipulation](wiki/papers/alrm-agentic-llm-for-robotic-manipulation-10f7a82b.md) | arXiv 2026 |

### 🔬 Scientific Discovery Agents

Hypotheses are encoded as differential equations or generative models; protocols as XDL or Opentrons scripts; analyses as Jupyter notebooks. Code carries scientific reasoning, scientific action, and the scientific environment itself.

#### Scientific Discovery as a Partially Observable Program World

| Paper | Venue |
| --- | --- |
| [The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search](wiki/papers/the-ai-scientist-v2-workshop-level-automated-scientific-discovery-via-ag-534bcc04.md) | arXiv 2025 |
| [ChemCrow: Augmenting large-language models with chemistry tools](wiki/papers/chemcrow-augmenting-large-language-models-with-chemistry-tools-df0e3895.md) | Nature MI 2024 |
| [Autonomous chemical research with large language models](wiki/papers/autonomous-chemical-research-with-large-language-models-8eae7fc9.md) | Nature 2023 |
| [Biomni: A General-Purpose Biomedical AI Agent](wiki/papers/biomni-a-general-purpose-biomedical-ai-agent-d7e73904.md) | bioRxiv 2025 |
| [Olympiad-Level Formal Mathematical Reasoning with Reinforcement Learning](wiki/papers/olympiad-level-formal-mathematical-reasoning-with-reinforcement-learning-60b4ebde.md) | Nature 2025 |
| [The virtual lab of AI agents designs new SARS-CoV-2 nanobodies](wiki/papers/the-virtual-lab-of-ai-agents-designs-new-sars-cov-2-nanobodies-f9eaab2f.md) | Nature 2025 |

#### Unifying Ideation, Experimentation, Analysis, and Communication

| Paper | Venue |
| --- | --- |
| [ResearchAgent: Iterative Research Idea Generation over Scientific Literature with Large Language Models](wiki/papers/researchagent-iterative-research-idea-generation-over-scientific-literat-2fb7c155.md) | NAACL 2025 |
| [BioPlanner: Automatic Evaluation of LLMs on Protocol Planning in Biology](wiki/papers/bioplanner-automatic-evaluation-of-llms-on-protocol-planning-in-biology-2595f41f.md) | EMNLP 2023 |
| [Agent Laboratory: Using LLM Agents as Research Assistants](wiki/papers/agent-laboratory-using-llm-agents-as-research-assistants-193c060a.md) | EMNLP 2025 Findings |
| [AgentRxiv: Towards Collaborative Autonomous Research](wiki/papers/agentrxiv-towards-collaborative-autonomous-research-d6573873.md) | arXiv 2025 |
| [The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery](wiki/papers/the-ai-scientist-towards-fully-automated-open-ended-scientific-discovery-703b516e.md) | arXiv 2024 |
| [Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents](wiki/papers/towards-scientific-intelligence-a-survey-of-llm-based-scientific-agents-aa066cd2.md) | arXiv 2026 |
| [Executable Code Actions Elicit Better LLM Agents](wiki/papers/executable-code-actions-elicit-better-llm-agents-31b16f13.md) | ICML 2024 |
| [A universal system for digitization and automatic execution of the chemical synthesis literature](wiki/papers/a-universal-system-for-digitization-and-automatic-execution-of-the-chemi-a1789abc.md) | Science 2020 |

#### Memory as Persistent Program State

| Paper | Venue |
| --- | --- |
| [AIDE: AI-Driven Exploration in the Space of Code](wiki/papers/aide-ai-driven-exploration-in-the-space-of-code-c428072e.md) | arXiv 2025 |
| [El Agente: An autonomous agent for quantum chemistry](wiki/papers/el-agente-an-autonomous-agent-for-quantum-chemistry-115ed543.md) | Matter 2025 |
| [PaperQA: Retrieval-Augmented Generative Agent for Scientific Research](wiki/papers/paperqa-retrieval-augmented-generative-agent-for-scientific-research-5a8dae6f.md) | arXiv 2023 |
| [Towards an AI co-scientist](wiki/papers/towards-an-ai-co-scientist-efbe9824.md) | arXiv 2025 |

#### Simulators as Executable Dynamics

| Paper | Venue |
| --- | --- |
| [AlphaEvolve: A coding agent for scientific and algorithmic discovery](wiki/papers/alphaevolve-a-coding-agent-for-scientific-and-algorithmic-discovery-9d1c64f5.md) | arXiv 2025 |

#### Self-Driving Labs as Executable Feedback Loops

| Paper | Venue |
| --- | --- |
| [Self-driving laboratory for accelerated discovery of thin-film materials](wiki/papers/self-driving-laboratory-for-accelerated-discovery-of-thin-film-materials-a0aa7707.md) | arXiv 2020 |
| [MatPilot: an LLM-enabled AI Materials Scientist under the Framework of Human-Machine Collaboration](wiki/papers/matpilot-an-llm-enabled-ai-materials-scientist-under-the-framework-of-hu-140d5eb3.md) | arXiv 2024 |
| [An autonomous laboratory for the accelerated synthesis of inorganic materials](wiki/papers/an-autonomous-laboratory-for-the-accelerated-synthesis-of-inorganic-mate-6197b701.md) | Nature 2023 |

#### Toward Agentic and Instruction-Following Science

| Paper | Venue |
| --- | --- |
| [MLAgentBench: Evaluating Language Agents on Machine Learning Experimentation](wiki/papers/mlagentbench-evaluating-language-agents-on-machine-learning-experimentat-26cca14a.md) | arXiv 2024 |
| [MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering](wiki/papers/mle-bench-evaluating-machine-learning-agents-on-machine-learning-enginee-94e42fb8.md) | arXiv 2025 |
| [A Survey of Scientific Large Language Models: From Data Foundations to Agent Frontiers](wiki/papers/a-survey-of-scientific-large-language-models-from-data-foundations-to-ag-4493b81b.md) | arXiv 2025 |
| [ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery](wiki/papers/scienceagentbench-toward-rigorous-assessment-of-language-agents-for-data-80d4c78e.md) | ICLR 2025 |
| [DiscoveryBench: Towards Data-Driven Discovery with Large Language Models](wiki/papers/discoverybench-towards-data-driven-discovery-with-large-language-models-f1a32ee6.md) | arXiv 2024 |

### 🧠 Agent Personalization

As recommendation moves from static prediction toward interactive agents, personalization systems must reason over latent and evolving user preferences through structured, editable preference states and executable feedback pipelines.

#### From Static Recommendation to Interactive Personalization

| Paper | Venue |
| --- | --- |
| [LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation](wiki/papers/lightgcn-simplifying-and-powering-graph-convolution-network-for-recommen-67e7ee43.md) | SIGIR 2020 |
| [DeepFM: A Factorization-Machine Based Neural Network for CTR Prediction](wiki/papers/deepfm-a-factorization-machine-based-neural-network-for-ctr-prediction-f84a369d.md) | IJCAI 2017 |
| [Large Language Models are Zero-Shot Rankers for Recommender Systems](wiki/papers/large-language-models-are-zero-shot-rankers-for-recommender-systems-6cc898f1.md) | ECIR 2024 |
| [Uncovering ChatGPT's Capabilities in Recommender Systems](wiki/papers/uncovering-chatgpt-s-capabilities-in-recommender-systems-2d2591c3.md) | RecSys 2023 |
| [RecoWorld: Building Simulated Environments for Agentic Recommender Systems](wiki/papers/recoworld-building-simulated-environments-for-agentic-recommender-system-bef0dd94.md) | arXiv 2025 |
| [RecMind: Large Language Model Powered Agent for Recommendation](wiki/papers/recmind-large-language-model-powered-agent-for-recommendation-e0579e21.md) | NAACL 2024 Findings |
| [Recommender AI Agent: Integrating Large Language Models for Interactive Recommendations](wiki/papers/recommender-ai-agent-integrating-large-language-models-for-interactive-r-73cf0644.md) | ACM TOIS 2025 |
| [On Generative Agents in Recommendation](wiki/papers/on-generative-agents-in-recommendation-38830c5b.md) | SIGIR 2024 |
| [iAgent: LLM Agent as a Shield Between User and Recommender Systems](wiki/papers/iagent-llm-agent-as-a-shield-between-user-and-recommender-systems-8d04b6af.md) | ACL 2025 Findings |

#### Preference State as an Editable Artifact

| Paper | Venue |
| --- | --- |
| [A-Mem: Agentic Memory for LLM Agents](wiki/papers/a-mem-agentic-memory-for-llm-agents-95975c4d.md) | NeurIPS 2026 |
| [Evo-Memory: Benchmarking LLM Agent Test-Time Learning with Self-Evolving Memory](wiki/papers/evo-memory-benchmarking-llm-agent-test-time-learning-with-self-evolving-63ad13df.md) | arXiv 2025 |
| [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](wiki/papers/mem0-building-production-ready-ai-agents-with-scalable-long-term-memory-4bb9a734.md) | arXiv 2025 |
| [MemRec: Collaborative Memory-Augmented Agentic Recommender System](wiki/papers/memrec-collaborative-memory-augmented-agentic-recommender-system-ddd5c1ab.md) | arXiv 2026 |

#### Feedback as Policy Adaptation

| Paper | Venue |
| --- | --- |
| [LLM-Powered User Simulator for Recommender System](wiki/papers/llm-powered-user-simulator-for-recommender-system-e1c7b08c.md) | AAAI 2025 |
| [User Behavior Simulation with Large Language Model-Based Agents](wiki/papers/user-behavior-simulation-with-large-language-model-based-agents-2c7c0dc4.md) | ACM TOIS 2025 |

#### Controllable and Instruction-Following Personalization

| Paper | Venue |
| --- | --- |
| [Conversational Recommendation: Formulation, Methods, and Evaluation](wiki/papers/conversational-recommendation-formulation-methods-and-evaluation-5a9037f4.md) | SIGIR 2020 |

---

## ✨ Acknowledgements

We thank the broader community for the contributions surveyed here. If your paper should be added or moved, please open a pull request or issue.

## 📄 License

This repository is released under the [MIT License](LICENSE).
