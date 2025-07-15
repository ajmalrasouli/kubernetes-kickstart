# 🌱 Step-by-Step Guide: Setting Up a Lab with Minikube

## 🚀 What is Minikube?

**Minikube** is a tool that makes it easy to run a single-node Kubernetes cluster on your local machine (like a laptop or desktop). It's perfect for:

- Beginners learning Kubernetes
- Developers testing locally
- Anyone who wants a lightweight Kubernetes setup without a cloud provider

Minikube runs all the core Kubernetes components inside a single virtual machine or container.

---

## 🧰 Prerequisites

Before we start, ensure you have the following:

1. **A decent computer**  
   - Minimum: 2 CPUs, 2GB RAM, 20GB disk space

2. **A VM or container manager**  
   - Recommended: [Docker Desktop](https://www.docker.com/products/docker-desktop)

---

## 🛠️ Step 1: Install Minikube

### 🖥 macOS

Install via [Homebrew](https://brew.sh/):

```bash
brew install minikube
```

---

### 🪟 Windows

Install via [Chocolatey](https://chocolatey.org/):

```powershell
choco install minikube
```

Or [download the installer](https://minikube.sigs.k8s.io/docs/start/) from the official documentation.

---

### 🐧 Linux

Download the binary and install it:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

---

## 🚦 Step 2: Start Your Cluster

Start your local Kubernetes cluster:

```bash
minikube start
```

> ⏳ The first time may take a few minutes as it pulls Kubernetes images and sets up the cluster.

---

## ✅ Step 3: Verify Your Cluster

Check Minikube status:

```bash
minikube status
```

Check if your Kubernetes node is ready:

```bash
kubectl get nodes
```

You should see output like:

```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   Xs    v1.XX.X
```

---

## 🎨 Bonus: Kubernetes Dashboard

Visualize your cluster using the dashboard:

```bash
minikube dashboard
```

This will launch a browser with a UI to explore your cluster.

---

## 🔧 Managing Your Cluster

Useful commands:

- 💤 **Pause (stop) the cluster**:
  ```bash
  minikube stop
  ```

- 🧹 **Delete the cluster**:
  ```bash
  minikube delete
  ```

---

## 🎉 Congratulations!

You now have a working local Kubernetes lab with Minikube!  
In the next module, we'll **deploy your first application** into this cluster.

> _Happy Kube-ing!_ 🚢
