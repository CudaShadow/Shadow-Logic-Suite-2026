# ==========================================
# Shadow Logic Suite 2026
# Offline Neuro-Symbolic Framework
# Modules: MiniAI | VideoAuditor | LogicLoop | PrivacyAuditor | LogicSanitizer
# CPU Lawas Friendly, Offline-First, Low Resource
# ==========================================

import random
import hashlib
import pickle
import time
import numpy as np

# ==========================================
# MODULE 1: MINI AI NEURO-SYMBOLIC
# ==========================================
class MiniAI:
    def __init__(self):
        self.knowledge = {
            "hai": ["Halo!", "Hai juga!"],
            "apa kabar": ["Baik!", "Sehat selalu!", "Lumayan lah."],
            "siapa kamu": ["Saya MiniAI, teman CPU lawasmu!"],
            "terima kasih": ["Sama-sama!", "Dengan senang hati!"],
            "cuaca": ["Maaf, saya belum bisa membaca cuaca, tapi semoga cerah!"]
        }
        self.memory_file = "mini_ai_memory.pkl"
        self.memory = self.load_memory()
        self.last_topic = None
        self.word_list = list(self.knowledge.keys())
        self.word_to_index = {w:i for i,w in enumerate(self.word_list)}
        self.input_dim = len(self.word_list)
        self.hidden_dim = 4
        self.W1 = np.random.randn(self.input_dim, self.hidden_dim) * 0.1
        self.b1 = np.zeros(self.hidden_dim)
        self.W2 = np.random.randn(self.hidden_dim, 1) * 0.1
        self.b2 = np.zeros(1)
        self.response_options = [
            "Hmm… saya kurang paham, coba jelaskan lagi.",
            "Menarik, teruskan ceritanya!",
            "Saya rasa itu penting, tapi saya mini AI, jadi sederhana jawabannya."
        ]

    # --- Memory ---
    def load_memory(self):
        try:
            with open(self.memory_file, "rb") as f:
                return pickle.load(f)
        except:
            return {}

    def save_memory(self):
        with open(self.memory_file, "wb") as f:
            pickle.dump(self.memory, f)

    # --- Helper ---
    def levenshtein(self,a,b):
        n,m=len(a),len(b)
        if n>m: a,b,b,n = b,a,n,m
        current = list(range(n+1))
        for i in range(1,m+1):
            previous, current = current, [i]+[0]*n
            for j in range(1,n+1):
                add,delete=previous[j]+1,current[j-1]+1
                change=previous[j-1]+(a[j-1]!=b[i-1])
                current[j]=min(add,delete,change)
        return current[n]

    def closest_word(self,word,word_list,max_distance=2):
        min_dist = max_distance+1
        closest = None
        for w in word_list:
            dist = self.levenshtein(word,w)
            if dist<min_dist:
                min_dist = dist
                closest=w
        return closest

    def encode_text(self,text):
        vec = np.zeros(self.input_dim)
        for w in text.split():
            closest = self.closest_word(w,self.word_list)
            if closest: vec[self.word_to_index[closest]]=1
        return vec

    def nn_predict(self,text):
        x=self.encode_text(text)
        h=1/(1+np.exp(-np.dot(x,self.W1)-self.b1))
        y=1/(1+np.dot(h,self.W2)+self.b2)
        index=int(y[0]*len(self.response_options))
        if index>=len(self.response_options): index=len(self.response_options)-1
        return self.response_options[index]

    # --- Core ---
    def respond(self,text):
        text_original=text.lower().strip()
        words = text_original.split()
        corrected_words=[]
        for w in words:
            closest=self.closest_word(w,self.word_list)
            corrected_words.append(closest if closest else w)
        corrected_text=" ".join(corrected_words)

        for key in self.knowledge:
            if key in corrected_text:
                response=random.choice(self.knowledge[key])
                self.last_topic=key
                self.memory[corrected_text]=response
                self.save_memory()
                return response

        if "siapa" in words and "dia" in words:
            if self.last_topic:
                resp=f"Saya kira kamu bertanya tentang {self.last_topic}."
                self.memory[corrected_text]=resp
                self.save_memory()
                return resp
            else:
                return "Siapa yang kamu maksud?"

        fallback=self.nn_predict(corrected_text)
        self.memory[corrected_text]=fallback
        self.save_memory()
        return fallback

# ==========================================
# MODULE 2: VIDEO TEMPORAL AUDITOR
# ==========================================
class VideoTemporalAuditor:
    def __init__(self):
        self.last_hash=None
        self.last_time=None
        self.anomalies=[]

    def frame_hash(self,frame_bytes):
        return hashlib.md5(frame_bytes).hexdigest()

    def ingest_frame(self,frame_bytes,timestamp):
        h=self.frame_hash(frame_bytes)
        if self.last_hash:
            if h==self.last_hash:
                self.anomalies.append("Duplicate frame detected")
            dt=timestamp-self.last_time
            if dt<0.01:
                self.anomalies.append("Suspicious ultra-short frame")
        self.last_hash=h
        self.last_time=timestamp

    def report(self):
        return {"status":"OK" if not self.anomalies else "ANOMALY","findings":self.anomalies}

# ==========================================
# MODULE 3: LOGIC LOOP SIMULATOR
# ==========================================
class LogicLoopSimulator:
    def __init__(self):
        self.context=None
    def next_action(self,stimulus):
        if stimulus==self.context: delay=random.uniform(1.2,2.8); action="hesitate"
        else: delay=random.uniform(0.4,1.6); action="decide"
        self.context=stimulus
        time.sleep(delay)
        return action,round(delay,2)

# ==========================================
# MODULE 4: PRIVACY SHADOW AUDITOR
# ==========================================
class PrivacyShadowAuditor:
    def __init__(self):
        self.events=[]
    def log_event(self,source,data_type,intent):
        self.events.append({"source":source,"data":data_type,"intent":intent})
    def score(self):
        risk=0
        for e in self.events:
            if e["data"]=="metadata" and e["intent"]=="unknown": risk+=2
            if e["source"]=="background" and e["intent"]=="analytics": risk+=1
        return {"privacy_score":max(0,10-risk),
                "risk_level":"LOW" if risk<3 else "MEDIUM" if risk<6 else "HIGH"}

# ==========================================
# MODULE 5: LOGIC PATH SANITIZER
# ==========================================
class LogicSanitizer:
    def __init__(self,app_name,declared_intent):
        self.app_name=app_name
        self.declared_intent=declared_intent
        self.violation_log=[]
    def audit_syscall(self,action,target):
        logic_gate={
            "FLASHLIGHT":["CAMERA_FLASH","POWER_MGMT"],
            "CALCULATOR":["MATH_PROC","DISPLAY"],
            "SYSTEM_UPDATE":["NETWORK","STORAGE","CPU_USAGE"]
        }
        allowed_actions=logic_gate.get(self.declared_intent,[])
        if action not in allowed_actions:
            msg=f"LOGIC_VIOLATION: {self.app_name} ({self.declared_intent}) mencoba {action} pada {target}"
            self.violation_log.append(msg)
            return False,msg
        return True,"Action Allowed"

# ==========================================
# DEMO OFFLINE
# ==========================================
if __name__=="__main__":
    print("=== Shadow Logic Suite 2026 Demo ===\n")

    # MiniAI Demo
    ai = MiniAI()
    print("MiniAI Response:", ai.respond("hai"))
    print("MiniAI Response:", ai.respond("siapa dia?"))

    # Video Auditor Demo
    video = VideoTemporalAuditor()
    video.ingest_frame(b"frame1",time.time())
    video.ingest_frame(b"frame1",time.time()+0.005)
    print("Video Auditor:", video.report())

    # Logic Loop Demo
    logic = LogicLoopSimulator()
    print("Logic Loop:", logic.next_action("menu_click"))
    print("Logic Loop:", logic.next_action("menu_click"))

    # Privacy Audit Demo
    privacy = PrivacyShadowAuditor()
    privacy.log_event("background","metadata","unknown")
    privacy.log_event("foreground","user_input","expected")
    print("Privacy Audit:", privacy.score())

    # Logic Path Sanitizer Demo
    sanitizer = LogicSanitizer("Flashlight_Pro","FLASHLIGHT")
    print(sanitizer.audit_syscall("CAMERA_FLASH","Hardware"))
    success,msg=sanitizer.audit_syscall("READ_CONTACTS","Database")
    if not success: print(f"⚠️ Warning: {msg}")
