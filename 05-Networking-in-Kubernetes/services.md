05-Networking-in-Kubernetes/services.md

# A Deep Dive into Services

In Module 3, you were introduced to a Service as a way to expose your application. Now, let's explore them in greater detail.

The core problem a Service solves is that **Pods are ephemeral**. A Deployment might create and destroy Pods for scaling or healing, meaning their IP addresses are unstable and cannot be relied upon for communication.

A **Service** provides a stable, virtual IP address and a DNS name that acts as a single, consistent entry point for a set of Pods. The Service automatically tracks the healthy Pods managed by a Deployment (using labels and selectors) and load-balances traffic between them.

There are three main types of Services you should know.

## 1. ClusterIP

*   **What it does**: Exposes the Service on an internal IP address within the cluster.
*   **Use Case**: This is the **default** Service type. It makes the Service reachable only from *within* the Kubernetes cluster. It's perfect for internal communication, such as a web frontend talking to a backend database.
*   **Analogy**: Think of it as an unlisted phone number that only people inside the same office building can call.

### Example: `ClusterIP`

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
