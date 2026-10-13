#!/usr/bin/env python3
"""
AIMLOCK X.509 — Free Fire Sensitivity & Precision Trainer
Local practice utility. Does not connect to, modify, or automate Free Fire.
Compatible with Python 3 on iSH/Alpine where supported.
"""
import json
import math
import random
import time
from pathlib import Path

CONFIG = Path(__file__).with_name("aimlock_config.json")

DEFAULTS = {
    "game": "Free Fire",
    "device": "iPhone",
    "sensitivity": {
        "general": 90,
        "red_dot": 85,
        "2x_scope": 80,
        "4x_scope": 75,
        "sniper_scope": 50,
        "free_look": 70
    },
    "notes": "Starting values only. Adjust gradually based on comfort and practice."
}

def load_config():
    if CONFIG.exists():
        try:
            data = json.loads(CONFIG.read_text())
            return data
        except (OSError, json.JSONDecodeError):
            print("Config unreadable; loading defaults.")
    save_config(DEFAULTS)
    return json.loads(json.dumps(DEFAULTS))

def save_config(data):
    CONFIG.write_text(json.dumps(data, indent=2))

def show_settings(cfg):
    print("\n--- Sensitivity profile ---")
    for key, value in cfg["sensitivity"].items():
        print(f"{key.replace('_', ' ').title():16}: {value}")
    print("\nThese are editable practice notes, not game settings applied automatically.")

def edit_settings(cfg):
    print("\nEnter values from 0 to 100. Press Enter to keep the current value.")
    for key, old in cfg["sensitivity"].items():
        raw = input(f"{key.replace('_', ' ').title()} [{old}]: ").strip()
        if not raw:
            continue
        try:
            val = int(raw)
            if 0 <= val <= 100:
                cfg["sensitivity"][key] = val
            else:
                print("Value must be between 0 and 100; unchanged.")
        except ValueError:
            print("Not a number; unchanged.")
    save_config(cfg)
    print("Profile saved locally.")

def reaction_test():
    print("\nReaction test: press Enter as soon as GO appears.")
    input("Press Enter when ready...")
    delay = random.uniform(2.0, 5.0)
    time.sleep(delay)
    print("\nGO!")
    start = time.perf_counter()
    input()
    ms = (time.perf_counter() - start) * 1000
    print(f"Reaction time: {ms:.0f} ms")
    if ms < 250:
        print("Fast response. Repeat several rounds for a more useful average.")
    elif ms < 400:
        print("Good baseline. Practice consistency.")
    else:
        print("Try again when rested and avoid rushing.")

def tracking_drill():
    print("\nTracking drill (text-based):")
    print("Imagine following each target smoothly; type its number when shown.")
    rounds = 5
    results = []
    for i in range(1, rounds + 1):
        target = random.randint(1, 9)
        input(f"Round {i}/{rounds}: press Enter to reveal target...")
        start = time.perf_counter()
        answer = input(f"TARGET: {target}  | Enter the number: ").strip()
        elapsed = (time.perf_counter() - start) * 1000
        hit = answer == str(target)
        results.append((hit, elapsed))
        print(("Correct" if hit else "Miss") + f" — {elapsed:.0f} ms")
    accuracy = sum(hit for hit, _ in results) / rounds * 100
    avg = sum(ms for _, ms in results) / rounds
    print(f"\nAccuracy: {accuracy:.0f}% | Average response: {avg:.0f} ms")
    print("This is a simple reaction/attention drill, not an in-game aim measurement.")

def main():
    cfg = load_config()
    while True:
        print("\n================================")
        print(" AIMLOCK X.509 | FREE FIRE")
        print(" Sensitivity & Precision Trainer")
        print("================================")
        print("1. View sensitivity profile")
        print("2. Edit/save sensitivity profile")
        print("3. Reaction-time test")
        print("4. Target attention drill")
        print("5. Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            show_settings(cfg)
        elif choice == "2":
            edit_settings(cfg)
        elif choice == "3":
            reaction_test()
        elif choice == "4":
            tracking_drill()
        elif choice == "5":
            print("Profile saved. Goodbye.")
            break
        else:
            print("Choose 1–5.")

if __name__ == "__main__":
    main()