BASE_WEIGHTS = {
    "operation": {
        "ADD":    {"base": 30, "reason": "إضافة قاعدة = تغيير سطح الهجوم"},
        "DELETE": {"base": 40, "reason": "حذف قاعدة = إزالة حماية"},
        "MODIFY": {"base": 35, "reason": "تعديل = إعادة توجيه سلوك"}
    },
    "signature": {
        "Valid":        -40,
        "NotSigned":    +50,
        "UntrustedRoot":+60,
        "HashMismatch": +80,  # أخطر حالة — تلاعب في الملف
        "Revoked":      +70,
        "NotTrusted":   +35,
        "UnknownError": +20,
        "Expired":      +25
    },
    "direction": {
        "Inbound":  +35,
        "Outbound": +20
    },
    "action": {
        "Allow": +25,
        "Block": +10   # حذف Block = خطر أكبر من إضافة Allow
    },
    "protocol": {
        "Any":  +30,
        "TCP":  +15,
        "UDP":  +20,
        "ICMP": +10
    },
    "ip_scope": {
        "Any":          +35,
        "Public IP":    +40,
        "Trusted IP":   +10,
        "Local Network":+5,
        "Localhost":    -30
    }
}

# المنافذ مصنفة حسب الخطورة
PORT_RISK = {
    "critical":  {"ports": ["3389","445","23","4444","5900"], "score": +50},
    "high":      {"ports": ["22","21","135","139","1433","5985","5986"], "score": +40},
    "medium":    {"ports": ["80","443","8080","8443","3306","5432"], "score": +15},
    "low":       {"ports": ["53","123","67","68"], "score": +5},
    "Any":       {"ports": ["Any"], "score": +30}
}



import datetime

def get_context_multiplier(user_role, timestamp):
    multiplier = 1.0
    
    hour = datetime.datetime.fromtimestamp(timestamp).hour
    weekday = datetime.datetime.fromtimestamp(timestamp).weekday()
    
    # وقت العمل: 8 صباح - 6 مساء، أيام الأسبوع
    is_working_hours = (8 <= hour <= 18) and (weekday < 5)
    
    if not is_working_hours:
        multiplier *= 1.8   # خارج وقت العمل = مضاعف خطر
    
    if weekday >= 5:
        multiplier *= 1.5   # عطلة نهاية الأسبوع
    
    # منتصف الليل - 5 صباح: أخطر فترة
    if 0 <= hour <= 5:
        multiplier *= 2.2
    
    # صلاحيات المستخدم
    role_multipliers = {
        "SYSTEM":    0.6,   # عمليات النظام متوقعة
        "ADMIN":     0.8,   # مشروع لكن يُراقَب
        "USER":      1.5,   # مستخدم عادي يعدل الجدار؟ خطر
        "UNKNOWN":   2.5    # مجهول الهوية = أعلى خطر
    }
    multiplier *= role_multipliers.get(user_role, 2.5)
    
    return round(multiplier, 2)


# يُخزَّن في SQLite — يناسب بنيتك الحالية
import sqlite3
import time

class BehavioralMemory:
    
    WINDOWS = {
        "short":  60,    # دقيقة
        "medium": 300,   # 5 دقائق
        "long":   3600   # ساعة
    }
    
    def __init__(self, db_path="C:\\FS-File\\risk_memory.db"):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()
    
    def _init_tables(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mac TEXT,
                operation TEXT,
                program TEXT,
                port TEXT,
                timestamp REAL,
                score REAL
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS baselines (
                mac TEXT PRIMARY KEY,
                avg_daily_changes REAL,
                last_updated REAL
            )
        """)
        self.db.commit()
    
    def record_event(self, mac, operation, program, port, score):
        self.db.execute(
            "INSERT INTO events VALUES (NULL,?,?,?,?,?,?)",
            (mac, operation, program, port, time.time(), score)
        )
        self.db.commit()
    
    def get_frequency_score(self, mac, window="medium"):
        cutoff = time.time() - self.WINDOWS[window]
        cursor = self.db.execute(
            "SELECT COUNT(*) FROM events WHERE mac=? AND timestamp>?",
            (mac, cutoff)
        )
        count = cursor.fetchone()[0]
        
        # جدول تصاعدي — كل تغيير إضافي يرفع الخطر
        if count == 0: return 0
        if count <= 2:  return 10
        if count <= 5:  return 30
        if count <= 10: return 55
        if count <= 20: return 75
        return 90  # أكثر من 20 تغيير في 5 دقائق = هجوم تلقائي
    
    def get_anomaly_score(self, mac, current_changes_today):
        cursor = self.db.execute(
            "SELECT avg_daily_changes FROM baselines WHERE mac=?", (mac,)
        )
        row = cursor.fetchone()
        
        if not row or row[0] == 0:
            return 20  # لا خط أساس = خطر متوسط
        
        baseline = row[0]
        deviation = (current_changes_today - baseline) / baseline
        
        if deviation <= 0.2:   return 0    # ضمن الطبيعي
        if deviation <= 0.5:   return 15
        if deviation <= 1.0:   return 35
        if deviation <= 2.0:   return 55
        return 75  # أكثر من ضعف المعدل الطبيعي
    
    def update_baseline(self, mac):
        # يُحدَّث يومياً
        cursor = self.db.execute(
            """SELECT COUNT(*) FROM events 
               WHERE mac=? AND timestamp > ?""",
            (mac, time.time() - 86400)
        )
        count = cursor.fetchone()[0]
        self.db.execute(
            """INSERT OR REPLACE INTO baselines VALUES (?,?,?)""",
            (mac, count, time.time())
        )
        self.db.commit()
    
    def apply_decay(self, current_score, mac):
        # الخطر يتراجع بمرور الوقت إن لم تحدث أحداث جديدة
        cursor = self.db.execute(
            "SELECT timestamp FROM events WHERE mac=? ORDER BY timestamp DESC LIMIT 1",
            (mac,)
        )
        row = cursor.fetchone()
        if not row:
            return current_score
        
        elapsed = time.time() - row[0]  # ثواني منذ آخر حدث
        
        decay_rate = 0.05  # 5% تراجع كل 10 دقائق
        decay_periods = elapsed / 600
        decay_factor = max(0.1, 1.0 - (decay_rate * decay_periods))
        
        return round(current_score * decay_factor, 2)




class CorrelationEngine:
    """
    يكشف الأنماط المركبة التي لا تُكشف بالنقاط المنفردة.
    كل نمط = سيناريو هجومي حقيقي.
    """
    
    ATTACK_PATTERNS = {
        
        # سيناريو 1: فتح RDP + السماح من الخارج
        "rdp_exposure": {
            "conditions": lambda op, port, action, ip, direction: (
                port in ["3389"] and
                action == "Allow" and
                ip in ["Any", "Public IP"] and
                direction == "Inbound"
            ),
            "bonus": +40,
            "label": "RDP Exposure"
        },
        
        # سيناريو 2: حذف قاعدة أمنية + إضافة قاعدة سماح
        "security_bypass": {
            "conditions": lambda op, port, action, ip, direction: (
                op == "DELETE" and action == "Block"
            ),
            "bonus": +35,
            "label": "Security Rule Removal"
        },
        
        # سيناريو 3: SMB مفتوح للخارج (مثل WannaCry)
        "smb_external": {
            "conditions": lambda op, port, action, ip, direction: (
                port in ["445", "139", "135"] and
                ip in ["Any", "Public IP"]
            ),
            "bonus": +45,
            "label": "SMB External Exposure"
        },
        
        # سيناريو 4: تعديل بدون عملية Python معروفة
        "process_anomaly": {
            "conditions": lambda op, port, action, ip, direction: (
                op == "MODIFY" and ip == "Any"
            ),
            "bonus": +20,
            "label": "Unattributed Modification"
        },
        
        # سيناريو 5: Reverse Shell indicators
        "reverse_shell": {
            "conditions": lambda op, port, action, ip, direction: (
                port in ["4444", "1337", "31337", "9001"] and
                action == "Allow" and
                direction == "Outbound"
            ),
            "bonus": +60,
            "label": "Possible Reverse Shell"
        }
    }
    
    def evaluate(self, operation, port, action, ip_scope, direction):
        triggered = []
        total_bonus = 0
        
        for name, pattern in self.ATTACK_PATTERNS.items():
            try:
                if pattern["conditions"](operation, port, action, ip_scope, direction):
                    total_bonus += pattern["bonus"]
                    triggered.append(pattern["label"])
            except Exception:
                continue
        
        return total_bonus, triggered



class AdvancedRiskEngine:
    
    def __init__(self):
        self.memory = BehavioralMemory()
        self.correlator = CorrelationEngine()
    
    def _get_port_score(self, port):
        port = str(port)
        for category, data in PORT_RISK.items():
            if port in data["ports"] or (category == "Any" and port == "Any"):
                return data["score"]
        return 10  # منفذ غير مصنف = خطر افتراضي منخفض
    
    def calculate(self,
                  operation,        # ADD / DELETE / MODIFY
                  mac,              # معرف الجهاز
                  signature,        # Valid / NotSigned / ...
                  action,           # Allow / Block
                  direction,        # Inbound / Outbound
                  protocol,         # TCP / UDP / Any
                  port,             # رقم المنفذ أو Any
                  ip_scope,         # Any / Public IP / ...
                  user_role,        # ADMIN / USER / UNKNOWN
                  timestamp,        # Unix timestamp
                  program_path      # مسار البرنامج
                  ):
        
        # ── طبقة 1: الأوزان الأساسية
        score = 0
        score += BASE_WEIGHTS["operation"][operation]["base"]
        score += BASE_WEIGHTS["signature"].get(signature, +20)
        score += BASE_WEIGHTS["direction"][direction]
        score += BASE_WEIGHTS["action"][action]
        score += BASE_WEIGHTS["protocol"].get(protocol, +15)
        score += BASE_WEIGHTS["ip_scope"].get(ip_scope, +20)
        score += self._get_port_score(port)
        
        # ── طبقة 2: السياق الزمني والصلاحيات
        ctx_multiplier = get_context_multiplier(user_role, timestamp)
        score *= ctx_multiplier
        
        # ── طبقة 3: الذاكرة السلوكية
        freq_score    = self.memory.get_frequency_score(mac, "medium")
        anomaly_score = self.memory.get_anomaly_score(mac, 
                            self._get_today_count(mac))
        score += freq_score + anomaly_score
        
        # ── طبقة 4: ربط الأحداث
        correlation_bonus, triggered_patterns = self.correlator.evaluate(
            operation, port, action, ip_scope, direction
        )
        score += correlation_bonus
        
        # ── Confidence Score
        confidence = self._calculate_confidence(
            signature, user_role, triggered_patterns
        )
        
        # ── تطبيع النتيجة (0–100)
        normalized = min(100, max(0, round((score / 300) * 100, 1)))
        
        # ── تراجع الخطر بمرور الوقت
        normalized = self.memory.apply_decay(normalized, mac)
        
        # ── تصنيف مستوى الخطر
        risk_level = self._classify(normalized)
        
        # ── تسجيل الحدث
        self.memory.record_event(mac, operation, program_path, port, normalized)
        
        return {
            "score":            normalized,
            "risk_level":       risk_level,
            "confidence":       confidence,
            "context_multiplier": ctx_multiplier,
            "triggered_patterns": triggered_patterns,
            "components": {
                "base":        round(score - freq_score - anomaly_score - correlation_bonus, 1),
                "frequency":   freq_score,
                "anomaly":     anomaly_score,
                "correlation": correlation_bonus
            }
        }
    
    def _get_today_count(self, mac):
        cursor = self.memory.db.execute(
            "SELECT COUNT(*) FROM events WHERE mac=? AND timestamp>?",
            (mac, time.time() - 86400)
        )
        return cursor.fetchone()[0]
    
    def _calculate_confidence(self, signature, user_role, patterns):
        base = 50
        if signature == "Valid":    base += 25
        if signature == "NotSigned": base += 15
        if user_role == "UNKNOWN":  base -= 20
        if patterns:                base += 10 * len(patterns)
        return min(100, max(0, base))
    
    def _classify(self, score):
        if score < 20:  return "LOW"
        if score < 45:  return "MEDIUM"
        if score < 70:  return "HIGH"
        return "CRITICAL"




engine = AdvancedRiskEngine()  # يُنشأ مرة واحدة عند بدء البرنامج

result = engine.calculate(
    operation   = "ADD",
    mac         = "00:1A:2B:3C:4D:5E",
    signature   = "Signed",
    action      = "Block",
    direction   = "Outbound",
    protocol    = "TCP",
    port        = "8080",
    ip_scope    = "Localhost",
    user_role   = "SYSTEM",
    timestamp   = time.time(),
    program_path= r"D:\auto_py_to_exe\output\hack tool.exe"
)

ricor = result["score"]
print(ricor)
if result["risk_level"] == "CRITICAL":
    print("1")
elif result["risk_level"] == "HIGH":
    print("2")
elif result["risk_level"] == "MEDIUM":
    print("3")
else:
    print("4")

