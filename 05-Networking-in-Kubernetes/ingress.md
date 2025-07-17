
---

### `05-Networking-in-Kubernetes/ingress.md`

```markdown
# Managing External Access with Ingress

Using a `LoadBalancer` service is great, but it has a drawback: you typically need one for every service you want to expose, which can be inefficient and costly. Imagine you have ten different microservices—you don't want to pay for ten different load balancers.

This is where **Ingress** comes in. An Ingress is not a Service, but rather a smart router that sits in front of multiple services. It acts as an "API Gateway" or entry point to your cluster, allowing you to define complex routing rules for your HTTP and HTTPS traffic.

With an Ingress, you can:
*   Give your services externally-reachable URLs.
*   Load balance traffic to different services.
*   Terminate SSL/TLS encryption.
*   Route traffic based on hostname (e.g., `api.myapp.com` goes to the API service, `www.myapp.com` goes to the web service).
*   Route traffic based on path (e.g., `myapp.com/api` goes to the API service, `myapp.com/` goes to the web service).

## The Two Parts of Ingress

For Ingress to work, you need two things in your cluster:

1.  **An Ingress Controller**: This is the actual software that does the routing. It's a Pod running in your cluster that watches for Ingress objects and configures itself accordingly. Popular Ingress controllers include NGINX, Traefik, and HAProxy.
2.  **An Ingress Resource**: This is the YAML file you create. It contains the routing rules that you want the Ingress Controller to implement.

## A Practical Example with Minikube

Let's expose our "hello-kubernetes" application using an Ingress.

### Step 1: Enable the Ingress Controller Addon

Minikube comes with an NGINX Ingress controller that you can easily enable as an addon.

```bash
minikube addons enable ingress
