#!/usr/bin/env python3
"""
Captures real terminal screenshots of the running Lernmaterialverwaltung app.
Uses pywinpty PTY + threaded reader + pyte VT100 emulator.
"""
import sys, os, time, re, io, threading, queue

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

import winpty, pyte
from rich.console import Console
from rich.text import Text

os.makedirs('screenshots', exist_ok=True)

DB_ENV = {
    'FORCE_COLOR':      '1',
    'PYTHONIOENCODING': 'utf-8',
    'DB_USERNAME':      os.getenv('DB_USERNAME', ''),
    'DB_PASSWORD':      os.getenv('DB_PASSWORD', ''),
    'DB_HOST':          os.getenv('DB_HOST', ''),
    'DB_PORT':          os.getenv('DB_PORT', '3306'),
    'DB_NAME':          os.getenv('DB_NAME', ''),
    'PATH':             os.environ.get('PATH', ''),
    'SYSTEMROOT':       os.environ.get('SYSTEMROOT', ''),
    'APPDATA':          os.environ.get('APPDATA', ''),
    'USERPROFILE':      os.environ.get('USERPROFILE', ''),
}

COLS = 100
ROWS = 60
STRIP_RE = re.compile(r'\x1b\[[0-9;?]*[a-zA-Z]')


def start_reader(p, q):
    """Read PTY in background thread, push chunks onto queue."""
    def _read():
        while True:
            try:
                chunk = p.read(4096)
                if chunk:
                    q.put(chunk)
            except Exception:
                q.put(None)
                return
    t = threading.Thread(target=_read, daemon=True)
    t.start()
    return t


def drain(q, timeout=0.3):
    """Drain queue for up to `timeout` seconds, return all collected text."""
    buf = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            chunk = q.get(timeout=0.05)
            if chunk is None:
                break
            buf.append(chunk)
        except Exception:
            pass
    return ''.join(buf)


def wait_for(q, sentinel, total_timeout=12.0):
    """Collect output until `sentinel` appears in plain text, or timeout."""
    buf = []
    deadline = time.time() + total_timeout
    while time.time() < deadline:
        try:
            chunk = q.get(timeout=0.1)
            if chunk is None:
                break
            buf.append(chunk)
            plain = STRIP_RE.sub('', ''.join(buf))
            if sentinel in plain:
                time.sleep(0.1)
                buf.append(drain(q, 0.3))
                return ''.join(buf)
        except Exception:
            pass
    return ''.join(buf)


def run_session(steps):
    """
    steps = list of (keystroke, wait_sentinel, extra_wait_sec)
    Returns full ANSI output string.
    """
    p = winpty.PtyProcess.spawn(
        'python -X utf8 app/main.py',
        dimensions=(ROWS, COLS),
        env=DB_ENV
    )
    q = queue.Queue()
    start_reader(p, q)

    print('    connecting to DB...')
    out = wait_for(q, 'Auswahl:', total_timeout=15.0)
    all_out = out

    for keystroke, sentinel, extra_wait in steps:
        p.write(keystroke + '\r')
        out = wait_for(q, sentinel, total_timeout=10.0)
        if extra_wait > 0:
            time.sleep(extra_wait)
            out += drain(q, 0.5)
        all_out += out

    try:
        p.close()
    except Exception:
        pass
    return all_out


def ansi_to_screen(ansi_text):
    screen = pyte.Screen(COLS, ROWS)
    stream = pyte.ByteStream(screen)
    stream.feed(ansi_text.encode('utf-8', errors='replace'))
    return screen


def screen_to_svg(screen, name, svg_title):
    buf = io.StringIO()
    c = Console(record=True, force_terminal=True, width=COLS,
                color_system="truecolor", file=buf)

    NAMED = {
        'default': 'white', 'black': 'black', 'red': 'red',
        'green': 'green', 'brown': 'dark_orange', 'blue': 'blue',
        'magenta': 'magenta', 'cyan': 'cyan', 'white': 'white',
    }

    # find last non-empty row
    last_row = 0
    for row_idx in range(ROWS):
        line = ''.join(
            screen.buffer[row_idx].get(col, pyte.screens.Char(' ')).data
            for col in range(COLS)
        ).rstrip()
        if line:
            last_row = row_idx

    for row_idx in range(last_row + 2):
        text = Text()
        for col_idx in range(COLS):
            ch_obj = screen.buffer[row_idx].get(col_idx, pyte.screens.Char(' '))
            ch = ch_obj.data if ch_obj.data else ' '
            fg_raw = getattr(ch_obj, 'fg', 'default')
            bold   = getattr(ch_obj, 'bold', False)
            fg = NAMED.get(fg_raw, fg_raw if fg_raw not in ('default', '') else 'white')
            text.append(ch, style=('bold ' if bold else '') + fg)
        c.print(text, end='\n', highlight=False)

    svg_path = f'screenshots/{name}.svg'
    c.save_svg(svg_path, title=svg_title)
    print(f'    -> {svg_path}')
    return svg_path


def to_png():
    import subprocess
    r = subprocess.run(['node', 'svg_to_png.js'], capture_output=True, text=True,
                       cwd=os.path.dirname(__file__))
    for line in r.stdout.strip().splitlines():
        print('   ', line)


# ── 1: Main menu ──────────────────────────────────────────────────────────────
print('\n[1/3] Main menu...')
out1 = run_session([])
screen_to_svg(ansi_to_screen(out1), 'menu', 'Hauptmenü der Lernmaterialverwaltung')

# ── 2: Materialliste (6 → 1) ──────────────────────────────────────────────────
print('\n[2/3] Materials list...')
out2 = run_session([
    ('6', 'Auswahl:', 0.3),  # listen-submenu
    ('1', 'Auswahl:', 2.5),  # show table, wait for DB query
])
screen_to_svg(ansi_to_screen(out2), 'materials', 'Materialliste der Lernmaterialverwaltung')

# ── 3: SQL Abfrage 1 (7 → 1) ─────────────────────────────────────────────────
print('\n[3/3] SQL Query 1...')
out3 = run_session([
    ('7', 'Auswahl:', 0.3),  # abfragen-submenu
    ('1', 'Auswahl:', 2.5),  # COUNT query result
])
screen_to_svg(ansi_to_screen(out3), 'query1', 'SQL-Abfrage 1: Materialien pro Themengebiet')

# ── Convert SVGs → PNGs ───────────────────────────────────────────────────────
print('\nConverting SVGs → PNGs...')
to_png()
print('\nDone. Check screenshots/ folder.')
