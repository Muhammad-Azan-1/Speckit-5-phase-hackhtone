# API Contracts: Kubernetes Deployment for Todo Chatbot

**Feature**: 010-k8s-deployment
**Date**: 2026-01-21
**Status**: Draft

## Overview

This document specifies the API contracts for the Kubernetes deployment of the Todo Chatbot application. The deployment introduces new operational endpoints for Kubernetes and AI-assisted DevOps while maintaining all existing functionality.

## Kubernetes API Endpoints

### 1. Helm Chart Values Contract

**Purpose**: Defines the configuration contract for the Helm chart deployment

**Values Structure**:
```yaml
# Global configuration
global:
  imageRegistry: string (optional) # Registry for all images
  imagePullSecrets: []string (optional) # Secrets for private registries
  storageClass: string (optional) # Default storage class

# Frontend configuration
frontend:
  enabled: boolean # Whether to deploy frontend
  image:
    repository: string # Image repository
    tag: string # Image tag
    pullPolicy: string # Image pull policy (Never for local Minikube)
  replicaCount: integer # Number of replicas (default: 1)
  service:
    type: string # Service type (ClusterIP, NodePort, LoadBalancer - default: ClusterIP)
    port: integer # Service port (default: 3000)
  resources:
    requests:
      cpu: string # CPU request (e.g., "100m")
      memory: string # Memory request (e.g., "128Mi")
    limits:
      cpu: string # CPU limit
      memory: string # Memory limit
  nodeSelector: object (optional) # Node selection constraints
  tolerations: []object (optional) # Tolerations for node taints
  affinity: object (optional) # Node affinity rules

# Backend configuration
backend:
  enabled: boolean # Whether to deploy backend
  image:
    repository: string # Image repository
    tag: string # Image tag
    pullPolicy: string # Image pull policy (Never for local Minikube)
  replicaCount: integer # Number of replicas (default: 1)
  service:
    type: string # Service type (ClusterIP, default)
    port: integer # Service port (default: 8000)
  resources:
    requests:
      cpu: string # CPU request
      memory: string # Memory request
    limits:
      cpu: string # CPU limit
      memory: string # Memory limit
  env:
    DATABASE_URL: string # Database connection string (required)
    BETTER_AUTH_SECRET: string # Better Auth secret (required)
    JWT_ALGORITHM: string # JWT algorithm (default: "HS256")
    CORS_ORIGINS: string # Comma-separated list of allowed origins

# MCP Server configuration
mcpServer:
  enabled: boolean # Whether to deploy MCP server
  image:
    repository: string # Image repository
    tag: string # Image tag
    pullPolicy: string # Image pull policy (Never for local Minikube)
  replicaCount: integer # Number of replicas (default: 1)
  service:
    type: string # Service type (ClusterIP, default)
    port: integer # Service port (default: 8808)
  resources:
    requests:
      cpu: string # CPU request
      memory: string # Memory request
    limits:
      cpu: string # CPU limit
      memory: string # Memory limit
  env:
    DATABASE_URL: string # Database connection string (required)
    BETTER_AUTH_SECRET: string # Better Auth secret (required)

# Ingress configuration
ingress:
  enabled: boolean # Whether to create ingress (default: true)
  className: string # Ingress class name (default: "nginx")
  annotations: object (optional) # Ingress annotations
  hosts:
    - host: string # Hostname (default: "todo.local")
      paths: # Path configurations
        - path: string # Path (default: "/")
          pathType: string # Path type (default: "Prefix")
  tls: # TLS configuration (optional)
    - secretName: string # TLS secret name
      hosts: []string # Hosts for TLS

# Database configuration (external - Neon PostgreSQL)
database:
  external: boolean # Whether to use external database (default: true)
  url: string # External database URL (required)
```

### 2. Kubernetes Resource Contracts

#### Deployment Contract
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: string # Must match pattern: {app-name}-{component}
  labels:
    app: string # Application name
    version: string # Application version
spec:
  replicas: integer # Number of pod replicas
  selector:
    matchLabels:
      app: string # Matching label selector
  template:
    metadata:
      labels:
        app: string # Pod labels
    spec:
      containers:
        - name: string # Container name
          image: string # Container image with tag
          imagePullPolicy: string # Image pull policy
          ports:
            - containerPort: integer # Container port
              name: string # Port name
          envFrom: # Environment from ConfigMaps/Secrets
            - configMapRef:
                name: string # ConfigMap reference
            - secretRef:
                name: string # Secret reference
          env: # Individual environment variables
            - name: string # Environment variable name
              valueFrom:
                secretKeyRef:
                  name: string # Secret name
                  key: string # Secret key
          resources: # Resource requests and limits
            requests:
              cpu: string # CPU request
              memory: string # Memory request
            limits:
              cpu: string # CPU limit
              memory: string # Memory limit
          livenessProbe: # Health check probe
            httpGet:
              path: string # Health check path
              port: integer # Health check port
            initialDelaySeconds: integer # Initial delay
            periodSeconds: integer # Check interval
          readinessProbe: # Ready check probe
            httpGet:
              path: string # Ready check path
              port: integer # Ready check port
            initialDelaySeconds: integer # Initial delay
            periodSeconds: integer # Check interval
```

#### Service Contract
```yaml
apiVersion: v1
kind: Service
metadata:
  name: string # Service name with component suffix
  labels:
    app: string # Application name
spec:
  type: string # Service type (ClusterIP, NodePort, LoadBalancer)
  selector:
    app: string # Selector for pods
  ports:
    - name: string # Port name
      port: integer # Service port
      targetPort: integer # Target port on pods
      protocol: string # Protocol (TCP/UDP)
```

#### Ingress Contract
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: string # Ingress name
  labels:
    app: string # Application name
  annotations: object # Ingress controller specific annotations
spec:
  ingressClassName: string # Ingress class name
  rules:
    - host: string # Hostname
      http:
        paths:
          - path: string # Path pattern
            pathType: string # Path type (Prefix, Exact, ImplementationSpecific)
            backend:
              service:
                name: string # Backend service name
                port:
                  number: integer # Backend service port
  tls: # TLS configuration (optional)
    - hosts: []string # Hosts for TLS termination
      secretName: string # TLS secret name
```

## MCP Server API Contract

### 3. MCP Tools Contract

The MCP server exposes the following tools for AI agent integration:

#### Tool: add_task
```json
{
  "name": "add_task",
  "description": "Create a new task in the database",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "The user ID who owns this task"},
      "title": {"type": "string", "description": "The task title"},
      "description": {"type": "string", "description": "Optional task description"},
      "category_id": {"type": "integer", "description": "Optional category ID"}
    },
    "required": ["user_id", "title"]
  }
}
```

#### Tool: list_tasks
```json
{
  "name": "list_tasks",
  "description": "Retrieve tasks with optional filtering by status",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "The user ID to list tasks for"},
      "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all", "description": "Filter by completion status"}
    },
    "required": ["user_id"]
  }
}
```

#### Tool: complete_task
```json
{
  "name": "complete_task",
  "description": "Mark a task as complete or incomplete",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "The user ID who owns this task"},
      "task_id": {"type": "integer", "description": "The ID of the task to update"}
    },
    "required": ["user_id", "task_id"]
  }
}
```

#### Tool: delete_task
```json
{
  "name": "delete_task",
  "description": "Remove a task from the database",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "The user ID who owns this task"},
      "task_id": {"type": "integer", "description": "The ID of the task to delete"}
    },
    "required": ["user_id", "task_id"]
  }
}
```

#### Tool: update_task
```json
{
  "name": "update_task",
  "description": "Modify task title, description, or category",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "The user ID who owns this task"},
      "task_id": {"type": "integer", "description": "The ID of the task to update"},
      "title": {"type": "string", "description": "New title (optional)"},
      "description": {"type": "string", "description": "New description (optional)"},
      "category_id": {"type": "integer", "description": "New category ID (optional)"}
    },
    "required": ["user_id", "task_id"]
  }
}
```

## Security Contracts

### 4. Authentication Contract
All API endpoints (existing and new) must maintain the same authentication contract:
- JWT tokens in `Authorization: Bearer <token>` header
- Token validation using Better Auth secret
- User ID validation: token user_id must match URL parameter
- No cross-user data access allowed

### 5. Network Contract
- Internal communication: Service DNS names (e.g., backend-service:8000)
- External access: Through Ingress controller
- Port configuration: Frontend 3000, Backend 8000, MCP Server 8808
- CORS configuration: Allow frontend origin from values.yaml

## Deployment Validation Contract

### 6. Success Criteria
- All pods running (Ready status)
- Services accessible within cluster
- Ingress routing external traffic correctly
- Health checks passing
- Existing functionality preserved
- AI tools accessible and functional
- Authentication working with JWT tokens
- User data isolation maintained

### 7. Configuration Validation
- Environment variables properly set from ConfigMaps/Secrets
- Database connections established
- Resource requests/limits respected
- Proper service discovery working
- MCP server communicating with AI agents

## Operational Contracts

### 8. Scaling Contract
- Horizontal Pod Autoscaler (HPA) configuration (optional)
- Resource utilization thresholds
- Replica count boundaries (min/max)

### 9. Monitoring Contract
- Health endpoints available on all services
- Metrics endpoints (Prometheus) (optional)
- Log output in structured format
- Error reporting with appropriate status codes

## Error Handling Contracts

### 10. Kubernetes Error Handling
- Proper status reporting in Deployment status
- Event logging for resource events
- Health check failure detection
- Resource limit violation handling

### 11. Application Error Handling
- Same error contracts as existing API
- Proper HTTP status codes
- Consistent error response format
- Graceful degradation when possible