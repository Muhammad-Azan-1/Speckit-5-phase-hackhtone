# ☸️ Kubernetes Operations Guide (Full Flow)

This guide covers everything you need to know to **Start, Run, Stop, and Manage** your Todo App on Kubernetes locally using Minikube.

---

## 🚀 1. How to START (Beginning of Day)

When you turn on your computer and want to start working:

### Step 1: Start Minikube
This starts your local Kubernetes cluster.
```bash
minikube start
```
*Wait until you see "Done! kubectl is now configured..."*

### Step 2: Check Status
Verify everything is running correctly.
```bash
kubectl get nodes
# Should show: minikube   Ready   control-plane
```

### Step 3: Check Your Pods
See if your app is already running from last time.
```bash
kubectl get pods
```
*If you see pods running, jump to **Section 4: How to ACCESS**.*

---

## 🏗️ 2. How to DEPLOY (If Fresh or Changed Code)

If you have **changed code** or this is a **fresh start** (pods not running):

### Step 1: Connect Docker to Minikube
**CRITICAL STEP**: This tells your terminal to use Minikube's internal Docker, not your desktop's.
```bash
eval $(minikube -p minikube docker-env)
```

### Step 2: Build Images
Build your latest code into images.
```bash
# Build Backend
docker build -t todo-backend:latest -f backend-app/Dockerfile backend-app/

# Build Frontend
docker build -t todo-frontend:latest -f frontend/Dockerfile frontend/
```

### Step 3: Deploy with Helm
Tell Kubernetes to launch your app using these images.
```bash
# First time install
helm install todo-chatbot k8s/helm/todo-chatbot

# OR Update existing deployment (if you changed code)
helm upgrade todo-chatbot k8s/helm/todo-chatbot
```

---

## 🌐 3. How to ACCESS (Use the App)

Once pods are running (`kubectl get pods` shows "Running"), you need to open connections to them.

**Open 3 separate terminal tabs/windows:**

### Tab 1: Access Frontend (Website)
```bash
kubectl port-forward svc/todo-chatbot-frontend 3000:3000
```
👉 Open Browser: [http://localhost:3000](http://localhost:3000)

### Tab 2: Access Backend (API)
```bash
kubectl port-forward svc/todo-chatbot-backend 8000:8000
```
👉 Check Health: `curl http://localhost:8000/health`

### Tab 3: Access MCP Server (AI Tools)
```bash
kubectl port-forward svc/todo-chatbot-mcp-server 8808:8808
```

---

## � 4. How to STOP (End of Day)

When you are done working and want to verify resources:

### Option A: Pause (Recommended)
Stops the cluster but keeps all your deployments and data ready for next time.
```bash
minikube stop
```

### Option B: Delete (Clean Slate)
**WARNING**: Deletes everything inside Kubernetes (Deployments, Database data, etc.). Use only if things are broken.
```bash
minikube delete
```

---

## 🔧 5. Troubleshooting (Fixing Issues)

### Issue: "Connection refused" or "Unable to connect"
**Cause**: Minikube is stopped or paused.
**Fix**:
```bash
minikube start
```

### Issue: "ImagePullBackOff" or "ErrImagePull"
**Cause**: Kubernetes can't find your Docker image.
**Fix**:
1. Run `eval $(minikube -p minikube docker-env)`
2. Rebuild images (See Section 2, Step 2)
3. Restart pod: `kubectl delete pod <pod-name>`

### Issue: "Changes not showing up"
**Cause**: You changed code but didn't rebuild/redeploy.
**Fix**:
1. Rebuild Docker images (Section 2, Step 2)
2. Run `kubectl rollout restart deployment todo-chatbot-frontend` (or backend)

### Issue: "Minikube stuck" or "weird errors"
**Fix**: The nuclear option.
```bash
minikube delete
minikube start
# Then follow Section 2 (Build & Deploy) again
```
