
---

### `05-Networking-in-Kubernetes/network-policies.md`

```markdown
# Securing Pods with Network Policies

By default, the network in a Kubernetes cluster is completely open. This means **any Pod can communicate with any other Pod**, regardless of which namespace they are in. This is simple, but not secure. For a production environment, you want to enforce a "zero-trust" security model, where you only allow the specific connections your application requires.

**Network Policies** are Kubernetes objects that act like a firewall for your Pods. They let you define rules about which Pods can accept traffic (ingress) and which Pods can send traffic (egress).

> **Important**: For Network Policies to work, your cluster must be running a networking plugin that supports them, such as Calico, Cilium, or Weave. Minikube's default CNI (Container Network Interface) supports them.

## A Practical Example

Let's create a scenario with a `frontend` and a `backend`, and then use a Network Policy to ensure that *only* the `frontend` can talk to the `backend`.

### Step 1: Deploy the Example Apps

First, let's create a dedicated namespace for this test.
`kubectl create namespace network-policy-demo`

Now, create a file named `demo-apps.yaml`:

```yaml
# demo-apps.yaml

# The backend application
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: nginx
        image: nginx
---
# The ClusterIP service for the backend
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - port: 80
---
# The frontend "client" application
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  containers:
  - name: busybox
    image: busybox
    # A simple command to keep the pod running
    command: ["sleep", "3600"]
