# Pick a starting path

These are suggested sequences, not a certification curriculum. Paid courses are optional.

## Coding-agent / tool-using track

The recommended starting track for students securing agents with access to tools, credentials, MCP servers, files and network services. Use labs and testing tools **only in environments where you have authorization**. Use synthetic data in disposable environments; never test against third-party systems without permission.

1. **Map authority.** Read [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices), then [OWASP ASI](https://genai.owasp.org/initiatives/agentic-security-initiative/). Draw the path from user authorization to identity, tool invocation and data access. Identify where an untrusted response could become an instruction.
2. **Practice and retest.** Work through [FinBot CTF](https://github.com/OWASP-ASI/finbot-ctf-demo), then [AgentDojo](https://github.com/ethz-spylab/agentdojo). For each case submit four observations: failure, crossed trust boundary, mitigation and retest result. Model/API and infrastructure costs may apply. Use our [Watcher infographic and worksheet](CODING_AGENT_THREAT_MODEL.md) to distinguish recording, grading and prevention.
3. **Challenge trace custody.** Read [LLM Agents Can Easily Tamper With Their Own Traces](https://arxiv.org/abs/2609.30266). The study demonstrates trace modification in tested local agent setups and motivates interception outside agent control. **Required tabletop exercise:** draw who and what remains reachable after injection, and after “deleting” the agent. Include retained credentials, delegated processes, remote sessions and logging services. Is a session log an authority record if the agent can edit it? Specify independently controlled, append-only capture and what stops execution if required evidence cannot be recorded. These are design requirements to evaluate, not properties we claim Watcher provides. Do not delete real logs or disable monitoring.
4. **Separate capability from permission.** Read [ScopeBench](https://arxiv.org/abs/2609.30325). Its tasks distinguish achieving a goal from obeying scope when that goal requires crossing a boundary. Our engineering takeaway: write rules of engagement (RoE), then enforce them through pre-execution controls. Document wording alone is not a stop. Explain what should happen when the objective is impossible within scope: stop and request authorization, rather than expand access.
5. **Compare a runtime gate.** Read [AGATE](https://arxiv.org/abs/2609.30830), which studies deterministic authorization and provenance checks at instrumented harness boundaries. Identify what is observed, what can be vetoed and where transformations or incomplete coverage weaken the design. Compare that boundary with Watcher’s documented review route; neither paper nor diagram establishes universal protection.
6. **Submit a one-page engagement perimeter.** Use the template below. Pair it with one allowed action, one denied action and one approval-required action, using mock inputs. Record the expected gate and the evidence you would need to verify each result.

### One-page engagement perimeter

| Decision | Your explicit boundary |
| --- | --- |
| Owner and legitimate objective | Who authorizes the work; what constitutes completion? |
| Allowed tools and identities | Exact tools, credentials and delegated identities; minimum privileges. |
| Data and filesystem | Allowed paths and data classes; forbidden reads/writes; synthetic fixtures. |
| Network | Permitted destinations and operations; deny everything else unless approved. |
| Approval thresholds | Which actions pause before execution; who may approve; expiry and exact scope. |
| Trace custody | Who captures, stores and can alter records; agent-independent evidence; behavior on logging failure. |
| Scope pressure | What stops an impossible or out-of-scope objective; how authorization is amended. |
| Shutdown and recovery | Revoke credentials, end remote sessions and delegated work, preserve evidence, restore state. |
| Retest evidence | Intended action, actual action, decision, outcome and independently retained evidence. |

Assessment is based on the boundary and evidence, not on obtaining a flag or collecting a credential. The papers describe particular experiments; their results are not guarantees for your environment.

## Understand the agent

Start with basic agent engineering such as LangChain Academy. Map the model, instructions, memory, tools, identity, and external data. Identify which actions require permission and where untrusted content enters.

## Secure the system

Read [OWASP's agentic guidance](https://genai.owasp.org/initiatives/agentic-security-initiative/) and [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices). Trace a tool call from user intent through authorization to result. Consider a structured security course after checking prerequisites and cost.

## Practice authorized red teaming

Explore [FinBot CTF](https://github.com/OWASP-ASI/finbot-ctf-demo), then [AgentDojo](https://github.com/ethz-spylab/agentdojo). Record each failure, affected trust boundary, mitigation, and retest result. Self-hosted labs may require model API credits or compute.

## Study safety

Read [Introduction to AI Safety, Ethics, and Society](https://www.aisafetybook.com/), then explore [Apollo Watcher](https://watcher.apolloresearch.ai/). Distinguish malicious misuse from unintended behavior. Ask what each evaluation measures and leaves untested.

## Govern deployment

Read the [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/) and follow [CSA AARM](https://cloudsecurityalliance.org/research/working-groups/autonomous-action-runtime-management-aarm). Draft a policy covering accountable owners, allowed actions, approval thresholds, monitoring, and incident response. These learning resources are not proof of compliance.

## Stay current

Follow blogs, videos, and podcasts in the library. Prefer technical explanations with evidence. Check certification claims and current availability with providers before paying.
