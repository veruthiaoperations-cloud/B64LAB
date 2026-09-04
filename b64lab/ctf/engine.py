"""
Dynamic Anti-Cheat CTF Challenge Arena Engine.
Zero Static Flags in Code. Machine-Unique HMAC-SHA256 Flag & Payload Synthesis.
Pure Python standard library implementation.
"""

import os
import json
import base64
import gzip
import hmac
import hashlib
from typing import List, Dict, Any, Optional, Tuple

from ..ui.components import UIComponents
from ..ui.themes import Theme
from ..ui.ansi import ANSI
from ..core.alphabets import Alphabets, CustomAlphabet
from ..core.signatures import SignatureDB

# Master salt component - unique per challenge
CHALLENGE_DEFINITIONS = [
    {
        "id": 1,
        "title": "Level 1: First Contact",
        "category": "Basic Decoding",
        "prefix": "first_principles",
        "description": "During a network capture audit, you intercepted this suspicious token in an Authorization header:\n\n  {payload}\n\nDecode the payload and extract your unique security flag.",
        "hint": "This is standard RFC 4648 Base64. You can use Quick Workbench [5] or Python standard decoding.",
    },
    {
        "id": 2,
        "title": "Level 2: The Broken Pad",
        "category": "Padding Evasion",
        "prefix": "pad_repaired",
        "description": "An adversary purposely stripped the padding '=' characters to evade an IDS rule:\n\n  {payload}\n\nNotice the string length is not a multiple of 4! Repair the padding to recover the flag.",
        "hint": "Calculate len(payload) % 4. If remainder is 2, append '=='. If remainder is 3, append '='.",
    },
    {
        "id": 3,
        "title": "Level 3: The Ghost Shell",
        "category": "PowerShell Forensics",
        "prefix": "utf16le_ninja",
        "description": "You retrieved a Windows Event ID 4104 log with this encoded command:\n\n  {payload}\n\nRemember: Windows PowerShell encodes commands as UTF-16LE, not UTF-8!",
        "hint": "Decode the Base64 to bytes, then decode those bytes using 'utf-16le' instead of 'ascii' or 'utf-8'.",
    },
    {
        "id": 4,
        "title": "Level 4: Needle in the Haystack",
        "category": "Log File Carving",
        "prefix": "carver_elite",
        "description": (
            "Examine this snippet from an Apache access log and carve out the hidden flag:\n\n"
            "  192.168.1.50 - - [03/Sep/2026:12:00:01] \"GET /index.html HTTP/1.1\" 200 452\n"
            "  192.168.1.55 - - [03/Sep/2026:12:00:04] \"GET /style.css HTTP/1.1\" 200 1205\n"
            "  10.0.0.99 - - [03/Sep/2026:12:01:22] \"POST /api?token={payload} HTTP/1.1\" 200 89\n"
            "  192.168.1.50 - - [03/Sep/2026:12:02:10] \"GET /favicon.ico HTTP/1.1\" 404 182\n"
        ),
        "hint": "Look for high-entropy tokens in query parameters, or run the Defensive Triage Carver [2].",
    },
    {
        "id": 5,
        "title": "Level 5: Magic Masquerade",
        "category": "File Signatures",
        "prefix": "pe_magic",
        "description": (
            "A suspicious blob was found uploaded as an 'avatar.png' image:\n\n"
            "  {payload}\n\n"
            "What type of file is REALLY disguised inside this Base64 payload? (Enter: EXE or PE)"
        ),
        "hint": "Decode the first 4 bytes. Notice '4D 5A' in hex, or 'MZ' in ASCII. What file format starts with 'MZ'?",
    },
    {
        "id": 6,
        "title": "Level 6: The Russian Doll",
        "category": "Multi-Stage Droppers",
        "prefix": "nest_unpacker",
        "description": (
            "A threat actor used multi-stage nesting: Plaintext Flag -> GZIP Compressed -> Base64 Encoded.\n"
            "Here is the stager:\n\n"
            "  {payload}\n\n"
            "Decompress and unroll the layers to recover the flag."
        ),
        "hint": "Decode Base64, check for the 1F 8B GZIP header, and decompress with gzip.decompress() or use Triage [3].",
    },
    {
        "id": 7,
        "title": "Level 7: The Shifted Table",
        "category": "Custom Alphabets",
        "prefix": "reversed_cipher",
        "description": (
            "An APT group used a reversed Base64 alphabet to bypass static YARA signatures:\n"
            "Alphabet: /+9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA\n\n"
            "Ciphertext:\n"
            "  {payload}\n\n"
            "Reverse the custom alphabet and retrieve your unique flag."
        ),
        "hint": "Use CustomAlphabet.translate_custom_to_standard with the reversed alphabet, then decode.",
    },
    {
        "id": 8,
        "title": "Level 8: Incident Response Final",
        "category": "Full Triage Incident",
        "prefix": "soc_commander",
        "description": (
            "Incident Alert #9042: C2 Beacon detected over DNS query.\n"
            "The exfiltrated DNS query is:\n"
            "  payload.{payload}.c2-threat-domain.net\n\n"
            "Carve the subdomain token and submit your unique incident flag to close the ticket."
        ),
        "hint": "Carve the token between 'payload.' and '.c2-threat-domain.net', decode it, and extract the flag.",
    },
]

class CTFAntiCheat:
    """Cryptographic Flag & Payload Synthesis Engine."""

    STATE_FILE = os.path.join(os.path.expanduser("~"), ".b64lab_profile.json")

    @classmethod
    def get_state_file(cls) -> str:
        """Returns the active state file path, checking user home first with legacy fallback."""
        local_legacy = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".b64lab_profile.json")
        if os.path.exists(local_legacy) and not os.path.exists(cls.STATE_FILE):
            return local_legacy
        return cls.STATE_FILE

    @classmethod
    def get_or_create_seed(cls) -> str:
        """Retrieves or creates a cryptographically random machine/user salt."""
        state_file = cls.get_state_file()
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f:
                    data = json.load(f)
                    if "salt" in data and len(data["salt"]) == 32:
                        return data["salt"]
            except Exception:
                pass

        # Generate a new 128-bit cryptographic salt
        new_salt = hashlib.sha256(os.urandom(32)).hexdigest()[:32]
        cls._save_profile_data({"salt": new_salt, "solved": []})
        return new_salt

    @classmethod
    def _save_profile_data(cls, data: Dict[str, Any]) -> None:
        state_file = cls.get_state_file()
        try:
            with open(state_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            # Fallback to local directory if home directory is not writable
            try:
                local_fallback = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".b64lab_profile.json")
                with open(local_fallback, "w") as f:
                    json.dump(data, f, indent=2)
            except Exception:
                pass

    @classmethod
    def _load_profile_data(cls) -> Dict[str, Any]:
        state_file = cls.get_state_file()
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"salt": cls.get_or_create_seed(), "solved": []}

    @classmethod
    def derive_flag(cls, challenge_id: int, salt: str) -> str:
        """Derives a mathematically unpredictable, unique flag using HMAC-SHA256."""
        c_def = next(c for c in CHALLENGE_DEFINITIONS if c["id"] == challenge_id)
        if challenge_id == 5:
            # Challenge 5 is identifying the file format (EXE / PE)
            return "EXE"

        key = f"B64LAB_CTF_KEY_2026_{challenge_id}".encode()
        msg = f"{salt}:{c_def['prefix']}:{challenge_id}".encode()
        token = hmac.new(key, msg, hashlib.sha256).hexdigest()[:10]
        return f"RFC4648{{{c_def['prefix']}_{token}}}"

    @classmethod
    def synthesize_challenge(cls, challenge_id: int, salt: str) -> Dict[str, Any]:
        """
        Dynamically synthesizes the challenge prompt and payload for this user session.
        ZERO static flags or payloads exist in the codebase!
        """
        c_def = next(c for c in CHALLENGE_DEFINITIONS if c["id"] == challenge_id)
        flag = cls.derive_flag(challenge_id, salt)

        # Synthesize payload based on challenge mechanics
        if challenge_id == 1:
            # Standard Base64
            payload = base64.b64encode(flag.encode()).decode()

        elif challenge_id == 2:
            # Base64 with stripped padding
            std_b64 = base64.b64encode(flag.encode()).decode()
            payload = std_b64.rstrip("=")

        elif challenge_id == 3:
            # PowerShell UTF-16LE
            payload = base64.b64encode(flag.encode("utf-16le")).decode()

        elif challenge_id == 4:
            # Query parameter payload
            payload = base64.b64encode(flag.encode()).decode()

        elif challenge_id == 5:
            # Windows PE executable signature simulation (synthesized dynamically in memory)
            pe_header = bytes([0x4D, 0x5A]) + bytes([0x90, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00]) + bytes(48)
            payload = base64.b64encode(pe_header).decode()

        elif challenge_id == 6:
            # Multi-stage: Plaintext -> GZIP -> Base64
            compressed = gzip.compress(flag.encode())
            payload = base64.b64encode(compressed).decode()

        elif challenge_id == 7:
            # Custom reversed alphabet
            std_b64 = base64.b64encode(flag.encode()).decode()
            rev_alpha = "/+9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA"
            payload = CustomAlphabet.translate_standard_to_custom(std_b64, rev_alpha)

        elif challenge_id == 8:
            # DNS token
            payload = base64.b64encode(flag.encode()).decode()

        else:
            payload = ""

        formatted_prompt = c_def["description"].format(payload=payload)

        return {
            "id": challenge_id,
            "title": c_def["title"],
            "category": c_def["category"],
            "prompt": formatted_prompt,
            "payload": payload,
            "flag": flag,
            "accepted_flags": ["EXE", "PE", "PORTABLE EXECUTABLE", ".EXE"] if challenge_id == 5 else [flag],
            "hint": c_def["hint"],
        }


class CTFArena:
    """CTF Challenge Arena Controller with Dynamic Flag Verification."""

    @classmethod
    def run(cls) -> None:
        """Main CTF loop."""
        profile = CTFAntiCheat._load_profile_data()
        salt = profile["salt"]

        while True:
            solved_ids = set(profile.get("solved", []))
            score = len(solved_ids) * 100
            total_possible = len(CHALLENGE_DEFINITIONS) * 100

            palette = Theme.get_palette()
            s = palette.secondary
            succ = palette.success
            r = ANSI.RESET

            UIComponents.header(
                f"CTF CHALLENGE ARENA  [SCORE: {score}/{total_possible} PTS]  [SALT: {salt[:8]}...]",
                "8 Cryptographically Synthesized Forensic Labs with Anti-Cheat Protection"
            )

            print(f"  {s}STATUS    ID   CHALLENGE TITLE                CATEGORY{r}")
            print(f"  {palette.dim}────────  ───  ─────────────────────────────  ─────────────────────{r}")

            for c_def in CHALLENGE_DEFINITIONS:
                is_solved = c_def["id"] in solved_ids
                status_str = f"{succ}[SOLVED]{r}" if is_solved else f"{palette.dim}[ACTIVE]{r}"
                print(f"  {status_str}  #{c_def['id']:02d}  {c_def['title'].ljust(29)}  {c_def['category']}")

            print("\n  [0] Return to Main Menu\n")

            sel = UIComponents.prompt("Select challenge number (1-8 or 0)")
            if sel == "0":
                break
            try:
                num = int(sel)
                if 1 <= num <= len(CHALLENGE_DEFINITIONS):
                    # Synthesize challenge dynamically for this session
                    active_challenge = CTFAntiCheat.synthesize_challenge(num, salt)
                    cls._play_challenge(active_challenge, profile)
                else:
                    print("  [!] Invalid challenge number.")
            except ValueError:
                pass

    @classmethod
    def _play_challenge(cls, challenge: Dict[str, Any], profile: Dict[str, Any]) -> None:
        solved_ids = set(profile.get("solved", []))
        is_solved = challenge["id"] in solved_ids
        palette = Theme.get_palette()
        r = ANSI.RESET

        UIComponents.header(challenge["title"], f"Category: {challenge['category']}")
        print(f"\n{challenge['prompt']}\n")

        if is_solved:
            print(f"  {palette.success}[✓] YOU HAVE ALREADY SOLVED THIS CHALLENGE!{r}\n")

        print("  [H] View Hint")
        print("  [S] Submit Flag")
        print("  [0] Return to Arena")

        while True:
            action = UIComponents.prompt("Choose action (H/S/0)")
            if action == "0":
                break
            elif action.upper() == "H":
                print(f"\n  {palette.secondary}[HINT]: {challenge['hint']}{r}\n")
            elif action.upper() == "S":
                guess = input("\n  Enter Flag: ").strip()
                accepted = [a.upper() for a in challenge.get("accepted_flags", [challenge["flag"]])]
                if guess.upper() in accepted:
                    print(f"\n  {palette.success}{ANSI.BOLD}[★] FLAG ACCEPTED! CHALLENGE COMPLETE! (+100 PTS){r}\n")
                    if challenge["id"] not in solved_ids:
                        solved_ids.add(challenge["id"])
                        profile["solved"] = list(solved_ids)
                        CTFAntiCheat._save_profile_data(profile)
                    UIComponents.pause()
                    break
                else:
                    print(f"\n  {ANSI.BRIGHT_RED}[✗] INCORRECT FLAG. Check your decoding and try again.{r}\n")
