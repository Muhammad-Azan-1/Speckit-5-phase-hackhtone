# 🚀 Kubernetes Deployment Guide - Phase IV

## 📚 Kubernetes Kya Hai? (Simple Concept)

Sochiye aapke paas ek application hai.

*   **Docker Container**: Yeh ek "Dukan" (Shop) hai jisme aapka sara saaman (code) packed hai.
*   **Hugging Face / Vercel**: Yeh ek "Managed Mall" hai. Aap bas apni dukan wahan rakhte hain, baaki bijli, paani, security (servers, scaling) woh khud sambhalte hain. Easy hai par control kam hai.
*   **Kubernetes (K8s)**: Yeh aapka "Apna Shopping Plaza" hai. Yahan aap zameen (servers) khud manage karte hain, decide karte hain konsi dukan kahan hogi, kitni dukanen hongi, aur raste (networking) kaise honge. Yeh professional production level hai jahan aapko full control milta hai.

**Is Phase IV mein humne kya kiya?**
Humne apni app jo pehle "Mall" (Hugging Face) mein thi, usse utha kar apne "Plaza" (Kubernetes Minikube) mein successfully shift kiya hai.

---

## 🏗️ Architecture: Hamare Cluster Mein Kya Chal Raha Hai?

Abhi aapke local computer (Minikube) par 3 services chal rahi hain jo ek dusre se baat kar sakti hain:

1.  **Backend API (FastAPI)**: Port `8000`. Database se connect karta hai aur logic chalata hai.
2.  **Frontend UI (Next.js)**: Port `3000`. User ko website dikhata hai.
3.  **MCP Server (AI Tools)**: Port `8808`. AI Agents ke liye tools provide karta hai.

Or Database (Neon PostgreSQL) abhi bhi bahar cloud par hai, jisse hamara backend connect kar raha hai.

---

## ✅ Hamne Kya Kaam Kiya?

1.  **Dockerization**: Frontend aur Backend ki optimized Docker images banayi. Specifically Frontend ke liye `production` build use ki taaki architecture issues solve hon.
2.  **Helm Charts**: Kubernetes ko batane ke liye "nakshe" (maps/templates) banaye ki konsi cheez kaise chalani hai (Ram, CPU, Ports).
3.  **Fixing Issues**: 
    *   Backend ka port `7860` se `8000` set kiya.
    *   MCP Server ki command `uv run python` set ki.
    *   Frontend ki build issues resolve kiye.

---

## 🚀 App Kaise Run Karein (Step-by-Step)

Apne terminal mein ye commands chalayen:

### 1. Status Check Karein
Dekhein ki kya sab kuch chal raha hai:
```bash
kubectl get pods
```
*Output mein sabhi pods ke aage `1/1 Running` hona chahiye.*

### 2. Frontend (Website) Chalayen
Apne browser mein website dekhne ke liye port-forwarding karein:
```bash
kubectl port-forward svc/todo-chatbot-frontend 3000:3000
```
👉 Ab browser mein kholein: **[http://localhost:3000]**

### 3. Backend (API) Test Karein
Dusre terminal mein backend connect karein:
```bash
kubectl port-forward svc/todo-chatbot-backend 8000:8000
```
👉 Health check test karein:
```bash
curl http://localhost:8000/health
```

### 4. MCP Server Access Karein (Optional)
Agar AI agent tools test karne hain:
```bash
kubectl port-forward svc/todo-chatbot-mcp-server 8808:8808
```

---

## 🛠️ Useful Commands (Cheat Sheet)

| Maqsad (Goal) | Command |
|---------------|---------|
| **Sab kuch dekhna** | `kubectl get all` |
| **Logs check karna** (Agar kuch error aye) | `kubectl logs -l app=backend` (ya `frontend`) |
| **Pod restart karna** | `kubectl delete pod <pod-name>` (Khud wapis aa jayega) |
| **Cluster band karna** | `minikube stop` |
| **Cluster start karna** | `minikube start` |

---

## 🎉 Conclusion
Mubarak ho! Aapne successfully ek **Cloud-Native Architecture** khada kar diya hai. Jo companies production mein AWS/Google Cloud par karti hain, wahi setup aapne local Minikube par kar liya hai.
