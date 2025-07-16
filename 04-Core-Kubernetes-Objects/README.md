# Module 4: Core Kubernetes Objects

Congratulations on deploying your first application! You now understand the workflow of getting an application running on Kubernetes. However, in real-world scenarios, applications have more complex needs than just running code. They need configuration data, and you need ways to organize your cluster resources.

This module dives deeper into some of the most essential Kubernetes objects that address these needs. You will learn how to isolate resources, manage non-sensitive configuration data, and handle sensitive information like passwords and API keys securely.

## Key Topics Covered

*   **Namespaces**: Learn how to use Namespaces as virtual partitions to organize your cluster resources for different projects, teams, or environments.
*   **ConfigMaps**: Understand how to use ConfigMaps to decouple configuration data from your application's container image, allowing for greater flexibility and easier updates.
*   **Secrets**: Discover the importance of Secrets for managing sensitive data and learn how they differ from ConfigMaps to provide an extra layer of security.

Mastering these objects is a key step toward managing production-grade applications on Kubernetes.
