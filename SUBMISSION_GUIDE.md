# 📦 Hackathon Submission Guide

## Repository Structure

This repository contains submissions for **3 phases** of the hackathon:

```
Speckit-5-phase-hackhtone/
├── Phase2/              # Phase II Submission
├── Phase3/              # Phase III Submission  
└── Todo-App-All-Phases/ # Phase IV Submission (Kubernetes)
```

---

## 📋 Phase-wise Submission Mapping

### Phase II: Full-Stack Web Application
**📁 Submit Folder**: `Phase2/`

**Deliverables**:
- ✅ Frontend (Next.js)
- ✅ Backend API (FastAPI + SQLModel)
- ✅ CRUD Operations
- ✅ JWT Authentication
- ✅ Persistent SQLite Database

**Run Instructions**: See [Phase2/README.md](Phase2/README.md)

---

### Phase III: AI Chatbot Integration
**📁 Submit Folder**: `Phase3/`

**Deliverables**:
- ✅ Phase II features (all cumulative)
- ✅ AI Chatbot Interface
- ✅ MCP Server Implementation
- ✅ Google Agents SDK Integration
- ✅ Task Management via AI

**Run Instructions**: See [Phase3/README.md](Phase3/README.md)

---

### Phase IV: Kubernetes Deployment
**📁 Submit Folder**: `Todo-App-All-Phases/`

**Deliverables**:
- ✅ Phase III features (all cumulative)
- ✅ Docker Containerization
- ✅ Kubernetes Manifests
- ✅ Helm Charts
- ✅ Minikube Deployment (Tested & Working)

**Run Instructions**: See [Todo-App-All-Phases/KUBERNETES_GUIDE.md](Todo-App-All-Phases/KUBERNETES_GUIDE.md)

**Why Todo-App-All-Phases**:
- Contains the **proven, tested Kubernetes deployment**
- All Docker images build successfully
- Helm charts validated
- Pods running in production

---

## ✅ Verification Checklist

### Phase II (`Phase2/`)
- [ ] Frontend runs on `http://localhost:3000`
- [ ] Backend runs on `http://localhost:8000`
- [ ] User can register, login, create todos
- [ ] Database persists data

### Phase III (`Phase3/`)
- [ ] All Phase II features work
- [ ] Chat interface accessible at `/chat`
- [ ] AI can list, create, update tasks
- [ ] MCP server responds on port 8808

### Phase IV (`Todo-App-All-Phases/`)
- [ ] `kubectl get pods` shows all pods running
- [ ] Frontend accessible via port-forward
- [ ] Backend API responds via port-forward
- [ ] Database persists in Kubernetes volumes

---

## 🚀 Quick Start

```bash
# Phase II
cd Phase2/backend-app && uv run uvicorn main:app --reload
cd Phase2/frontend && npm run dev

# Phase III  
cd Phase3/backend-app && uv run uvicorn main:app --reload
cd Phase3/frontend && npm run dev

# Phase IV
cd Todo-App-All-Phases
minikube start
# Follow KUBERNETES_GUIDE.md for full deployment
```

---

## 📝 Notes

- **Phase2** and **Phase3** are standalone submission folders
- **Phase4** uses `Todo-App-All-Phases` as it contains the working K8s deployment
- All phases include comprehensive README files
- Environment variables are documented in respective folders




<!-- 

> /specs  I have completed phase4 of my hackhtone you cawn view the constituion.md and other files to understand all the
  implmentation now wee need to work on phase5 you can also view the hackhtone document at @"Hackathon II - Todo Spec-Driven
  Development.md"
  I want you to please undertand the hackhtone phase 5 requirments then start writing the specs to work on phase5

  ultrathink -->