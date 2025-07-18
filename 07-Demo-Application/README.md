
# Module 7: Kube-Demo-App

Welcome to the final hands-on module! This application is a simple two-tier guestbook designed to demonstrate all the core Kubernetes concepts we've learned in this guide. This is a complete, end-to-end workflow that includes building a container image, deploying it, and debugging common issues.

---

## 🏗️ Application Architecture

- **Frontend**: A Python Flask web server.
- **Backend**: A PostgreSQL database.

---

## 📦 Kubernetes Objects Used

This demo creates and uses the following objects:

- `Namespace`
- `Secret`
- `ConfigMap`
- `PersistentVolumeClaim` (via `StorageClass`)
- `Deployment` (for frontend and backend)
- `Service` (`ClusterIP`)
- `NetworkPolicy`

---

## ⚙️ Prerequisites

Before you begin:

1. A running Minikube cluster (`minikube start`)
2. Docker Desktop installed and running
3. A free [Docker Hub](https://hub.docker.com/) account (used to push your image)

---

## 🚀 Deployment Steps

### 🔧 Step 1: Build and Push the Frontend Image

```bash
# Navigate to the app directory
cd guestbook-app

# Build the container image (replace with your Docker Hub username)
docker build -t your-dockerhub-username/kube-demo-app:v2 .

# Login to Docker Hub
docker login

# Push the image
docker push your-dockerhub-username/kube-demo-app:v2
```

---

### ✏️ Step 2: Update the Deployment Manifest

Edit the frontend Deployment manifest to point to your image:

```yaml
# BEFORE
image: "google/gemini-kube-demo:latest"

# AFTER (replace with your actual Docker Hub username)
image: "your-dockerhub-username/kube-demo-app:v2"
```

Save the file after editing.

---

### 🚢 Step 3: Deploy the Application

```bash
# Go back to the root directory
cd ../07-Demo-Application

# Apply all manifests
kubectl apply -R -f kubernetes-manifests/
```

---

### ✅ Step 4: Verify the Deployment

```bash
# Check the status of all resources
kubectl get all -n kube-demo-app
```

Wait until all pods are in `Running` state and `READY` column shows `1/1`.

---

### 🌐 Step 5: Access the Application

```bash
minikube service frontend-service -n kube-demo-app
```

This opens the guestbook app in your browser (e.g., <http://127.0.0.1:XXXXX>).

---

### 💾 Step 6: Demonstrate Persistence

```bash
# Post a message on the guestbook app

# Delete the database pod
kubectl delete pod -l app=postgres -n kube-demo-app

# Wait for the new pod to start
kubectl get pods -n kube-demo-app

# Refresh the browser to confirm your message is still there
```

The data is preserved thanks to the PersistentVolumeClaim.

---

## 🧰 Troubleshooting

### ❌ Pod status is `ImagePullBackOff` or `ErrImagePull`

- Ensure the image name matches exactly (including your Docker Hub username).
- Make sure your Docker Hub repo is set to **Public**.
- If networking issues, try:

```bash
minikube delete
minikube start
```

---

### 🔁 Pod status is `CrashLoopBackOff`

Run this to get logs from the previous container instance:

```bash
kubectl logs <pod-name> -n kube-demo-app --previous
```

Fix the error (e.g., in `requirements.txt`), rebuild your image (e.g., `:v3`), and update the deployment.

---

## 🧹 Cleanup

To delete everything:

```bash
kubectl delete namespace kube-demo-app
```

This removes all resources tied to the app.

---

🎉 Congratulations! You've completed a full-stack Kubernetes deployment using all core concepts from this course.
