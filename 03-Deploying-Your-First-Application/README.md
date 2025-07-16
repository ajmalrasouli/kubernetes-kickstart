# 🚀 Module 3: Deploying Your First Application on Kubernetes

This is the moment you've been waiting for! In this module, we will take a simple, pre-built container image and deploy it to your local Minikube cluster. You will write your first Kubernetes manifest file and learn how to use `kubectl` to bring your application to life.

By the end of this module, you will have a tangible result: a running web server accessible from your own machine, all managed by Kubernetes.

## Key Topics Covered

*   **Understanding the Goal**: We'll start by looking at the simple web application we're going to deploy.
*   **Kubernetes Manifests (YAML)**: An introduction to the YAML file format, which is how you declare the "desired state" of your application to Kubernetes.
*   **Creating a Deployment**: You will write a Deployment manifest to tell Kubernetes to run your application.
*   **Creating a Service**: You will then write a Service manifest to expose your application and make it accessible over the network.
*   **Applying and Verifying**: You will learn the `kubectl apply` command to send your manifests to the cluster and other commands to verify that your application is running correctly.


_Module 3 brings your Kubernetes learning to life!_  
You'll finally see your application **running inside the Kubernetes cluster** you've built in earlier modules.

---

## 📁 File Overview

This module includes:
- `README.md`: High-level overview
- `app-deployment.md`: Step-by-step walkthrough
- `simple-app.yaml`: Kubernetes manifest

---

## 📘 03-Deploying-Your-First-Application/app-deployment.md

# Step-by-Step Guide: Deploying Your First Application

In this guide, we’ll deploy a simple “Hello World” web application using a publicly available container image. This keeps the focus on Kubernetes concepts rather than container creation.

The app is a basic web server that listens on port `8080` and returns:

> **"Hello Kubernetes!"**

---

## 🔧 Declarative Configuration with YAML

We’ll create one manifest file (`simple-app.yaml`) with two Kubernetes resources:

1. **Deployment** – manages your app's pods  
2. **Service** – exposes the app for external access

---

## 📝 Step 1: Create the Manifest File

Create a file called `simple-app.yaml` and paste the following:

```yaml
# Deployment definition
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-kubernetes-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-kubernetes
  template:
    metadata:
      labels:
        app: hello-kubernetes
    spec:
      containers:
      - name: hello-kubernetes-container
        image: "paulbouwer/hello-kubernetes:1.7"
        ports:
        - containerPort: 8080

---

# Service definition
apiVersion: v1
kind: Service
metadata:
  name: hello-kubernetes-service
spec:
  type: NodePort
  selector:
    app: hello-kubernetes
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
      nodePort: 30001
```

---

## 📖 Step 2: Understand the Deployment

| Key | Description |
|-----|-------------|
| `apiVersion: apps/v1` | Uses the apps API group for Deployments |
| `replicas: 2` | Runs two pods for high availability |
| `selector.matchLabels` | Matches pods with `app: hello-kubernetes` |
| `template.spec.containers.image` | Pulls a public image from Docker Hub |
| `containerPort: 8080` | Port the app listens to inside the container |

---

## 📖 Step 3: Understand the Service

| Key | Description |
|-----|-------------|
| `type: NodePort` | Exposes the app outside the cluster |
| `selector.app` | Targets pods labeled `app: hello-kubernetes` |
| `port: 80` | Internal cluster access port |
| `targetPort: 8080` | Forwards traffic to the container's port |
| `nodePort: 30001` | Access point from host machine |

---

## 📦 Step 4: Apply the Manifest

Make sure Minikube is running:

```bash
minikube start
```

Then apply the manifest:

```bash
kubectl apply -f simple-app.yaml
```

You should see success messages for both the deployment and service.

---

## 🔍 Step 5: Verify the Deployment

Check the status of the deployed resources:

```bash
# Check deployment
kubectl get deployment

# Check pods
kubectl get pods

# Check service
kubectl get service
```

---

## 🌐 Step 6: Access the Application

Retrieve Minikube’s IP:

```bash
minikube ip
```

Visit the application in your browser at:

```
http://<MINIKUBE_IP>:30001
```

You should see:

> Hello Kubernetes!

🎉 **Congratulations!** You've just deployed your first app on Kubernetes!

---

## 📄 03-Deploying-Your-First-Application/simple-app.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-kubernetes-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-kubernetes
  template:
    metadata:
      labels:
        app: hello-kubernetes
    spec:
      containers:
      - name: hello-kubernetes-container
        image: "paulbouwer/hello-kubernetes:1.7"
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: hello-kubernetes-service
spec:
  type: NodePort
  selector:
    app: hello-kubernetes
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
      nodePort: 30001
```
