---
name: social-research-profile-routing
description: "Use when deciding whether to route social web research."
version: 1.0.0
author: MASTER
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [routing, profiles, social-research, agent-reach, orchestration]
---

# Social Research Profile Routing

Route only the tasks that materially benefit from the dedicated `socialresearcher` profile. MASTER remains the integration and final-decision owner.

## When to Use

Route to `socialresearcher` when any of these is central to the task:

- a named platform or URL from Twitter/X, Reddit, Facebook, Instagram, LinkedIn, XiaoHongShu, Bilibili, V2EX, Xueqiu, Xiaoyuzhou, YouTube comments/transcripts, GitHub discussions/community signals, or RSS;
- "what people say", reviews, user complaints, community experience, sentiment, reactions, comments, threads, engagement, virality, creators/influencers, forum research, social listening, or regional Chinese web research;
- authenticated platform content;
- cross-platform human-signal collection;
- ordinary search/browser retrieval already failed on a supported platform.

## Do not route

Keep work in the normal `researcher` or current specialist when it is purely:

- general current facts or ordinary public web search;
- official documents, standards, filings, academic literature, PDF/OCR;
- coding documentation or repository implementation work;
- synthesis from sources already provided;
- a task where social/community evidence would not change the answer.

A platform name mentioned incidentally is not enough. Route only when platform-native human evidence is a load-bearing part of the requested outcome.

## Hybrid work

For decisions requiring both authoritative evidence and human signals:

1. Give `researcher` the official/document/academic workstream.
2. Give `socialresearcher` only the social/community/platform-native workstream.
3. Require `social-evidence/v1` or an equivalent structured packet.
4. MASTER verifies and integrates both; profiles do not recursively invoke each other.

## Invocation

1. Write a complete prompt to a task-local UTF-8 file. Include objective, platforms, geography/language, cutoff, read/write intent, required output, evidence fields, and acceptance criteria. Never put secrets in the prompt file.
2. Run:

```text
python C:/Users/admin/AppData/Local/hermes/skills/autonomous-ai-agents/social-research-profile-routing/scripts/run_socialresearcher.py --prompt-file <path> [--workdir <absolute-path>]
```

3. Treat the result as delegated and unverified until MASTER checks it.
4. If the profile reports login, QR, CAPTCHA, browser-extension, credential, account, or payment requirements, surface the exact human action needed rather than pretending the channel is available.
5. For external write actions, the current Administrator request must explicitly name the action and target; verify resulting state afterward.

## Hermes project safety

The runner never changes the active Hermes project. It passes `--in` only when an explicit absolute `--workdir` is supplied. Otherwise the profile starts in its dedicated configured workspace. Do not call `hermes project use`, create projects, or change another profile while routing.

## Verification

A routing acceptance test must prove:

- an explicit social-platform task routes to `socialresearcher`;
- an ordinary official-fact task stays with `researcher`/MASTER;
- a hybrid task is split by evidence class;
- the child identifies itself as SOCIALRESEARCHER;
- returned evidence is attributable and limitations are preserved;
- `hermes project list` is unchanged before and after invocation.
