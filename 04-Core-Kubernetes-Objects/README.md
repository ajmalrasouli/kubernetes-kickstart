# 🔐 Module 4: Core Kubernetes Objects

Congratulations on deploying your first application! You now understand the workflow of getting an application running on Kubernetes. However, in real-world scenarios, applications have more complex needs than just running code. They need configuration data, and you need ways to organize your cluster resources.

This module dives deeper into some of the most essential Kubernetes objects that address these needs. You will learn how to isolate resources, manage non-sensitive configuration data, and handle sensitive information like passwords and API keys securely.

## Key Topics Covered

*   **Namespaces**: Learn how to use Namespaces as virtual partitions to organize your cluster resources for different projects, teams, or environments.
*   **ConfigMaps**: Understand how to use ConfigMaps to decouple configuration data from your application's container image, allowing for greater flexibility and easier updates.
*   **Secrets**: Discover the importance of Secrets for managing sensitive data and learn how they differ from ConfigMaps to provide an extra layer of security.

Mastering these objects is a key step toward managing production-grade applications on Kubernetes.


Welcome to **Module 4** – the next step in your Kubernetes journey!

Now that you've successfully deployed your first app, it's time to go beyond "Hello World" and explore tools used by professionals to manage Kubernetes at scale. In this module, you'll learn how to organize, configure, and secure your applications.

---

## 📦 Key Topics Covered

- **Namespaces** – Virtual environments to organize your cluster
- **ConfigMaps** – Externalize your app’s configuration
- **Secrets** – Securely handle sensitive data

---

## 📂 File Index

- [`README.md`](#) – This overview file
- [`namespaces.md`](#organizing-your-cluster-with-namespaces)
- [`configmaps.md`](#managing-configuration-with-configmaps)
- [`secrets.md`](#managing-sensitive-data-with-secrets)

---

## 🗂 Organizing Your Cluster with Namespaces

Namespaces allow logical separation of resources in a single cluster. They are helpful for:

- Organizing projects or teams
- Avoiding naming conflicts
- Applying RBAC and resource limits

### Example:

```bash
kubectl create namespace dev
kubectl create namespace prod
```

View all namespaces:

```bash
kubectl get namespaces
```

Deploy into a namespace:

```bash
kubectl apply -f simple-app.yaml -n dev
```

Cleanup:

```bash
kubectl delete namespace dev
```

---

## ⚙️ Managing Configuration with ConfigMaps

Use ConfigMaps to inject configuration into Pods without hardcoding them into images.

### Create a ConfigMap:

```bash
kubectl create configmap my-app-config --from-literal=APP_COLOR=blue --from-literal=APP_MODE=production
```

### Use it in a Pod:

```yaml
env:
  - name: APP_COLOR
    valueFrom:
      configMapKeyRef:
        name: my-app-config
        key: APP_COLOR
```

Or mount it as a volume:

```yaml
volumes:
  - name: config-volume
    configMap:
      name: my-app-config
```

---

## 🔒 Managing Sensitive Data with Secrets

Secrets are like ConfigMaps, but for **confidential data** (e.g. passwords, API keys).

### Create a Secret:

```bash
kubectl create secret generic my-db-credentials \
  --from-literal=username=admin \
  --from-literal=password=S3cr3tP@ss
```

### Use in a Pod:

```yaml
volumes:
  - name: secret-volume
    secret:
      secretName: my-db-credentials
```

Mount as files (read-only):

```yaml
volumeMounts:
  - name: secret-volume
    mountPath: "/etc/secrets"
    readOnly: true
```

View Secret data (base64 encoded):

```bash
kubectl get secret my-db-credentials -o yaml
```

---

## 🎓 Summary

| Concept     | Purpose                                         |
|-------------|-------------------------------------------------|
| Namespace   | Organize and isolate resources                 |
| ConfigMap   | Inject non-sensitive config into containers     |
| Secret      | Securely provide sensitive values to workloads |

These objects are foundational for **production-ready Kubernetes** environments.

➡️ Next, we’ll dive into managing application lifecycle, rolling updates, and monitoring.

Happy K8s-ing! 🐳
