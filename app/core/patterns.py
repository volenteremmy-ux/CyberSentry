import re

# 1. KNOWN SAFE SENDERS (Whitelist)
WHITELIST = ["MPESA", "M-PESA", "SAFARICOM", "KCB", "EQUITY", "CO-OP", "NCBA", "KRA", "ABSA", "STANCHART"]

# 2. FRAUD PATTERNS
SCAM_PATTERNS = {
    "technical_attack": [
        r"\*33\*\d+", r"bit\.ly", r"tinyurl", r"http:\/\/", r"\.apk"
    ],
    "social_engineering": [
        r"imefungiwa", r"fungiwa", r"suspended", r"reward", r"zawadi", 
        r"winner", r"reverse", r"dial", r"pin", r"password", r"unlock"
    ],
    "urgency": [
        r"haraka", r"immediately", r"urgent", r"leo", r"today", r"now", r"within"
    ],
    "threats": [
        r"kill", r"kil ", r"die", r"death", r"police", r"arrest", r"shika",
        r"mtoto", r"kidnap", r"bullet", r"snet" 
    ]
}

# 3. SAFE PATTERNS (NEW) - If these match, we lower the risk immediately
SAFE_PATTERNS = [
    r"transaction.*declined",
    r"insufficient funds",
    r"balance is",
    r"confirmed\. on",
    r"sent to",
    r"received from",
    r"withdraw",
    r"tuition",
    r"school fees",
    r"payment of"
]

WEIGHTS = {
    "technical_attack": 60,
    "social_engineering": 30,
    "urgency": 20,
    "impersonation": 50,
    "threats": 85
}