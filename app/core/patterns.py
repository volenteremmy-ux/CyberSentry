import re

# 1. KNOWN SAFE SENDERS (Whitelist)
WHITELIST = ["MPESA", "M-PESA", "SAFARICOM", "KCB", "EQUITY", "CO-OP", "NCBA", "KRA"]

# 2. FRAUD PATTERNS
SCAM_PATTERNS = {
    "technical_attack": [
        r"\*33\*\d+",          # USSD Forwarding
        r"bit\.ly",            # Short links
        r"tinyurl",
        r"http:\/\/",          # Insecure links
        r"\.apk",              # Malicious apps
    ],
    "social_engineering": [
        r"imefungiwa",         # Blocked
        r"fungiwa",            # Blocked (root)
        r"suspended",
        r"reward",
        r"zawadi",
        r"winner",
        r"reverse",
        r"dial",
        r"pin",
        r"password",
        r"unlock",
    ],
    "urgency": [
        r"haraka",
        r"immediately",
        r"urgent",
        r"leo",
        r"today",
        r"now",
        r"within",
    ],
    # NEW: THREATS & EXTORTION (Catches "kill", "die", etc.)
    "threats": [
        r"kill", r"kil ", r"die", r"death", r"police", r"arrest", r"shika",
        r"mtoto", r"kidnap", r"bullet", r"snet" 
    ]
}

WEIGHTS = {
    "technical_attack": 60,
    "social_engineering": 30,
    "urgency": 20,
    "impersonation": 50,
    "threats": 85  # Highest danger level
}