# Crabigator announcement media

Edit the post in `_drafts/introducing-crabigator.markdown`. Each video has one sentence beneath it. The post stays unpublished while it is in `_drafts`.

## Clips

| File | Length | Shows |
| --- | --- | --- |
| same-session.mp4 | 18 s | A dashboard answer reaches the same Claude Code terminal session. |
| four-agents.mp4 | 26 s | Grok, opencode, Codex, and Claude Code running inside Crabigator. |
| questions.mp4 | 12 s | A close-up of answering a question on the mobile dashboard. |
| dashboard-sync.mp4 | 18 s | Desktop and mobile views of the same question and response. |
| glyphs.mp4 | 8 s | A close-up of the session glyph on the PR board. |
| pr-board.mp4 | 13 s | The board switches between pull requests and sessions. |
| changes.mp4 | 10 s | Terminal file and function changes beside the web diff view. |

Finished videos and JPEG posters live in `media/crabigator`. Videos are silent H.264 MP4 files. They autoplay muted, loop, and retain browser controls and inline mobile playback.

## What was recorded

All clips use real Crabigator sessions working in an isolated clone of Crabigator itself. Claude Code asked which README topic to explain and received “Phone controls” through the dashboard. The replacement color take asks it to suggest a paragraph without editing files. An earlier take edited the README and changed `cursor_to` in `src/terminal/escape.rs` to use named format arguments and ran the Rust tests. Grok, Codex, and opencode read the repository and explained it.

The mobile view is a real dashboard in a 390 × 770 emulated browser viewport. A temporary recording stylesheet keeps the controls at the bottom and lets the terminal shrink for a question and expand after the answer. This layout adjustment is only in the recording; it was not added to the product. The stylesheet is saved as `mobile-layout.css` in the source archive. It is not a recording of a physical phone. Desktop and mobile browser frames share wall-clock timestamps with the terminal recordings. The two side-by-side question clips use the same timestamp cuts for all views. Waiting time is removed between the opening, question, answer, and completed response. These cuts are listed in `question-timing.json`. The four-agent montage uses separate takes; it does not imply that all four answers arrived together.

Browser images are captured frames. Terminal images are drawn from recorded tmux ANSI buffers, with font fallback for glyphs and cell-sized rectangles for Unicode block elements. Claude was re-recorded with `NO_COLOR` removed from the child environment; its original ANSI colors are retained. Pairing-code fields are hidden. Zooms, cuts, labels, and panel layouts were added during editing. Terminal footage sits in a drawn macOS Ghostty-style window. Mobile footage sits in a drawn iPhone 17 frame with a Dynamic Island, status bar, and home indicator. The full 770-pixel browser viewport fits between the safe areas. These are decorative frames, not recordings of Ghostty or a physical iPhone. The bottom half of the changes clip is a still capture of the web diff. PRs #5 and #6 are real, already merged public Crabigator PRs; the recording did not create or merge them. The PR board was re-recorded with three separate sessions: Claude reviews grouping and test coverage in two sessions for PR #5, and Codex reviews session titles for PR #6. The clip cuts from two PR groups to three session groups. The glyph close-up uses this same take.

The draft links the existing MCP interface and Herdr plugin. Add your plans for other extensions in the marked space.

## Make a new cut

`source-recordings.tar.gz` holds the browser frames, terminal buffers, and timing files used by the renderer. It excludes abandoned setup attempts and removes pairing-code text. This folder is excluded from the public Jekyll build.

On macOS, with Python and ffmpeg installed:

```sh
python3 -m venv /tmp/crabigator-media-edit
/tmp/crabigator-media-edit/bin/pip install pillow pyte fonttools
mkdir -p /tmp/crabigator-media-source
tar -xzf tools/crabigator-media/source-recordings.tar.gz -C /tmp/crabigator-media-source
/tmp/crabigator-media-edit/bin/python tools/crabigator-media/render.py /tmp/crabigator-media-source/source media/crabigator
```

Use `--only questions glyphs` to render selected clips. When replacing videos, bump the `v` query value in `_includes/crabigator-video.html` so browsers load the new files. Adjust crop rectangles and timings in `render.py`. The renderer uses macOS Menlo, Apple Symbols, STIX Two Math, and Avenir Next fonts.

## Preview the draft

Build Jekyll with `--drafts`. The page is `/2026/09/22/introducing-crabigator/`. This session used Jekyll 4.4.1 and a temporary preview configuration that excludes the existing `tools` directory and Gemfiles. No site dependency files were changed.

The local preview is served at http://127.0.0.1:4100/2026/09/22/introducing-crabigator/ while the preview server is running.

## Capture colors correctly

The agent command environment sets `NO_COLOR=1`. Claude honors it, while Crabigator draws its widgets with explicit ANSI colors. Start recording sessions with `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor` before the Crabigator command. Check that `tmux capture-pane -ep` contains color sequences in Claude’s output before recording. Do not recolor monochrome footage by guessing.

The renderer fills Unicode block and quadrant characters to the cell edges, so the Claude crab has no font side bearings or gaps between rows.

## Matching identity chips

The question take was replaced after fixing the live dashboard session list, which omitted the stored glyph and local session ID. The replacement recording uses session `fbad78ef-b4f2-4358-a32f-1514630c2b07` (local ID `dc6d5f14a866`). Its terminal and both dashboard views show `≈△≈`, with foreground RGB `(126, 224, 232)` and background RGB `(10, 42, 50)`. The fix was deployed as Worker version `5673a051-f170-46f7-9f7b-4f07815e9c79`.
