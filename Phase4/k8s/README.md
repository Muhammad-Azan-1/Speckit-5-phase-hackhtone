# Kubernetes Deployment for Todo Chatbot

This directory contains the Kubernetes deployment configuration for the Todo Chatbot application using Helm charts.

## Overview

The Todo Chatbot application is deployed to Kubernetes with the following components:
- **Frontend**: Next.js application serving the UI
- **Backend**: FastAPI application providing REST API endpoints (runs on port 7860 to match Hugging Face requirements)
- **MCP Server**: Python-based server exposing task management tools for AI agents

## Prerequisites

- Kubernetes cluster (tested with Minikube)
- Helm 3.x
- kubectl

## Quick Start

### 1. Start Minikube (if using Minikube)

```bash
# Start Minikube with sufficient resources
minikube start --driver=docker --cpus=2 --memory=4g

# Enable ingress addon for external access
minikube addons enable ingress
```

### 2. Configure Docker Environment (for Minikube)

```bash
# Configure your shell to use Minikube's Docker daemon
eval $(minikube docker-env)
```

### 3. Build Docker Images

```bash
# Build frontend image
cd frontend
docker build -t todo-frontend:latest .

# Build backend image
cd ../backend-app
docker build -t todo-backend:latest .
```

### 4. Update Values

Edit the `values.yaml` file to include your actual database URL and auth secret:

```yaml
backend:
  env:
    DATABASE_URL: "your_actual_neon_db_url_here"
    BETTER_AUTH_SECRET: "your_actual_better_auth_secret_here"

database:
  url: "your_actual_neon_db_url_here"
```

### 5. Install the Helm Chart

```bash
# Navigate to the Helm chart directory
cd k8s/helm/todo-chatbot

# Install the chart
helm install todo-chatbot . --values values.yaml

# Or upgrade an existing installation
helm upgrade todo-chatbot . --values values.yaml --install
```

### 6. Access the Application

```bash
# Get the Minikube IP
minikube ip

# Add the domain to your hosts file
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Access the application at http://todo.local
```

## Configuration

The Helm chart is configured through the `values.yaml` file with the following main sections:

### Frontend Configuration
```yaml
frontend:
  enabled: true
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  replicaCount: 1
  service:
    type: ClusterIP
    port: 3000
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 200m
      memory: 256Mi
```

### Backend Configuration
```yaml
backend:
  enabled: true
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  replicaCount: 1
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
  env:
    DATABASE_URL: "your_neon_db_url_here"
    BETTER_AUTH_SECRET: "your_better_auth_secret_here"
    # ... other environment variables
```

### MCP Server Configuration
```yaml
mcpServer:
  enabled: true
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  replicaCount: 1
  service:
    type: ClusterIP
    port: 8808
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi
```

## AI-Assisted DevOps Tools

### Installing kubectl-ai
Follow the instructions at https://github.com/GoogleCloudPlatform/kubectl-ai to install the kubectl-ai plugin for AI-assisted Kubernetes operations.

### Example AI Commands
```bash
# Describe pods
kubectl ai "describe the pods in the default namespace"

# Scale deployments
kubectl ai "scale the backend deployment to 2 replicas"

# Troubleshoot issues
kubectl ai "check why a pod is failing"
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods
```

### Check Logs
```bash
kubectl logs <pod-name>
```

### Check Services
```bash
kubectl get services
```

### Check Ingress
```bash
kubectl get ingress
```

### Describe Resources
```bash
kubectl describe pod <pod-name>
```

### Port Forwarding for Direct Access
```bash
kubectl port-forward service/todo-chatbot-frontend 3000:3000
kubectl port-forward service/todo-chatbot-backend 8000:8000
```

## Cleanup

```bash
# Uninstall the Helm release
helm uninstall todo-chatbot

# Stop Minikube
minikube stop

# Optionally delete the Minikube VM
minikube delete
```

## Notes

- The application uses an external Neon PostgreSQL database (not deployed to Kubernetes)
- Authentication continues to work with Better Auth and JWT tokens
- All existing functionality (tasks, categories, user isolation) remains intact
- The deployment maintains the same security model as the existing application