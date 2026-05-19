# advanced_risk_engine.py
# ضعه في نفس مجلد AOF.py

import sqlite3
import time
import datetime
from typing import Tuple

try:
    import win32api
    import win32security
    import win32con
    import psutil
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════
# الجزء 1 — الأوزان الأساسية
# ═══════════════════════════════════════════════════════════════

PORT_RISK = {
    "critical": {
        "ports": ["3389", "445", "23", "4444", "5900", "5985", "5986"],
        "score": 50
    },
    "high": {
        "ports": ["22", "21", "135", "139", "1433", "3306", "5432", "27017"],
        "score": 40
    },
    "medium": {
        "ports": ["80", "443", "8080", "8443", "8888"],
        "score": 15
    },
    "low": {
        "ports": ["53", "123", "67", "68"],
        "score": 5
    },
}

BASE_WEIGHTS = {
    "operation": {
        "ADD":    30,
        "DELETE": 40,
        "MODIFY": 35
    },
    "signature": {
        "Valid":         -40,
        "NotSigned":     +50,
        "UntrustedRoot": +60,
        "HashMismatch":  +80,
        "Revoked":       +70,
        "NotTrusted":    +35,
        "UnknownError":  +20,
        "Expired":       +25
    },
    "direction": {
        "Inbound":  +35,
        "Outbound": +20
    },
    "action": {
        "Allow": +25,
        "Block":  +10
    },
    "protocol": {
        "Any":  +30,
        "TCP":  +15,
        "UDP":  +20,
        "ICMP": +10
    },
    "ip_scope": {
        "Any":           +35,
        "Public IP":     +40,
        "Trusted IP":    +10,
        "Local Network": +5,
        "Localhost":     -30
    }
}


def _get_port_score(port: str) -> int:
    port = str(port).strip()
    if port == "Any":
        return 30
    for category, data in PORT_RISK.items():
        if port in data["ports"]:
            return data["score"]
    return 10  # منفذ غير مصنف


def calculate_base_score(operation: str, signature: str, action: str,
                          direction: str, protocol: str,
                          port: str, ip_scope: str) -> int:
    score = 0
    score += BASE_WEIGHTS["operation"].get(operation, 35)
    score += BASE_WEIGHTS["signature"].get(signature.strip(), 20)
    score += BASE_WEIGHTS["direction"].get(direction, 20)
    score += BASE_WEIGHTS["action"].get(action, 20)
    score += BASE_WEIGHTS["protocol"].get(protocol, 15)
    score += BASE_WEIGHTS["ip_scope"].get(ip_scope, 20)
    score += _get_port_score(port)
    return score


# ═══════════════════════════════════════════════════════════════
# الجزء 2 — صلاحيات العملية
# ═══════════════════════════════════════════════════════════════

def get_process_role(pid) -> str:
    """
    تحدد مستوى صلاحيات العملية بناءً على PID.
    تُستدعى في mal_dit() فور اكتشاف العملية.

    الإرجاع: "SYSTEM" | "ADMIN" | "USER" | "UNKNOWN"
    """
    if not WIN32_AVAILABLE:
        return "UNKNOWN"

    try:
        pid = int(pid)
        process  = psutil.Process(pid)
        username = process.username()

        # عمليات النظام الأساسية
        system_accounts = [
            "NT AUTHORITY\\SYSTEM",
            "NT AUTHORITY\\LOCAL SERVICE",
            "NT AUTHORITY\\NETWORK SERVICE",
            "SYSTEM"
        ]
        for acc in system_accounts:
            if acc.lower() in username.lower():
                return "SYSTEM"

        # فحص UAC token — هل العملية مرفوعة الصلاحيات؟
        handle = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION, False, pid
        )
        token_handle = win32security.OpenProcessToken(
            handle, win32con.TOKEN_QUERY
        )
        elevation = win32security.GetTokenInformation(
            token_handle,
            win32security.TokenElevation
        )
        win32api.CloseHandle(handle)

        return "ADMIN" if elevation else "USER"

    except psutil.NoSuchProcess:
        # العملية انتهت قبل الفحص — مشبوه
        return "UNKNOWN"
    except psutil.AccessDenied:
        # لا نستطيع الوصول — مشبوه
        return "UNKNOWN"
    except Exception:
        return "UNKNOWN"


# ═══════════════════════════════════════════════════════════════
# الجزء 3 — مضاعف السياق
# ═══════════════════════════════════════════════════════════════

def get_context_multiplier(user_role: str, timestamp: float,
                           work_start: int = 8,
                           work_end:   int = 18,
                           work_days: list = None) -> float:
    """
    work_start : ساعة بداية العمل (0-23)
    work_end   : ساعة نهاية العمل (0-23)
    work_days  : قائمة أيام العمل [0=الإثنين ... 6=الأحد]
                 القيمة الافتراضية: الإثنين إلى الجمعة
    """
    if work_days is None:
        work_days = [0, 1, 2, 3, 4]  # الافتراضي

    multiplier = 1.0
    dt      = datetime.datetime.fromtimestamp(timestamp)
    hour    = dt.hour
    weekday = dt.weekday()

    # هل الوقت الحالي ضمن ساعات العمل المحددة من المستخدم؟
    is_working_hours = (work_start <= hour < work_end) and (weekday in work_days)

    if not is_working_hours:
        multiplier *= 1.8

    if weekday not in work_days:
        multiplier *= 1.5

    if 0 <= hour <= 5:
        multiplier *= 2.2

    role_map = {
        "SYSTEM":  0.6,
        "ADMIN":   0.8,
        "USER":    1.5,
        "UNKNOWN": 2.5
    }
    multiplier *= role_map.get(user_role.upper(), 2.5)
    return round(multiplier, 2)


# ═══════════════════════════════════════════════════════════════
# الجزء 4 — الذاكرة السلوكية
# ═══════════════════════════════════════════════════════════════

class BehavioralMemory:
    """
    تحفظ سجل الأحداث لكل جهاز (مفتاح الربط = MAC).
    تستخدم SQLite — يبقى على القرص حتى بعد إعادة التشغيل.

    الجداول:
      events    ← كل حدث جدار حماية
      baselines ← المعدل الطبيعي اليومي لكل جهاز
    """

    WINDOWS = {
        "short":  60,
        "medium": 300,
        "long":   3600
    }

    def __init__(self, db_path: str = r"C:\FS-File\risk_memory.db"):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()

    def _init_tables(self):
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS events (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                mac       TEXT    NOT NULL,
                operation TEXT,
                program   TEXT,
                port      TEXT,
                timestamp REAL,
                score     REAL
            );
            CREATE TABLE IF NOT EXISTS baselines (
                mac               TEXT PRIMARY KEY,
                avg_daily_changes REAL DEFAULT 0,
                last_updated      REAL
            );
        """)
        self.db.commit()

    def record_event(self, mac: str, operation: str,
                     program: str, port: str, score: float):
        """يسجل كل حدث في قاعدة البيانات."""
        self.db.execute(
            "INSERT INTO events VALUES (NULL,?,?,?,?,?,?)",
            (mac, operation, program, str(port), time.time(), score)
        )
        self.db.commit()

    def get_frequency_score(self, mac: str,
                             window: str = "medium") -> int:
        """
        كم تغيير حدث في النافذة الزمنية؟

        0        → 0 نقطة
        1-2      → 10
        3-5      → 30
        6-10     → 55
        11-20    → 75
        فوق 20   → 90 (هجوم آلي على الأرجح)
        """
        cutoff = time.time() - self.WINDOWS[window]
        cursor = self.db.execute(
            "SELECT COUNT(*) FROM events WHERE mac=? AND timestamp>?",
            (mac, cutoff)
        )
        count = cursor.fetchone()[0]

        thresholds = [(20, 90), (10, 75), (5, 55), (2, 30), (0, 10)]
        for limit, score in thresholds:
            if count > limit:
                return score
        return 0

    def get_anomaly_score(self, mac: str,
                           current_today: int) -> int:
        """
        هل عدد التغييرات اليوم أعلى من المعتاد لهذا الجهاز؟

        انحراف ≤20%  → 0
        انحراف ≤50%  → 15
        انحراف ≤100% → 35
        انحراف ≤200% → 55
        فوق 200%     → 75
        """
        cursor = self.db.execute(
            "SELECT avg_daily_changes FROM baselines WHERE mac=?",
            (mac,)
        )
        row = cursor.fetchone()

        if not row or row[0] == 0:
            return 20  # لا خط أساس بعد = خطر معتدل افتراضي

        baseline  = row[0]
        deviation = (current_today - baseline) / baseline

        if deviation <= 0.2:  return 0
        if deviation <= 0.5:  return 15
        if deviation <= 1.0:  return 35
        if deviation <= 2.0:  return 55
        return 75

    def update_baseline(self, mac: str):
        """
        يُحدّث المعدل الطبيعي اليومي للجهاز.
        استخدم متوسطاً متحركاً (80% قديم + 20% جديد)
        لتجنب تأثير يوم شاذ واحد.
        يُستدعى من خيط مجدول كل 24 ساعة.
        """
        count = self.get_today_count(mac)
        cursor = self.db.execute(
            "SELECT avg_daily_changes FROM baselines WHERE mac=?",
            (mac,)
        )
        row = cursor.fetchone()

        new_avg = (row[0] * 0.8 + count * 0.2) if row else float(count)

        self.db.execute(
            "INSERT OR REPLACE INTO baselines VALUES (?,?,?)",
            (mac, new_avg, time.time())
        )
        self.db.commit()

    def apply_decay(self, score: float, mac: str) -> float:
        """
        الخطر يتراجع تلقائياً إذا هدأ الجهاز.
        كل 10 دقائق هدوء = 5% تراجع.
        الحد الأدنى 10% — السجل التاريخي لا يمحى.
        """
        cursor = self.db.execute(
            "SELECT timestamp FROM events "
            "WHERE mac=? ORDER BY timestamp DESC LIMIT 1",
            (mac,)
        )
        row = cursor.fetchone()
        if not row:
            return score

        elapsed       = time.time() - row[0]
        decay_periods = elapsed / 600
        decay_factor  = max(0.1, 1.0 - (0.05 * decay_periods))
        return round(score * decay_factor, 2)

    def get_today_count(self, mac: str) -> int:
        cursor = self.db.execute(
            "SELECT COUNT(*) FROM events "
            "WHERE mac=? AND timestamp>?",
            (mac, time.time() - 86400)
        )
        return cursor.fetchone()[0]

    def analyze_program_behavior(self, mac: str,
                                  program_path: str) -> int:
        """
        هل رأينا هذا البرنامج يعدّل الجدار من قبل؟
        برنامج جديد لأول مرة = أكثر خطورة.
        """
        cursor = self.db.execute(
            "SELECT COUNT(*) FROM events "
            "WHERE mac=? AND program=? AND timestamp>?",
            (mac, program_path, time.time() - 604800)  # 7 أيام
        )
        count = cursor.fetchone()[0]

        if count == 0:  return 25  # لأول مرة
        if count <= 5:  return 10  # نادر
        return 0                   # برنامج معتاد


# ═══════════════════════════════════════════════════════════════
# الجزء 5 — محرك ربط الأحداث
# ═══════════════════════════════════════════════════════════════

class CorrelationEngine:
    """
    يكشف أنماط الهجوم المركبة.
    كل نمط = سيناريو هجومي موثّق.
    """

    ATTACK_PATTERNS = {

        "smb_external_exposure": {
            "check": lambda op, port, action, ip, direction: (
                str(port) in ["445", "139", "135"] and
                ip in ["Any", "Public IP"]
            ),
            "bonus": 45,
            "label": "SMB External Exposure"
        },

        "rdp_public_exposure": {
            "check": lambda op, port, action, ip, direction: (
                str(port) == "3389" and
                action == "Allow" and
                ip in ["Any", "Public IP"] and
                direction == "Inbound"
            ),
            "bonus": 40,
            "label": "RDP Public Exposure"
        },

        "reverse_shell_indicator": {
            "check": lambda op, port, action, ip, direction: (
                str(port) in ["4444", "1337", "31337", "9001", "8888"] and
                action == "Allow" and
                direction == "Outbound"
            ),
            "bonus": 60,
            "label": "Reverse Shell Indicator"
        },

        "security_rule_removal": {
            "check": lambda op, port, action, ip, direction: (
                op == "DELETE" and action == "Block"
            ),
            "bonus": 35,
            "label": "Security Rule Removal"
        },

        "block_to_allow_flip": {
            "check": lambda op, port, action, ip, direction: (
                op == "MODIFY" and
                action == "Allow" and
                ip in ["Any", "Public IP"]
            ),
            "bonus": 30,
            "label": "Block-to-Allow Flip"
        },

        "database_external": {
            "check": lambda op, port, action, ip, direction: (
                str(port) in ["1433", "3306", "5432", "27017"] and
                ip in ["Any", "Public IP"] and
                direction == "Inbound"
            ),
            "bonus": 50,
            "label": "Database External Exposure"
        },

        "wildcard_inbound": {
            "check": lambda op, port, action, ip, direction: (
                str(port) == "Any" and
                action == "Allow" and
                direction == "Inbound" and
                ip in ["Any", "Public IP"]
            ),
            "bonus": 55,
            "label": "Wildcard Inbound Rule"
        }
    }

    def evaluate(self, operation: str, port: str, action: str,
                 ip_scope: str, direction: str) -> Tuple[int, list]:

        total_bonus = 0
        triggered   = []

        for name, pattern in self.ATTACK_PATTERNS.items():
            try:
                if pattern["check"](operation, str(port),
                                    action, ip_scope, direction):
                    total_bonus += pattern["bonus"]
                    triggered.append(pattern["label"])
            except Exception:
                continue

        return total_bonus, triggered


# ═══════════════════════════════════════════════════════════════
# الجزء 6 — النظام المركزي
# ═══════════════════════════════════════════════════════════════

class AdvancedRiskEngine:
    """
    يجمع الطبقات الخمس في نتيجة واحدة.

    الاستخدام في AOF.py:
        engine = AdvancedRiskEngine()   # مرة واحدة عند البدء
        result = engine.calculate(...)
        ricor  = result["score"]
    """

    def __init__(self, db_path: str = r"C:\FS-File\risk_memory.db"):
        self.memory     = BehavioralMemory(db_path)
        self.correlator = CorrelationEngine()

    def calculate(self,
              operation:    str,
              mac:          str,
              signature:    str,
              action:       str,
              direction:    str,
              protocol:     str,
              port:         str,
              ip_scope:     str,
              user_role:    str,
              timestamp:    float,
              program_path: str,
              work_start:   int  = 8,
              work_end:     int  = 18,
              work_days:    list = None) -> dict:
        """
        المعاملات:
          operation    : ADD / DELETE / MODIFY
          mac          : عنوان MAC للجهاز (AA-BB-CC-DD-EE-FF)
          signature    : Valid / NotSigned / HashMismatch / ...
          action       : Allow / Block
          direction    : Inbound / Outbound
          protocol     : TCP / UDP / Any / ICMP
          port         : رقم المنفذ أو "Any"
          ip_scope     : Any / Public IP / Local Network / ...
          user_role    : SYSTEM / ADMIN / USER / UNKNOWN
          timestamp    : time.time()
          program_path : المسار الكامل للبرنامج المُعدِّل

        الإرجاع: dict يحتوي على:
          score              : 0.0 – 100.0
          risk_level         : LOW / MEDIUM / HIGH / CRITICAL
          confidence         : 0 – 100
          context_multiplier : المضاعف المُطبَّق
          triggered_patterns : قائمة الأنماط التي اكتُشفت
          breakdown          : تفاصيل كل طبقة
        """

        # ── طبقة 1: الأوزان الأساسية
        base = calculate_base_score(
            operation, signature, action,
            direction, protocol, str(port), ip_scope
        )

        # ── طبقة 2: مضاعف السياق
        ctx_mult = get_context_multiplier(
            user_role, timestamp,
            work_start = work_start,
            work_end   = work_end,
            work_days  = work_days
        )
        score    = base * ctx_mult

        # ── طبقة 3: الذاكرة السلوكية
        freq_score    = self.memory.get_frequency_score(mac, "medium")
        today_count   = self.memory.get_today_count(mac)
        anomaly_score = self.memory.get_anomaly_score(mac, today_count)
        prog_score    = self.memory.analyze_program_behavior(
                            mac, program_path)
        score += freq_score + anomaly_score + prog_score

        # ── طبقة 4: ربط الأحداث
        corr_bonus, triggered = self.correlator.evaluate(
            operation, str(port), action, ip_scope, direction
        )
        score += corr_bonus

        # ── تطبيع (0–100)
        normalized = min(100.0, max(0.0, round((score / 350) * 100, 1)))

        # ── تراجع الخطر بمرور الوقت
        normalized = self.memory.apply_decay(normalized, mac)

        # ── Confidence
        confidence = self._confidence(signature, user_role, triggered)

        # ── تصنيف المستوى
        risk_level = self._classify(normalized)

        # ── تسجيل الحدث
        self.memory.record_event(
            mac, operation, program_path, str(port), normalized
        )

        return {
            "score":               normalized,
            "risk_level":          risk_level,
            "confidence":          confidence,
            "context_multiplier":  ctx_mult,
            "triggered_patterns":  triggered,
            "breakdown": {
                "base_raw":        round(base, 1),
                "after_context":   round(base * ctx_mult, 1),
                "frequency":       freq_score,
                "anomaly":         anomaly_score,
                "program_new":     prog_score,
                "correlation":     corr_bonus
            }
        }

    def _confidence(self, signature: str,
                    role: str, patterns: list) -> int:
        base = 50
        sig_map = {
            "Valid":         +30,
            "NotSigned":     +20,
            "HashMismatch":  +25,
            "Revoked":       +20,
            "UntrustedRoot": +20,
        }
        base += sig_map.get(signature.strip(), 0)
        if role.upper() == "UNKNOWN":
            base -= 20
        base += min(25, len(patterns) * 8)
        return min(100, max(0, base))

    def _classify(self, score: float) -> str:
        if score < 20:  return "LOW"
        if score < 45:  return "MEDIUM"
        if score < 70:  return "HIGH"
        return "CRITICAL"


# ═══════════════════════════════════════════════════════════════
# الجزء 7 — مجدول تحديث الخط الأساس
# ═══════════════════════════════════════════════════════════════

def start_baseline_updater(engine: AdvancedRiskEngine):
    """
    خيط في الخلفية يحدّث المعدل الطبيعي كل 24 ساعة.
    استدعه مرة واحدة في بداية AOF.py.
    """
    import threading
# اسئل عن الداله دي هل اللابت توب ح يكون شغال 24 ساعه ولا لا ؟
    def _updater():
        while True:
            time.sleep(86400)
            try:
                cursor = engine.memory.db.execute(
                    "SELECT DISTINCT mac FROM events"
                )
                for (mac,) in cursor.fetchall():
                    engine.memory.update_baseline(mac)
            except Exception:
                pass

    t = threading.Thread(target=_updater, daemon=True)
    t.start()
