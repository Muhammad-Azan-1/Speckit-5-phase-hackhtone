# Kubernetes Deployment Status

## Current State (2026-01-22)

### ✅ What's Working
- Minikube cluster is running
- Helm charts are created and valid (passes `helm lint`)
- MCP Server pod is **NOW RUNNING** on port 8808 ✅
- Images exist in Minikube's Docker registry

### ❌ What's Broken

#### 1. Backend Pod - CrashLoopBackOff
**Problem**: Running on port 8000 instead of 7860
- Health checks expect port 7860
- Container runs on port 8000
- **Root Cause**: Dockerfile CMD specifies `--port 7860` but something is overriding it

**Logs:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Shutting down
```

**Why it's crashing:**
- Kubernetes health probe checks `http://pod-ip:7860/health`
- App is actually running on port 8000
- Health check fails → Pod gets killed → Restart loop

#### 2. Frontend Pod - Architecture Issues
**Problem**: Next.js SWC binary mismatch
**Logs:**
```
⚠ Attempted to load @next/swc-linux-arm64-gnu, but it was not installed
```

**Status**: Running but may have performance issues

---

## Quick Fixes

### Fix 1: Backend Port Issue

**Option A - Change health probe to port 8000:**
Edit `k8s/helm/todo-chatbot/values.yaml`:
```yaml
backend:
  service:
    port: 8000  # Change from 7860 to 8000
```

**Option B - Force backend to use port 7860:**
Make sure PORT env var is set in deployment (already done) and fix Dockerfile

---

## What I've Done So Far

1. ✅ Fixed MCP server command: `python` → `uv run python`
2. ✅ Rebuilt backend Docker image with `--no-cache`
3. ✅ Upgraded Helm deployment (revision 2)
4. ✅ MCP Server now working!

---

## Next Steps

### Immediate (to get demo working):
1. **Change backend service port to 8000** in values.yaml
2. Upgrade Helm deployment
3. Test all 3 pods

### Proper Fix (for production):
1. Figure out why Dockerfile CMD `--port 7860` is being ignored
2. Rebuild images correctly
3. Fix frontend architecture issues

---

## Commands to Monitor

```bash
# Watch pods
kubectl get pods -w

# Check logs
kubectl logs <pod-name> --tail=50

# Describe pod for events
kubectl describe pod <pod-name>

# Upgrade Helm after fixes
helm upgrade todo-chatbot ./k8s/helm/todo-chatbot

# Restart deployments
kubectl rollout restart deployment/todo-chatbot-backend
kubectl rollout restart deployment/todo-chatbot-frontend
kubectl rollout restart deployment/todo-chatbot-mcp-server
```

---

## Architecture

```
┌─────────────────────────────────────────────┐
│          Minikube Cluster                   │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │  Frontend    │  │   Backend    │        │
│  │  Port 3000   │  │   Port ???? │        │
│  │  ❌ Issues   │  │   ❌ CRASHED │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
│  ┌──────────────┐                          │
│  │ MCP Server   │                          │
│  │  Port 8808   │                          │
│  │  ✅ WORKING  │                          │
│  └──────────────┘                          │
│                                             │
└─────────────────────────────────────────────┘
```
