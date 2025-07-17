
# Module 5: Networking in Kubernetes

So far, you've successfully deployed an application and learned how to manage its configuration. But how do different parts of your application talk to each other? How do users from the outside world access your service? And how do you secure that communication?

Welcome to the networking module! In this section, you'll explore the fundamental networking concepts that make communication possible and secure in a Kubernetes cluster. We will revisit Services in more detail and introduce two powerful new objects: Ingress and Network Policies.

## Key Topics Covered

- **A Deep Dive into Services**: We'll explore the different types of Services (`ClusterIP`, `NodePort`, and `LoadBalancer`) and understand the specific use case for each one.
- **Ingress: The API Gateway**: Learn how to use an Ingress to manage external access to multiple services in your cluster, routing traffic based on hostnames or paths. This is the standard way to expose web applications in production.
- **Network Policies: A Firewall for Your Pods**: Discover how to use Network Policies to control the flow of traffic between Pods, creating a more secure, "zero-trust" environment within your cluster.

Understanding these concepts is essential for building robust, scalable, and secure applications on Kubernetes.

## 1. A Deep Dive into Services

In Module 3, you were introduced to a Service as a way to expose your application. Now, let's explore them in greater detail.

The core problem a Service solves is that **Pods are ephemeral**. A Deployment might create and destroy Pods for scaling or healing, meaning their IP addresses are unstable and cannot be relied upon for communication.

A **Service** provides a stable, virtual IP address and a DNS name that acts as a single, consistent entry point for a set of Pods. The Service automatically tracks the healthy Pods managed by a Deployment (using labels and selectors) and load-balances traffic between them.

There are three main types of Services you should know.

### 1.1 ClusterIP

- **What it does**: Exposes the Service on an internal IP address within the cluster.
- **Use Case**: This is the **default** Service type. It makes the Service reachable only from *within* the Kubernetes cluster. It's perfect for internal communication, such as a web frontend talking to a backend database.
- **Analogy**: Think of it as an unlisted phone number that only people inside the same office building can call.

#### Example: `ClusterIP`

Let's create a backend service that is only accessible internally.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-internal-backend
spec:
  # type: ClusterIP is the default, so it's optional
  type: ClusterIP
  selector:
    app: my-backend # Forwards traffic to Pods with this label
  ports:
    - protocol: TCP
      port: 8080       # The port this Service is available on
      targetPort: 80   # The port the container is listening on
```

### 1.2 NodePort

- **What it does**: Exposes the Service on a static port on each Node's IP address.
- **Use Case**: This is great for development, testing, and demos (like we did in Module 3!). It gives you a quick and easy way to access your application from outside the cluster. It is not typically used for production web traffic.
- **Analogy**: This is like giving every employee in the office a special extension number on the main company phone line that anyone from the outside can dial.

#### Example: NodePort

This is the type we used to access our "hello-kubernetes" application.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport-service
spec:
  type: NodePort
  selector:
    app: hello-kubernetes
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
      # The port on the Node you can use to access this service
      nodePort: 30001
```

To access this, you would go to `http://<Node_IP>:<nodePort>`.

### 1.3 LoadBalancer

- **What it does**: Exposes the Service externally using a cloud provider's load balancer.
- **Use Case**: This is the standard, production-grade way to expose a service to the internet. When you create a Service of this type in a cloud environment (like GCP, AWS, or Azure), Kubernetes will automatically provision a network load balancer from that cloud provider and configure it to route traffic to your Service.
- **Analogy**: This is like getting a dedicated, official 1-800 number for your business that automatically routes calls to the right employees.

#### Example: LoadBalancer

In a real cloud, this YAML would provision an external load balancer.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-loadbalancer-service
spec:
  type: LoadBalancer
  selector:
    app: my-production-app
  ports:
    - protocol: TCP
      port: 80      # The port the load balancer listens on
      targetPort: 8080 # The port on the pods to forward to
```

**Using LoadBalancer with Minikube**: Minikube doesn't have a real cloud load balancer, but it can simulate one! You can run the following command in a separate terminal window:

```bash
minikube tunnel
```

This command will run a process that allocates an "external" IP address to your LoadBalancer service, allowing you to access it just like you would in the cloud.

## 2. Managing External Access with Ingress

Using a `LoadBalancer` service is great, but it has a drawback: you typically need one for every service you want to expose, which can be inefficient and costly. Imagine you have ten different microservices—you don't want to pay for ten different load balancers.

This is where **Ingress** comes in. An Ingress is not a Service, but rather a smart router that sits in front of multiple services. It acts as an "API Gateway" or entry point to your cluster, allowing you to define complex routing rules for your HTTP and HTTPS traffic.

With an Ingress, you can:
- Give your services externally-reachable URLs.
- Load balance traffic to different services.
- Terminate SSL/TLS encryption.
- Route traffic based on hostname (e.g., `api.myapp.com` goes to the API service, `www.myapp.com` goes to the web service).
- Route traffic based on path (e.g., `myapp.com/api` goes to the API service, `myapp.com/` goes to the web service).

### 2.1 The Two Parts of Ingress

For Ingress to work, you need two things in your cluster:

1. **An Ingress Controller**: This is the actual software that does the routing. It's a Pod running in your cluster that watches for Ingress objects and configures itself accordingly. Popular Ingress controllers include NGINX, Traefik, and HAProxy.
2. **An Ingress Resource**: This is the YAML file you create. It contains the routing rules that you want the Ingress Controller to implement.

### 2.2 A Practical Example with Minikube

Let's expose our "hello-kubernetes" application using an Ingress.

#### Step 1: Enable the Ingress Controller Addon

Minikube comes with an NGINX Ingress controller that you can easily enable as an addon.

```bash
minikube addons enable ingress
```

This will install the Ingress controller in your cluster. You can verify it's running by checking for pods in the ingress-nginx namespace.

#### Step 2: Deploy an Application with a ClusterIP Service

The beauty of Ingress is that our services no longer need to be NodePort or LoadBalancer. The Ingress controller will route traffic to them internally.

Let's deploy our hello-kubernetes app again, but this time we'll use a simple ClusterIP service. Create a file named `ingress-demo-app.yaml`:

```yaml
# ingress-demo-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-k8s-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-k8s
  template:
    metadata:
      labels:
        app: hello-k8s
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
  name: hello-k8s-service
spec:
  type: ClusterIP # Internal service only
  selector:
    app: hello-k8s
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

Apply it to your cluster:
```bash
kubectl apply -f ingress-demo-app.yaml
```

#### Step 3: Create the Ingress Resource

Now, let's create the routing rules. Create a file named `my-ingress.yaml`:

```yaml
# my-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
spec:
  rules:
  - http:
      paths:
      - path: /hello
        pathType: Prefix
        backend:
          service:
            name: hello-k8s-service
            port:
              number: 80
```

This Ingress resource tells the controller: "Any HTTP traffic that comes in with a path starting with /hello should be sent to hello-k8s-service on port 80."

Apply the Ingress resource:
```bash
kubectl apply -f my-ingress.yaml
```

#### Step 4: Access Your Service via the Ingress

Now, you don't need a NodePort or a special tunnel. You can access your application directly through the Minikube IP address, which acts as the entry point for the Ingress controller.

First, get your Minikube IP:
```bash
minikube ip
```

Then, navigate to `http://<MINIKUBE_IP>/hello` in your browser or with curl.

You should see the "Hello Kubernetes!" response. You have successfully routed external traffic to an internal service using Ingress!

## 3. Securing Pods with Network Policies

By default, the network in a Kubernetes cluster is completely open. This means **any Pod can communicate with any other Pod**, regardless of which namespace they are in. This is simple, but not secure. For a production environment, you want to enforce a "zero-trust" security model, where you only allow the specific connections your application requires.

**Network Policies** are Kubernetes objects that act like a firewall for your Pods. They let you define rules about which Pods can accept traffic (ingress) and which Pods can send traffic (egress).

> **Important**: For Network Policies to work, your cluster must be running a networking plugin that supports them, such as Calico, Cilium, or Weave. Minikube's default CNI (Container Network Interface) supports them.

### 3.1 A Practical Example

Let's create a scenario with a `frontend` and a `backend`, and then use a Network Policy to ensure that *only* the `frontend` can talk to the `backend`.

#### Step 1: Deploy the Example Apps

First, let's create a dedicated namespace for this test.
```bash
kubectl create namespace network-policy-demo
```

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
```

Apply this in our new namespace:
```bash
kubectl apply -f demo-apps.yaml -n network-policy-demo
```

#### Step 2: Test Unrestricted Communication

Let's prove that the frontend can reach the backend by default. We will exec into the frontend pod and try to connect to the backend service.

```bash
# Exec into the frontend pod and run a 'wget' command against the backend
kubectl exec -it frontend -n network-policy-demo -- wget -O- http://backend-service
```

This should work, and you will see the default NGINX "Welcome" HTML page. This confirms the network is open.

#### Step 3: Isolate the Backend with a "Deny All" Policy

Now, let's lock down the backend. Create a file named `backend-deny-all.yaml`:

```yaml
# backend-deny-all.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-deny-all
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
```

This policy selects all Pods with the label `app: backend`. Because it specifies `policyTypes: [Ingress]` but has an empty ingress rule set, it denies all incoming traffic.

Apply it:
```bash
kubectl apply -f backend-deny-all.yaml -n network-policy-demo
```

Now, try the wget command from Step 2 again.

```bash
kubectl exec -it frontend -n network-policy-demo -- wget -O- http://backend-service
```

This time, the command will hang and eventually time out. We have successfully firewalled our backend Pod!

#### Step 4: Allow Traffic Only from the Frontend

Finally, let's create a rule to allow only the frontend to connect. Create `allow-frontend.yaml`:

```yaml
# allow-frontend.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  # Apply this policy to backend pods
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    # Allow traffic from pods with this label
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 80
```

This policy is also applied to backend pods, but this time it has an ingress rule. It says: "Allow incoming traffic on TCP port 80 from any pod that has the label `app: frontend`."

Apply it:
```bash
kubectl apply -f allow-frontend.yaml -n network-policy-demo
```

Now, run the test from Step 2 one last time. It will work again! You have successfully defined and enforced a specific network rule, which is a cornerstone of building secure applications in Kubernetes.

## Summary

In this module, you've learned about the three pillars of Kubernetes networking:

1. **Services** provide stable endpoints for ephemeral Pods, with different types (`ClusterIP`, `NodePort`, `LoadBalancer`) serving different use cases.

2. **Ingress** acts as an intelligent router and API gateway, allowing you to efficiently manage external access to multiple services with features like path-based routing, SSL termination, and load balancing.

3. **Network Policies** provide security by acting as a firewall for your Pods, allowing you to implement zero-trust networking principles by controlling which Pods can communicate with each other.

These concepts work together to create a robust, scalable, and secure networking foundation for your Kubernetes applications. Module 5 represents a crucial step in understanding how to build production-ready applications that can communicate securely both internally and with the outside world.
