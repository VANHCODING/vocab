# -*- coding: utf-8 -*-
with open(r"C:\Users\vanh\.gemini\antigravity\scratch\lexiup\index.html", "r", encoding="utf-8") as f:
    html = f.read()

required_ids = [
    'view-home', 'view-library', 'view-session', 'view-summary', 'view-progress', 'view-settings',
    'dash-streak-count', 'dash-xp-count', 'dash-goal-text', 'btn-start-continue-learn', 'btn-start-due-review',
    'library-search-input', 'library-topic-grid', 'session-stage-root', 'btn-session-exit',
    'modal-topic-preview', 'modal-import-vocab', 'modal-confirm-exit', 'modal-confirm-reset',
    'confetti-canvas', 'toast-container'
]

missing = [i for i in required_ids if f'id="{i}"' not in html]
if missing:
    print("Missing IDs:", missing)
    exit(1)
else:
    print(f"PASS: All {len(required_ids)} required DOM IDs are present!")
    print(f"Total HTML file size: {len(html)} bytes")
