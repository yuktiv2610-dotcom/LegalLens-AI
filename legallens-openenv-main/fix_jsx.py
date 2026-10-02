import os

def fix_file(path, replacements):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

base = 'frontend/src/'
fix_file(base + 'components/BootSequence.tsx', [('> {log}', '{">"} {log}'), ('> </div>', '{">"} </div>'), ('> READY FOR CASE', '{">"} READY FOR CASE')])
fix_file(base + 'components/EvidenceBoard.tsx', [('>> EVIDENCE BOARD', '{\">>\"} EVIDENCE BOARD')])
fix_file(base + 'pages/AgentLab.tsx', [('> LIVE EXECUTION LOG', '{">\"} LIVE EXECUTION LOG'), ('> {s.error', '{\">\"} {s.error'), ('> Reward:', '{\">\"} Reward:'), ('> </div>', '{\">\"} </div>')])
fix_file(base + 'pages/CaseAnalyzer.tsx', [('>> INVESTIGATION', '{\">>\"} INVESTIGATION'), ('> SYSTEM LOGS', '{\">\"} SYSTEM LOGS'), ('> ACTION:', '{\">\"} ACTION:'), ('> </div>', '{\">\"} </div>'), ('>> KNOWN FACTS', '{\">>\"} KNOWN FACTS'), ('>> MANUAL OVERRIDE', '{\">>\"} MANUAL OVERRIDE')])
fix_file(base + 'pages/HomeScreen.tsx', [('>> SELECT CASE FILE', '{\">>\"} SELECT CASE FILE')])
fix_file(base + 'pages/ScoreScreen.tsx', [('>> EVALUATION BREAKDOWN', '{\">>\"} EVALUATION BREAKDOWN'), ('>> FINAL ANALYSIS', '{\">>\"} FINAL ANALYSIS'), ('>> METRICS & FEEDBACK', '{\">>\"} METRICS & FEEDBACK')])
print('Replaced > and >> in components')
