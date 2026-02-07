# Quickstart Guide: Kubernetes Deployment for Todo Chatbot

**Feature**: 010-k8s-deployment
**Date**: 2026-01-21
**Status**: Complete

## Overview

This guide provides the essential steps to set up and run the Kubernetes deployment for the Todo Chatbot application using Minikube, Helm Charts, and AI-assisted DevOps tools.

## Prerequisites

### System Requirements
- Docker Desktop with Kubernetes enabled OR Minikube installed
- Helm 3.x
- kubectl
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL database (existing from Phase II)

### Installation Commands
```bash
# Install Minikube (if not using Docker Desktop Kubernetes)
brew install minikube

# Install Helm
brew install helm

# Install kubectl (usually comes with Docker Desktop or kubectl)
brew install kubectl

# Install kubectl-ai plugin (AI-assisted Kubernetes operations)
# Follow instructions from: https://github.com/GoogleCloudPlatform/kubectl-ai

# Install kagent (AI-assisted cluster management)
# Follow instructions from: https://github.com/kagent-dev/kagent
```

### Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Navigate to the project directory:
   ```bash
   cd Phase2  # or your project directory
   ```

3. Ensure you have the required environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Update the .env file with your actual values:
   # - DATABASE_URL (your Neon PostgreSQL connection string)
   # - BETTER_AUTH_SECRET (same secret used in Phase II)
   # - JWT_ALGORITHM (should be "HS256")
   # - CORS_ORIGINS (your frontend URL, e.g., "http://localhost:3000")
   ```

## Quick Start: Deploy to Minikube

### 1. Start Minikube
```bash
# Start Minikube with sufficient resources
minikube start --driver=docker --cpus=2 --memory=4g

# Enable ingress addon for external access
minikube addons enable ingress

# Verify Minikube is running
minikube status
```

### 2. Switch to Minikube Docker Environment
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

# Verify images were built
docker images | grep todo
```

### 4. Create Helm Chart
```bash
# Navigate back to project root
cd ..

# Create Helm chart directory structure
mkdir -p k8s/helm/todo-chatbot/{templates,charts}

# Create Chart.yaml
cat > k8s/helm/todo-chatbot/Chart.yaml << EOF
apiVersion: v2
name: todo-chatbot
description: A Helm chart for deploying the Todo Chatbot application
type: application
version: 0.1.0
appVersion: "1.0.0"
EOF

# Create values.yaml with default configuration
cat > k8s/helm/todo-chatbot/values.yaml << EOF
# Default values for todo-chatbot
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

global:
  imageRegistry: ""
  imagePullSecrets: []
  storageClass: ""

frontend:
  enabled: true
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: Never  # Since we're using Minikube's local registry
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

backend:
  enabled: true
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: Never  # Since we're using Minikube's local registry
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
    JWT_ALGORITHM: "HS256"
    CORS_ORIGINS: "http://localhost:30000,http://todo.local"

mcpServer:
  enabled: true
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: Never
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

ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

config:
  NEXT_PUBLIC_API_URL: "http://todo.local/api"
  NEXT_PUBLIC_BETTER_AUTH_URL: "http://todo.local"
  LOG_LEVEL: "INFO"

# Database configuration (external - Neon PostgreSQL)
database:
  external: true
  url: "your_neon_db_url_here"
EOF
```

### 5. Update Values with Real Configuration
```bash
# Edit the values.yaml file to include your actual database URL and auth secret
# Replace "your_neon_db_url_here" with your actual Neon PostgreSQL connection string
# Replace "your_better_auth_secret_here" with your actual Better Auth secret
# Update CORS_ORIGINS to match your ingress host
```

### 6. Create Helm Templates
```bash
# Create frontend deployment template
cat > k8s/helm/todo-chatbot/templates/frontend-deployment.yaml << 'EOF'
{{- if .Values.frontend.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-frontend
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app: frontend
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chatbot.selectorLabels" . | nindent 6 }}
      app: frontend
  template:
    metadata:
      labels:
        {{- include "todo-chatbot.selectorLabels" . | nindent 8 }}
        app: frontend
    spec:
      containers:
        - name: frontend
          image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
          imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.frontend.service.port }}
              name: http
          env:
            - name: NEXT_PUBLIC_API_URL
              value: "{{ .Values.config.NEXT_PUBLIC_API_URL }}"
            - name: NEXT_PUBLIC_BETTER_AUTH_URL
              value: "{{ .Values.config.NEXT_PUBLIC_BETTER_AUTH_URL }}"
            - name: LOG_LEVEL
              value: "{{ .Values.config.LOG_LEVEL }}"
          resources:
            {{- toYaml .Values.frontend.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
{{- end }}
EOF

# Create frontend service template
cat > k8s/helm/todo-chatbot/templates/frontend-service.yaml << 'EOF'
{{- if .Values.frontend.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-frontend
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app: frontend
spec:
  type: {{ .Values.frontend.service.type }}
  ports:
    - port: {{ .Values.frontend.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-chatbot.selectorLabels" . | nindent 4 }}
    app: frontend
{{- end }}
EOF

# Create backend deployment template
cat > k8s/helm/todo-chatbot/templates/backend-deployment.yaml << 'EOF'
{{- if .Values.backend.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-backend
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app: backend
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chatbot.selectorLabels" . | nindent 6 }}
      app: backend
  template:
    metadata:
      labels:
        {{- include "todo-chatbot.selectorLabels" . | nindent 8 }}
        app: backend
    spec:
      containers:
        - name: backend
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.backend.service.port }}
              name: http
          env:
            - name: DATABASE_URL
              value: "{{ .Values.database.url }}"
            - name: BETTER_AUTH_SECRET
              value: "{{ .Values.backend.env.BETTER_AUTH_SECRET }}"
            - name: JWT_ALGORITHM
              value: "{{ .Values.backend.env.JWT_ALGORITHM }}"
            - name: CORS_ORIGINS
              value: "{{ .Values.backend.env.CORS_ORIGINS }}"
            - name: LOG_LEVEL
              value: "{{ .Values.config.LOG_LEVEL }}"
          resources:
            {{- toYaml .Values.backend.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
{{- end }}
EOF

# Create backend service template
cat > k8s/helm/todo-chatbot/templates/backend-service.yaml << 'EOF'
{{- if .Values.backend.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-backend
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app: backend
spec:
  type: {{ .Values.backend.service.type }}
  ports:
    - port: {{ .Values.backend.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-chatbot.selectorLabels" . | nindent 4 }}
    app: backend
{{- end }}
EOF

# Create MCP server deployment template
cat > k8s/helm/todo-chatbot/templates/mcp-server-deployment.yaml << 'EOF'
{{- if .Values.mcpServer.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-mcp-server
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app: mcp-server
spec:
  replicas: {{ .Values.mcpServer.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chatbot.selectorLabels" . | nindent 6 }}
      app: mcp-server
  template:
    metadata:
      labels:
        {{- include "todo-chatbot.selectorLabels" . | nindent 8 }}
        app: mcp-server
    spec:
      containers:
        - name: mcp-server
          image: "{{ .Values.mcpServer.image.repository }}:{{ .Values.mcpServer.image.tag }}"
          imagePullPolicy: {{ .Values.mcpServer.image.pullPolicy }}
          command: ["python", "mcp_server.py"]
          ports:
            - containerPort: {{ .Values.mcpServer.service.port }}
              name: http
          env:
            - name: DATABASE_URL
              value: "{{ .Values.database.url }}"
            - name: BETTER_AUTH_SECRET
              value: "{{ .Values.backend.env.BETTER_AUTH_SECRET }}"
          resources:
            {{- toYaml .Values.mcpServer.resources | nindent 12 }}
{{- end }}
EOF

# Create MCP server service template
cat > k8s/helm/todo-chatbot/templates/mcp-server-service.yaml << 'EOF'
{{- if .Values.mcpServer.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-mcp-server
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app: mcp-server
spec:
  type: {{ .Values.mcpServer.service.type }}
  ports:
    - port: {{ .Values.mcpServer.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-chatbot.selectorLabels" . | nindent 4 }}
    app: mcp-server
{{- end }}
EOF

# Create ingress template
cat > k8s/helm/todo-chatbot/templates/ingress.yaml << 'EOF'
{{- if and .Values.ingress.enabled .Values.frontend.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-ingress
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "todo-chatbot.fullname" $ }}-frontend
                port:
                  number: {{ $.Values.frontend.service.port }}
          {{- end }}
    {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
{{- end }}
EOF

# Create helper templates
cat > k8s/helm/todo-chatbot/templates/_helpers.tpl << 'EOF'
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-chatbot.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "todo-chatbot.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-chatbot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-chatbot.labels" -}}
helm.sh/chart: {{ include "todo-chatbot.chart" . }}
{{ include "todo-chatbot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-chatbot.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
EOF
```

### 7. Install the Helm Chart
```bash
# Navigate to the Helm chart directory
cd k8s/helm/todo-chatbot

# Install the chart
helm install todo-chatbot . --values values.yaml

# Verify the installation
kubectl get pods
kubectl get services
kubectl get ingress
```

### 8. Access the Application
```bash
# Get the Minikube IP
minikube ip

# Add the domain to your hosts file
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Access the application at http://todo.local
```

### 9. AI-Assisted Operations (kubectl-ai and kagent)
```bash
# Test kubectl-ai (if installed)
kubectl ai "describe the pods in the default namespace"

# Test kagent (if installed)
kagent "analyze the cluster health"

# Example AI-assisted operations:
kubectl ai "scale the backend deployment to 2 replicas"
kubectl ai "check why a pod is failing"
kubectl ai "show me the resource usage of all deployments"
```

### 10. Troubleshooting
```bash
# Check pod status
kubectl get pods

# Check logs for a specific pod
kubectl logs <pod-name>

# Check service status
kubectl get services

# Check ingress status
kubectl get ingress

# Describe a resource for more details
kubectl describe pod <pod-name>

# Port forward to access services directly
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

## Additional Notes
- The application will use your existing Neon PostgreSQL database from Phase II
- Authentication will continue to work with Better Auth and JWT tokens
- The MCP server will be available for AI agent integration
- All existing functionality (tasks, categories, user isolation) remains intact
- The deployment maintains the same security model as the existing application