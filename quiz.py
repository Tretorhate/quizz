import json
import os
import random
import time

# Colors
R  = "\033[0m"
B  = "\033[1m"
DIM= "\033[2m"
CY = "\033[96m"
YL = "\033[93m"
GR = "\033[92m"
RD = "\033[91m"
MG = "\033[95m"
BL = "\033[94m"
WH = "\033[97m"

LETTERS = ["1", "2", "3", "4"]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"{CY}{B}")
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║     DISTRIBUTED COMPUTING — FINAL EXAM PREP          ║")
    print("  ║               Astana IT University                   ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print(f"{R}")

def divider():
    print(f"{DIM}  {'─' * 60}{R}")

def load_questions(path="questions.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, path)
    with open(full_path, encoding="utf-8") as f:
        return json.load(f)

def get_lectures(questions):
    seen = []
    for q in questions:
        if q["lecture"] not in seen:
            seen.append(q["lecture"])
    return seen

def prompt_int(msg, lo, hi):
    while True:
        try:
            val = int(input(msg))
            if lo <= val <= hi:
                return val
            print(f"{RD}  Enter a number between {lo} and {hi}.{R}")
        except ValueError:
            print(f"{RD}  Please enter a valid number.{R}")

def main_menu(questions):
    lectures = get_lectures(questions)
    while True:
        clear()
        banner()
        print(f"  {WH}{B}MAIN MENU{R}\n")
        print(f"  {BL}1{R}  ›  {WH}Full Exam (182 questions){R}")
        print(f"  {BL}2{R}  ›  {WH}Quick Quiz (random){R}")
        print(f"  {BL}3{R}  ›  {WH}Quiz by Lecture{R}")
        print(f"  {BL}4{R}  ›  {WH}Score History{R}")
        print(f"  {BL}5{R}  ›  {WH}Quit{R}\n")
        choice = prompt_int(f"  {CY}Choose (1-5): {R}", 1, 5)

        if choice == 1:
            run_quiz(questions, label="Full Final Exam")
        elif choice == 2:
            quick_quiz(questions)
        elif choice == 3:
            lecture_quiz(questions, lectures)
        elif choice == 4:
            show_history()
        elif choice == 5:
            clear()
            print(f"\n  {GR}{B}Good luck on your Distributed Computing final! 🚀{R}\n")
            break

def quick_quiz(questions):
    clear()
    banner()
    n = prompt_int(f"  {CY}How many questions? (1-{len(questions)}): {R}", 1, len(questions))
    selected = random.sample(questions, n)
    run_quiz(selected, label=f"Quick Quiz ({n}Q)")

def lecture_quiz(questions, lectures):
    clear()
    banner()
    print(f"  {WH}{B}QUIZ BY LECTURE{R}\n")
    for i, lec in enumerate(lectures, 1):
        count = sum(1 for q in questions if q["lecture"] == lec)
        print(f"  {BL}{i}{R}  ›  {WH}{lec}{R}  {DIM}({count} questions){R}")
    print()
    choice = prompt_int(f"  {CY}Choose lecture (1-{len(lectures)}): {R}", 1, len(lectures))
    chosen = lectures[choice - 1]
    filtered = [q for q in questions if q["lecture"] == chosen]
    run_quiz(filtered, label=chosen)

def run_quiz(questions, label="Quiz"):
    questions = list(questions)
    random.shuffle(questions)
    score = 0
    total = len(questions)
    wrong = []
    start = time.time()

    for idx, q in enumerate(questions, 1):
        clear()
        banner()
        print(f"  {YL}{idx}/{total}{R}   {MG}{label}{R}")
        print(f"  {DIM}Lecture: {q['lecture']}{R}")
        divider()
        print(f"\n  {WH}{B}Q{idx}. {q['question']}{R}\n")

        opts = list(enumerate(q["options"]))
        random.shuffle(opts)
        display_map = {}
        for i, (orig_idx, text) in enumerate(opts):
            letter = LETTERS[i]
            display_map[letter] = orig_idx
            print(f"  {BL}[{letter}]{R}  {text}")

        divider()
        while True:
            raw = input(f"\n  {CY}Your answer ({'/'.join(LETTERS[:len(q['options'])])}): {R}").strip().upper()
            if raw in display_map:
                break
            print(f"  {RD}Invalid choice.{R}")

        chosen_orig = display_map[raw]
        correct_orig = q["answer"]
        correct_letter = next(l for l, oi in display_map.items() if oi == correct_orig)

        print()
        if chosen_orig == correct_orig:
            score += 1
            print(f"  {GR}{B}✔ Correct!{R}")
        else:
            wrong.append(q)
            print(f"  {RD}{B}✘ Wrong.{R}  Correct: {GR}[{correct_letter}] {q['options'][correct_orig]}{R}")

        print(f"\n  {DIM}💡 {q['explanation']}{R}")
        divider()
        input(f"\n  {DIM}Press Enter for next...{R}")

    elapsed = int(time.time() - start)
    mins, secs = divmod(elapsed, 60)
    show_results(score, total, wrong, mins, secs, label)

def show_results(score, total, wrong, mins, secs, label):
    clear()
    banner()
    pct = score / total * 100
    grade = "EXCELLENT" if pct >= 90 else "GOOD" if pct >= 75 else "PASS" if pct >= 60 else "NEEDS WORK"
    color = GR if pct >= 75 else YL if pct >= 60 else RD

    print(f"  {WH}{B}RESULTS — {label}{R}")
    divider()
    print(f"\n  Score   :  {color}{B}{score}/{total} ({pct:.1f}%){R}")
    print(f"  Grade   :  {color}{B}{grade}{R}")
    print(f"  Time    :  {mins}m {secs}s\n")

    save_history(label, score, total, pct, mins, secs)

    if wrong:
        print(f"  {RD}{B}Missed questions:{R}")
        for q in wrong:
            print(f"\n  {YL}•{R} {q['question']}")
            print(f"    {GR}✔ {q['options'][q['answer']]}{R}")

    divider()
    input(f"\n  {DIM}Press Enter to return...{R}")

HISTORY_FILE = "quiz_history.json"

def save_history(label, score, total, pct, mins, secs):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    history.append({
        "label": label,
        "score": score,
        "total": total,
        "percent": round(pct, 1),
        "time": f"{mins}m {secs}s",
        "timestamp": time.strftime("%Y-%m-%d %H:%M")
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def show_history():
    clear()
    banner()
    print(f"  {WH}{B}SCORE HISTORY{R}\n")
    if not os.path.exists(HISTORY_FILE):
        print(f"  {DIM}No history yet.{R}")
    else:
        with open(HISTORY_FILE) as f:
            history = json.load(f)
        for h in reversed(history[-10:]):
            color = GR if h["percent"] >= 75 else YL if h["percent"] >= 60 else RD
            print(f"  {h['timestamp']}  {h['label'][:35]:<35}  {color}{B}{h['score']}/{h['total']} ({h['percent']}%){R}  {h['time']}")
    divider()
    input(f"\n  {DIM}Press Enter...{R}")

if __name__ == "__main__":
    questions = load_questions()
    main_menu(questions)