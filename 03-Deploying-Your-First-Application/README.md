# Module 3: Deploying Your First Application

This is the moment you've been waiting for! In this module, we will take a simple, pre-built container image and deploy it to your local Minikube cluster. You will write your first Kubernetes manifest file and learn how to use `kubectl` to bring your application to life.

By the end of this module, you will have a tangible result: a running web server accessible from your own machine, all managed by Kubernetes.

## Key Topics Covered

*   **Understanding the Goal**: We'll start by looking at the simple web application we're going to deploy.
*   **Kubernetes Manifests (YAML)**: An introduction to the YAML file format, which is how you declare the "desired state" of your application to Kubernetes.
*   **Creating a Deployment**: You will write a Deployment manifest to tell Kubernetes to run your application.
*   **Creating a Service**: You will then write a Service manifest to expose your application and make it accessible over the network.
*   **Applying and Verifying**: You will learn the `kubectl apply` command to send your manifests to the cluster and other commands to verify that your application is running correctly.

Let's start deploying!
