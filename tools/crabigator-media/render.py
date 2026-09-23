#!/usr/bin/env python3
"""Cut recorded browser frames and terminal buffers into silent blog videos.

Requires Pillow, pyte, fonttools, and ffmpeg. Source timestamps stay on the same clock.
Terminal buffers are rendered as text; browser frames are unmodified captures.
"""
import argparse
import bisect
import json
import math
import subprocess
from functools import lru_cache
from pathlib import Path

import pyte
from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps
from fontTools.ttLib import TTFont

BG = '#090d16'
FONT = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 20)
FALLBACKS = [(FONT, TTFont('/System/Library/Fonts/Menlo.ttc', fontNumber=0).getBestCmap())]
for font_path in ['/System/Library/Fonts/Apple Symbols.ttf', '/System/Library/Fonts/Supplemental/STIXTwoMath.otf']:
    FALLBACKS.append((ImageFont.truetype(font_path, 22), TTFont(font_path).getBestCmap()))


@lru_cache(maxsize=512)
def font_for(text):
    codepoints = {ord(c) for c in text if ord(c) not in (0xfe0e, 0xfe0f)}
    return next((font for font, cmap in FALLBACKS if codepoints.issubset(cmap)), FONT)

TITLE = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 34, index=2)
CONTEXT = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 21, index=5)
NOTE = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 21, index=7)
COLORS = dict(black='#151923', red='#ff667a', green='#98d779', brown='#d7af5f',
              blue='#81a9ed', magenta='#c5a0ff', cyan='#75d7e8', white='#e4e7ef',
              brightblack='#747b8a', brightred='#ff8a9a', brightgreen='#b1ee91',
              brightbrown='#ffe29a', brightblue='#a4c5ff', brightmagenta='#dfbdff',
              brightcyan='#a1edfa', brightwhite='#ffffff')


def color(value, default):
    return default if value == 'default' else COLORS.get(value, '#' + value)


# Block elements are terminal-cell geometry, not spaced font outlines.
QUADRANTS = {
    '▖': (2,), '▗': (3,), '▘': (0,), '▙': (0, 2, 3),
    '▚': (0, 3), '▛': (0, 1, 2), '▜': (0, 1, 3),
    '▝': (1,), '▞': (1, 2), '▟': (1, 2, 3),
}


def draw_block(draw, char, x, y, fill):
    rects = []
    if char in QUADRANTS:
        for q in QUADRANTS[char]:
            rects.append((q % 2 / 2, q // 2 / 2, q % 2 / 2 + .5, q // 2 / 2 + .5))
    elif char == '▀':
        rects = [(0, 0, 1, .5)]
    elif char == '▐':
        rects = [(.5, 0, 1, 1)]
    elif '▁' <= char <= '█':
        rects = [(0, 1 - (ord(char) - 0x2580) / 8, 1, 1)]
    elif '▉' <= char <= '▏':
        rects = [(0, 0, (0x2590 - ord(char)) / 8, 1)]
    else:
        return False
    for left, top, right, bottom in rects:
        draw.rectangle((x + round(left * 12), y + round(top * 25),
                        x + round(right * 12) - 1, y + round(bottom * 25) - 1), fill=fill)
    return True


@lru_cache(maxsize=96)
def terminal(text, cols=100, rows=34):
    screen = pyte.Screen(cols, rows)
    # capture-pane supplies complete rows, without carriage returns.
    pyte.Stream(screen).feed(text.rstrip('\n').replace('\n', '\r\n'))
    im = Image.new('RGB', (cols * 12 + 32, rows * 25 + 24), BG)
    draw = ImageDraw.Draw(im)
    for y in range(rows):
        for x in range(cols):
            c = screen.buffer[y][x]
            fg, bg = color(c.fg, '#dde2ed'), color(c.bg, BG)
            if c.reverse:
                fg, bg = bg, fg
            px, py = 16 + x * 12, 12 + y * 25
            if bg != BG:
                draw.rectangle((px, py, px + 11, py + 24), fill=bg)
            if c.data.strip() and not draw_block(draw, c.data, px, py, fg):
                font = font_for(c.data)
                draw.text((px, py), c.data.replace('\ufe0e', '').replace('\ufe0f', ''), font=font, fill=fg)
    # Pairing codes grant access. Cover the code field in every terminal frame.
    for y, line in enumerate(screen.display):
        if 'Streaming ' in line:
            start = line.index('Streaming ')
            visible = line[start:start + 18].strip()
            draw.rectangle((16 + start * 12, 12 + y * 25, 16 + (start + 36) * 12, 37 + y * 25), fill=BG)
            draw.text((16 + start * 12, 12 + y * 25), visible, font=FONT, fill='#75d7e8')
    return im


class Track:
    def __init__(self, path, cols=100, rows=34):
        self.cols, self.rows = cols, rows
        if path.is_dir():
            self.data = sorted(path.glob('*.png'))
            self.times = [int(p.stem) / 1000 for p in self.data]
            self.kind = 'browser'
        else:
            self.data = [json.loads(line) for line in path.read_text().splitlines()]
            self.times = [v['timestamp'] for v in self.data]
            self.kind = 'terminal'
        if not self.data:
            raise ValueError(f'No captured frames: {path}')

    def at(self, timestamp):
        i = max(0, bisect.bisect_right(self.times, timestamp) - 1)
        if self.kind == 'browser':
            with Image.open(self.data[i]) as im:
                return im.convert('RGB')
        return terminal(self.data[i]['screen'], self.cols, self.rows)


def ease(t):
    t = max(0, min(1, t))
    return t * t * (3 - 2 * t)


def zoom(im, start, end, progress, size):
    rect = tuple(a + (b - a) * ease(progress) for a, b in zip(start, end))
    return ImageOps.fit(im.crop(rect), size, method=Image.Resampling.LANCZOS)


def panel_title(canvas, x, y, width, title, context, accent):
    draw = ImageDraw.Draw(canvas)
    base = ImageColor.getrgb(BG)
    tint = ImageColor.getrgb(accent)
    fill = tuple(round(bg * .78 + fg * .22) for bg, fg in zip(base, tint))
    draw.rounded_rectangle((x, y, x + width, y + 46), radius=11, fill=fill)
    draw.text((x + 18, y + 6), title, font=TITLE, fill='#eef1f6', anchor='lt')
    draw.text((x + width - 18, y + 13), context, font=CONTEXT,
              fill='#c1cad8', anchor='rt')



def ghostty_frame(im, title='Crabigator'):
    inset, top = 12, 48
    w, h = im.width + inset * 2, im.height + top + inset
    frame = Image.new('RGB', (w, h), BG)
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=15,
                           fill='#191c24', outline='#424753', width=2)
    for i, color in enumerate(['#ff5f57', '#febc2e', '#28c840']):
        x = 22 + i * 22
        draw.ellipse((x, 18, x + 12, 30), fill=color)
    draw.text((w // 2, 16), 'crabigator — ' + title, font=CONTEXT,
              fill='#b5bdcb', anchor='mt')
    draw.line((1, top - 1, w - 2, top - 1), fill='#303540')
    frame.paste(im, (inset, top))
    return frame


def iphone_frame(im):
    # iPhone 17 display proportions, with a safe area above and below the page.
    w, h = 414, 872
    frame = Image.new('RGB', (w, h), BG)
    draw = ImageDraw.Draw(frame)
    for box in [(0, 159, 5, 187), (0, 215, 5, 263),
                (0, 283, 5, 331), (409, 241, 413, 312)]:
        draw.rounded_rectangle(box, radius=2, fill='#666b72')
    draw.rounded_rectangle((3, 0, 410, h - 1), radius=55,
                           fill='#24272d', outline='#747982', width=2)
    draw.rounded_rectangle((7, 4, 406, h - 5), radius=51,
                           fill='#050608', outline='#363b43', width=2)
    screen = Image.new('RGB', (390, 848), '#090d16')
    # Keep the captured page's pixels and text proportions; crop below the safe area.
    page = im.resize((390, round(im.height * 390 / im.width)), Image.Resampling.LANCZOS)
    screen.paste(page.crop((0, 0, 390, 770)), (0, 54))
    sd = ImageDraw.Draw(screen)
    sd.text((31, 18), '9:41', font=CONTEXT, fill='#eef1f6', anchor='lt')
    sd.rounded_rectangle((141, 10, 249, 41), radius=16, fill='#000000')
    sd.ellipse((226, 20, 236, 30), fill='#101620')
    for i in range(4):
        sd.rounded_rectangle((282 + i * 5, 30 - i * 3, 285 + i * 5, 34), radius=1, fill='#eef1f6')
    sd.arc((307, 19, 327, 37), 220, 320, fill='#eef1f6', width=2)
    sd.arc((311, 24, 323, 37), 220, 320, fill='#eef1f6', width=2)
    sd.ellipse((316, 31, 319, 34), fill='#eef1f6')
    sd.rounded_rectangle((334, 22, 359, 34), radius=3, outline='#a6acb5', width=1)
    sd.rounded_rectangle((337, 25, 355, 31), radius=1, fill='#eef1f6')
    sd.rectangle((360, 26, 362, 30), fill='#a6acb5')
    sd.rounded_rectangle((129, 835, 261, 840), radius=3, fill='#eef1f6')
    mask = Image.new('L', screen.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 389, 847), radius=43, fill=255)
    frame.paste(screen, (12, 12), mask)
    return frame

def panel(canvas, im, box, label=None, frame=None):
    if frame == 'terminal':
        im = ghostty_frame(im, label[0] if label else 'Crabigator')
    elif frame == 'phone':
        im = iphone_frame(im)
    x, y, w, h = box
    fitted = ImageOps.contain(im, (w, h), method=Image.Resampling.LANCZOS)
    canvas.paste(fitted, (x + (w - fitted.width) // 2, y + (h - fitted.height) // 2))
    if label:
        panel_title(canvas, x, y - 50, w, *label)


def encode(output, duration, make_frame, fps=15):
    first = make_frame(0)
    w, h = first.size
    proc = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', str(fps),
        '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '19',
        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(output)], stdin=subprocess.PIPE)
    try:
        for i in range(math.ceil(duration * fps)):
            frame = make_frame(i / fps)
            proc.stdin.write(frame.tobytes())
            if i == fps * (4 if output.stem in ('glyphs', 'changes', 'pr-board') else 2):
                frame.save(output.with_suffix('.jpg'), quality=92)
    finally:
        proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f'Encoding failed: {output}')
    print(output.name, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--only', nargs='*')
    args = parser.parse_args()
    src, out = args.source, args.output
    out.mkdir(parents=True, exist_ok=True)
    clips = {}
    question = json.loads((src / 'question-timing.json').read_text())
    def recorded_time(t):
        for segment in question['segments']:
            if t < segment['duration']:
                return segment['start'] / 1000 + t
            t -= segment['duration']
        last = question['segments'][-1]
        return last['start'] / 1000 + last['duration']

    phone = Track(src / 'mobile')
    desk = Track(src / 'desktop')
    term = Track(src / 'terminal.jsonl')

    def same_session(t):
        canvas = Image.new('RGB', (1600, 1000), BG)
        panel(canvas, term.at(recorded_time(t)), (24, 80, 1136, 850), ('Claude Code', 'Terminal', '#d78787'), frame='terminal')
        panel(canvas, phone.at(recorded_time(t)), (1190, 80, 386, 850), ('Mobile', 'Dashboard', '#75d7c5'), frame='phone')
        ImageDraw.Draw(canvas).text((41, 957), 'Same session. Same moment.', font=NOTE, fill='#77869d')
        return canvas
    clips['same-session'] = (18, same_session)

    def questions(t):
        im = iphone_frame(phone.at(recorded_time(t)))
        # First establish the phone, then bring the actual answer buttons closer.
        p = ease((t - 2.3) / .8) * (1 - ease((t - 4.8) / .8))
        canvas = Image.new('RGB', (800, 1000), BG)
        crop = tuple(a + (b - a) * p for a, b in zip((0, 0, 414, 872), (12, 414, 402, 746)))
        panel(canvas, im.crop(crop), (24, 80, 752, 896), ('Answer from anywhere', 'Mobile', '#75d7c5'))
        return canvas
    clips['questions'] = (12, questions)

    def dashboard(t):
        canvas = Image.new('RGB', (1600, 1000), BG)
        panel(canvas, desk.at(recorded_time(t)), (24, 80, 1136, 850), ('Desktop', 'Dashboard', '#a99ade'))
        panel(canvas, phone.at(recorded_time(t)), (1190, 80, 386, 850), ('Mobile', 'Dashboard', '#75d7c5'), frame='phone')
        return canvas
    clips['dashboard-sync'] = (18, dashboard)

    board = Track(src / 'board-prs.jsonl', cols=140, rows=24)
    sessions = Track(src / 'board-sessions.jsonl', cols=140, rows=24)

    def pr_board(t):
        track, offset = (board, t) if t < 6 else (sessions, t - 6)
        im = ghostty_frame(track.at(track.times[0] + offset), 'PR board')
        canvas = Image.new('RGB', (1600, 900), BG)
        panel(canvas, im, (24, 90, 1552, 750),
              ('PR board', 'Two PRs' if t < 6 else 'Three sessions', '#a99ade'))
        return canvas
    clips['pr-board'] = (13, pr_board)

    def glyphs(t):
        im = ghostty_frame(board.at(board.times[0] + min(t, 5)), 'Session glyphs')
        # Start with the board, then show the two distinct Claude session marks.
        canvas = Image.new('RGB', (1280, 720), BG)
        closeup = zoom(im, (0, 0, im.width, im.height), (46, 184, 846, 584),
                       (t - 1) / 2, (1232, 612))
        panel(canvas, closeup, (24, 82, 1232, 612),
              ('Session glyphs', 'A mark for each session', '#75d7c5'))
        return canvas
    clips['glyphs'] = (8, glyphs)

    # The actual terminal widget strip shows both changed files and cursor_to.
    end_start = term.times[-1] - 12
    def changes(t):
        im = ghostty_frame(term.at(end_start + t), 'Changes')
        w, h = im.size
        canvas = Image.new('RGB', (1600, 900), BG)
        p = ease((t - .8) / 2)
        rect = tuple(a + (b - a) * p for a, b in zip((0, 0, w, h), (450, 784, w - 12, 912)))
        panel(canvas, im.crop(rect), (30, 70, 1540, 355), ('Terminal', 'Files & functions', '#d78787'))
        with Image.open(src / 'changes.png') as web:
            panel(canvas, web.crop((18, 960, 1250, 1165)), (30, 520, 1540, 330), ('Dashboard', 'The same change', '#a99ade'))
        return canvas
    clips['changes'] = (10, changes)

    providers = {name: Track(src / (name + '.jsonl')) for name in ['grok', 'opencode', 'codex']}
    provider_start = json.loads((src / 'providers-start.json').read_text())['start']
    labels = {
        'grok': ('Grok', 'Crabigator', '#d3dbe8'),
        'opencode': ('opencode', 'Crabigator', '#a99ade'),
        'codex': ('Codex', 'Crabigator', '#75d7c5'),
        'claude': ('Claude Code', 'Crabigator', '#d78787'),
    }

    def provider_frame(name, t):
        # OpenCode took longer to read the file; show the last part of that real turn.
        origin = provider_start + (22 if name == 'opencode' else 2)
        if name == 'claude':
            return term.at(recorded_time(min(t, 16)))
        return providers[name].at(origin + t)

    def four_agents(t):
        canvas = Image.new('RGB', (1600, 1000), BG)
        names = ['grok', 'opencode', 'codex', 'claude']
        if t < 3 or t >= 23:
            for i, name in enumerate(names):
                x, y = 20 + i % 2 * 800, 60 + i // 2 * 495
                panel(canvas, provider_frame(name, min(t, 9)), (x, y, 760, 420), labels[name], frame='terminal')
        else:
            i = min(3, int((t - 3) / 5))
            name = names[i]
            panel(canvas, provider_frame(name, (t - 3) % 5 + 4), (30, 70, 1540, 900), labels[name], frame='terminal')
        return canvas
    clips['four-agents'] = (26, four_agents)

    for name, (duration, render) in clips.items():
        if args.only is None or name in args.only:
            encode(out / (name + '.mp4'), duration, render)


if __name__ == '__main__':
    main()
