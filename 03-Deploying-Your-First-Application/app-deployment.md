# Step-by-Step Guide: Deploying Your First Application

In this guide, we will deploy a simple "Hello World" web application. For simplicity, we will use a pre-existing container image available on public container registries. This lets us focus on the Kubernetes side of things without needing to build our own container image first.

Our application is a simple web server that listens on port 80 and responds with "Hello Kubernetes!".

## The Kubernetes Way: Declarative Configuration with YAML

As we learned in Module 1, you tell Kubernetes what you want by providing a **declarative** configuration file. [8] These files are written in YAML (YAML Ain't Markup Language) and are often called "manifests". A manifest file describes the desired state of a resource, such as a Deployment or a Service. [1, 3]

We will create a single YAML file that contains the definitions for two separate Kubernetes objects:
1.  **A Deployment**: To manage our application's Pods.
2.  **A Service**: To expose our application to the network.

## Step 1: Create the Manifest File

Create a new file named `simple-app.yaml` in this directory. Copy and paste the following content into it. We will break down what it all means below.

```yaml
# In this file, we define two Kubernetes objects: a Deployment and a Service.
# Note the '---' separator which allows defining multiple resources in one file.

# ------------------- Deployment ------------------- #

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

# -------------------- Service -------------------- #

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
      # NodePort is the external port on the node to access the service
      # If not specified, Kubernetes will assign a random port.
      nodePort: 30001
