
---

### `04-Core-Kubernetes-Objects/configmaps.md`

```markdown
# Managing Configuration with ConfigMaps

## The Problem: Configuration in Container Images

A common mistake when starting with containers is to bake configuration files directly into the container image. This is inflexible. If you want to change a single configuration value (like a database URL or a feature flag), you have to rebuild the entire image, push it to a registry, and redeploy.

Kubernetes provides a much better solution: **ConfigMaps**.

## What is a ConfigMap?

A **ConfigMap** is a Kubernetes object used to store non-confidential configuration data in a key-value format. This data can then be consumed by your Pods, decoupling the configuration from the application code and container image.

This allows you to:
*   Use the same container image across different environments (dev, staging, prod) with different configurations.
*   Update application configuration without rebuilding and redeploying your application.
*   Let different teams manage configuration separately from application developers.

> **Important**: ConfigMaps are for non-sensitive data only. They store data in plain text. For sensitive data like passwords, API keys, and certificates, you must use **Secrets**.

## Creating a ConfigMap

You can create a ConfigMap from the command line or from a YAML file.

### Method 1: From a File

Let's say you have a configuration file named `app-config.properties`:

```properties
# app-config.properties
APP_COLOR=blue
APP_MODE=production
