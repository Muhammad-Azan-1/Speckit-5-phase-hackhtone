# Data Model: Kubernetes Deployment for Todo Chatbot

**Feature**: 010-k8s-deployment
**Date**: 2026-01-21
**Status**: Complete

## Overview

This document describes the data model considerations for deploying the Todo Chatbot application to Kubernetes. The deployment introduces new configuration data structures while maintaining the existing application data model.

## Existing Data Model (Unchanged)

The application's core data model remains unchanged from the existing implementation:

### Task Model
```sql
-- tasks table (existing)
id: INTEGER PRIMARY KEY
title: VARCHAR(255) NOT NULL
description: TEXT
completed: BOOLEAN DEFAULT FALSE
user_id: VARCHAR(255) NOT NULL -- Foreign key to Better Auth user
created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
category_id: INTEGER REFERENCES categories(id) -- Nullable foreign key
```

### Category Model
```sql
-- categories table (existing)
id: INTEGER PRIMARY KEY
name: VARCHAR(100) NOT NULL
icon: VARCHAR(10) DEFAULT '📁'
user_id: VARCHAR(255) NOT NULL -- Foreign key to Better Auth user
created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
```

## New Configuration Data Models (Kubernetes Deployment)

### Helm Values Data Model
The Helm chart will use a values.yaml structure with the following configuration model:

```yaml
# Global configuration
global:
  imageRegistry: string (optional) # Registry for all images
  imagePullSecrets: []string # Secrets for private registries
  storageClass: string (optional) # Default storage class

# Frontend configuration
frontend:
  enabled: boolean # Whether to deploy frontend
  image:
    repository: string # Image repository
    tag: string # Image tag
    pullPolicy: string # Image pull policy
  replicaCount: integer # Number of replicas
  service:
    type: string # Service type (ClusterIP, NodePort, LoadBalancer)
    port: integer # Service port
  resources:
    requests:
      cpu: string # CPU request (e.g., "100m")
      memory: string # Memory request (e.g., "128Mi")
    limits:
      cpu: string # CPU limit
      memory: string # Memory limit
  nodeSelector: object # Node selection constraints
  tolerations: []object # Tolerations for node taints
  affinity: object # Node affinity rules

# Backend configuration
backend:
  enabled: boolean # Whether to deploy backend
  image:
    repository: string # Image repository
    tag: string # Image tag
    pullPolicy: string # Image pull policy
  replicaCount: integer # Number of replicas
  service:
    type: string # Service type
    port: integer # Service port
  resources:
    requests:
      cpu: string # CPU request
      memory: string # Memory request
    limits:
      cpu: string # CPU limit
      memory: string # Memory limit
  env:
    DATABASE_URL: string # Database connection string
    BETTER_AUTH_URL: string # Better Auth URL
    BETTER_AUTH_SECRET: string # Better Auth secret
    JWT_ALGORITHM: string # JWT algorithm
    CORS_ORIGINS: string # CORS allowed origins

# MCP Server configuration
mcpServer:
  enabled: boolean # Whether to deploy MCP server
  image:
    repository: string # Image repository
    tag: string # Image tag
    pullPolicy: string # Image pull policy
  replicaCount: integer # Number of replicas
  service:
    type: string # Service type
    port: integer # Service port
  resources:
    requests:
      cpu: string # CPU request
      memory: string # Memory request
    limits:
      cpu: string # CPU limit
      memory: string # Memory limit
  env:
    DATABASE_URL: string # Database connection string
    BETTER_AUTH_URL: string # Better Auth URL
    BETTER_AUTH_SECRET: string # Better Auth secret

# Ingress configuration
ingress:
  enabled: boolean # Whether to create ingress
  className: string # Ingress class name
  annotations: object # Ingress annotations
  hosts:
    - host: string # Hostname
      paths: # Path configurations
        - path: string # Path
          pathType: string # Path type
  tls: # TLS configuration
    - secretName: string # TLS secret name
      hosts: []string # Hosts for TLS

# Database configuration (external - Neon PostgreSQL)
database:
  external: boolean # Whether to use external database
  url: string # External database URL
```

### Kubernetes Secret Model
The deployment will create Kubernetes secrets with the following structure:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-chatbot-secrets
type: Opaque
data:
  BETTER_AUTH_SECRET: base64-encoded-string
  DATABASE_URL: base64-encoded-string
  JWT_ALGORITHM: base64-encoded-string
  OPENAI_API_KEY: base64-encoded-string # If needed for AI features
```

### Kubernetes ConfigMap Model
Configuration data will be stored in ConfigMaps:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-chatbot-config
data:
  NEXT_PUBLIC_API_URL: string # Frontend API URL
  NEXT_PUBLIC_BETTER_AUTH_URL: string # Frontend Auth URL
  CORS_ORIGINS: string # Comma-separated list of allowed origins
  LOG_LEVEL: string # Logging level (e.g., "INFO", "DEBUG")
```

### Deployment Resource Model
Kubernetes deployments will have the following structure:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: string # Deployment name
  labels:
    app: string # Application name
    version: string # Application version
spec:
  replicas: integer # Number of replicas
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
          image: string # Container image
          ports:
            - containerPort: integer # Container port
              name: string # Port name
          envFrom:
            - configMapRef:
                name: string # ConfigMap reference
            - secretRef:
                name: string # Secret reference
          env:
            - name: string # Environment variable name
              valueFrom:
                secretKeyRef:
                  name: string # Secret name
                  key: string # Secret key
          resources:
            requests:
              cpu: string # CPU request
              memory: string # Memory request
            limits:
              cpu: string # CPU limit
              memory: string # Memory limit
          livenessProbe:
            httpGet:
              path: string # Health check path
              port: integer # Health check port
            initialDelaySeconds: integer # Initial delay
            periodSeconds: integer # Check interval
          readinessProbe:
            httpGet:
              path: string # Ready check path
              port: integer # Ready check port
            initialDelaySeconds: integer # Initial delay
            periodSeconds: integer # Check interval
      imagePullSecrets:
        - name: string # Image pull secret name (if private registry)
```

### Service Resource Model
Kubernetes services will have the following structure:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: string # Service name
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

## MCP Server Data Model (AI Integration)

The MCP server will maintain its existing data model for tool operations, but will now run as a Kubernetes service:

### Task Operation Data Flow
- Input: Natural language request from AI agent
- Processing: MCP server translates to database operations
- Output: Structured response with operation results
- Database: Standard Task and Category models (unchanged)

## Security Data Model

### RBAC Configuration
The deployment will implement the following RBAC model:

```yaml
# Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: todo-chatbot-service-account
  namespace: default

# Role (if namespace-level access needed)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
rules:
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps", "secrets"]
    verbs: ["get", "list", "watch"]

# Role Binding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
subjects:
  - kind: ServiceAccount
    name: todo-chatbot-service-account
roleRef:
  kind: Role
  name: todo-chatbot-role
  apiGroup: rbac.authorization.k8s.io
```

## Migration Considerations

### Database Schema (No Changes)
- The existing Neon PostgreSQL schema remains unchanged
- No new tables or modifications required
- All existing data remains compatible

### Configuration Migration
- Environment variables will be moved from local .env files to Kubernetes ConfigMaps/Secrets
- Database connection strings will remain external (Neon PostgreSQL)
- Authentication tokens will continue to use Better Auth JWT system

## Validation Criteria

### Data Integrity
- All existing data remains accessible and unchanged
- User data isolation is maintained across deployments
- Authentication system continues to function correctly
- No data loss during deployment process

### Configuration Validation
- All environment variables properly configured in Kubernetes
- Database connections established successfully
- Authentication tokens validated correctly
- AI tools configured with proper access

## Dependencies

- Neon PostgreSQL (external database)
- Better Auth service (authentication)
- Kubernetes cluster (Minikube/local)
- Helm package manager
- Docker for containerization