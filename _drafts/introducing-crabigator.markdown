---
layout: post
title: "Crabigator"
date: '2026-09-22T12:00:00-07:00'
class: crabigator-announcement
---

Crabigator lets me follow my coding agents and answer them from my phone.

<!-- Add your opening here. -->

{% include crabigator-video.html name="same-session" caption="I answer on my phone, and the same session carries on in my terminal." %}

<!--more-->

It wraps Claude Code, Codex, opencode, and Grok in the terminal I already use.

{% include crabigator-video.html name="four-agents" caption="Grok, opencode, Codex, and Claude Code each run inside Crabigator." %}

<!-- Add why you built it here. -->

{% include crabigator-video.html name="questions" caption="The dashboard turns an agent’s question into choices I can tap." %}

{% include crabigator-video.html name="dashboard-sync" caption="The desktop and mobile dashboards follow the same session." %}

{% include crabigator-video.html name="glyphs" caption="Each session has a small glyph and its own colors, so I can spot it quickly." %}

{% include crabigator-video.html name="pr-board" caption="The PR board brings pull requests and the sessions working on them into one view." %}

{% include crabigator-video.html name="changes" caption="The file and function views show what the agent changed." %}

<!-- Add the details and examples you want between these clips. -->

Crabigator is free and open source under the [MIT license](https://github.com/samuelclay/crabigator/blob/main/LICENSE).

Its [MCP interface](https://drinkcrabigator.com/mcp-tools) lets other tools work with the same sessions, and its [Herdr plugin](https://github.com/samuelclay/crabigator/tree/main/plugins/herdr) brings it into a Herdr pane.

<!-- Add your plans for extensions here. -->

```sh
npm install -g crabigator
crabigator
```

[Try Crabigator](https://drinkcrabigator.com) or [read the code](https://github.com/samuelclay/crabigator).
