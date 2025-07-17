# Module 6: Storage and Persistence

So far, all the applications we have deployed have been **stateless**. This means they don't need to save any unique data between restarts. If a Pod running a stateless web server dies, Kubernetes creates a new one, and it's a perfect, clean replacement.

But what about applications like databases, message queues, or user-generated content platforms? These applications are **stateful** and require their data to be preserved even if their Pod is deleted or moved to another node. This is one of the most critical challenges in container orchestration.

This module introduces the Kubernetes storage architecture, a powerful system that decouples storage from the Pod lifecycle.

## Key Topics Covered

- **The Problem with Pod Storage**: Understanding why the default storage inside a container is ephemeral and unsuitable for stateful applications.
- **PersistentVolumes (PVs)**: Learn about `PersistentVolumes` as administrator-provisioned blocks of storage available to the cluster.
- **PersistentVolumeClaims (PVCs)**: Understand how applications request storage using `PersistentVolumeClaims` without needing to know the underlying storage details.
- **StorageClasses and Dynamic Provisioning**: Discover the modern, automated way to manage storage where volumes are created on-demand when a claim is made.

By the end of this module, you'll know how to provide stable, persistent storage to your stateful applications, completing your foundational knowledge of Kubernetes.

## 1. Providing Persistent Storage with PVs and PVCs

### 1.1 The Problem: Ephemeral Pods

A container's filesystem is tied to the lifecycle of the container itself. When a container inside a Pod is restarted or when a Pod is deleted, any data written inside that container is lost forever. This is fine for stateless apps, but a disaster for a database.

Kubernetes solves this with a storage model that is inspired by how developers and infrastructure teams work in the real world. It separates the **provisioning** of storage (done by an administrator) from the **consumption** of storage (done by an application developer).

This is achieved using two key Kubernetes objects: `PersistentVolume` and `PersistentVolumeClaim`.

### 1.2 PersistentVolume (PV)

A **PersistentVolume (PV)** is a piece of storage in the cluster that has been provisioned by an administrator. It is a cluster-level resource, just like a Node. A PV captures the details of the storage implementation, be it a physical hard drive on a node (`hostPath`), an NFS share, or a cloud provider's storage like an AWS EBS volume or a GCP Persistent Disk.

**Analogy**: Think of a PV as a pre-racked server or a pre-configured storage array in a company's data center. The IT administrator sets it up and makes it available for general use.

### 1.3 PersistentVolumeClaim (PVC)

A **PersistentVolumeClaim (PVC)** is a request for storage by a user or application. The user creating the PVC specifies the required size and the access mode (e.g., can it be mounted by one Pod or by many?). The user doesn't need to know anything about how the storage is actually provided.

**Analogy**: A PVC is like a developer filling out a ticket requesting a server from the IT department. The ticket says, "I need a machine with 2 CPUs and 8GB of RAM." The developer doesn't care which physical machine they get, as long as it meets their requirements.

### 1.4 How They Work Together: The Binding Process

1. An administrator creates one or more `PersistentVolumes` and adds them to the cluster's pool of available storage.
2. A user creates a `PersistentVolumeClaim` requesting a certain amount of storage.
3. Kubernetes' control plane looks for a PV in the pool that can satisfy the claim's requirements.
4. If a suitable PV is found, the PVC is **bound** to that PV. The PV is now considered "in use" and cannot be claimed by another PVC.
5. The application's Pod can then use the PVC as a volume, giving it access to the persistent storage.

### 1.5 A Practical Example with Minikube

Let's create a PV, claim it with a PVC, and use it in a Pod to see this in action.

#### Step 1: Create a PersistentVolume

For Minikube, the easiest type of PV to create is a `hostPath` volume. This simply uses a directory on the Minikube node's own filesystem.

Create a file named `my-pv.yaml`:

```yaml
# my-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-hostpath-pv
spec:
  capacity:
    storage: 1Gi # Size of the volume
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce # Can be mounted as read-write by a single Node
  hostPath:
    path: "/mnt/data" # A path inside the Minikube VM
```

- `accessModes: ReadWriteOnce` means the volume can be mounted by a single node at a time. This is common for block storage.
- `hostPath.path` specifies the directory on the host node that backs this volume.

Apply it:
```bash
kubectl apply -f my-pv.yaml
```

#### Step 2: Create a PersistentVolumeClaim

Now, let's create a PVC that requests storage and is compatible with the PV we just created.

Create a file named `my-pvc.yaml`:

```yaml
# my-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi # Request 500 Megabytes
```

Even though we requested 500Mi and the PV has 1Gi, Kubernetes will bind them because the PV is large enough to satisfy the claim.

Apply it:
```bash
kubectl apply -f my-pvc.yaml
```

Now, check the status of your PV and PVC. You'll see that their status is Bound.

```bash
# Check the PV, STATUS should be Bound
kubectl get pv

# Check the PVC, STATUS should be Bound
kubectl get pvc
```

#### Step 3: Use the PVC in a Pod

Finally, let's create a Pod that mounts this volume and writes a file to it.

Create `persistent-pod.yaml`:

```yaml
# persistent-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: persistent-storage-pod
spec:
  volumes:
    - name: my-storage
      persistentVolumeClaim:
        claimName: my-pvc # Reference the PVC we created
  containers:
    - name: nginx
      image: nginx
      ports:
        - containerPort: 80
      volumeMounts:
        - mountPath: "/usr/share/nginx/html" # Mount the persistent storage here
          name: my-storage
```

Here, under volumes, we are not defining a hostPath or emptyDir. We are referencing our PersistentVolumeClaim by name.

Apply it:
```bash
kubectl apply -f persistent-pod.yaml
```

#### Step 4: Test Persistence

Let's write a file to our persistent storage from within the Pod.

```bash
# Exec into the pod and create a file in the mounted directory
kubectl exec -it persistent-storage-pod -- /bin/sh -c "echo 'My data is safe!' > /usr/share/nginx/html/index.html"
```

Now, the ultimate test. Delete the Pod:

```bash
kubectl delete pod persistent-storage-pod
```

The Pod is gone, but what about our PV and PVC? They are still there, and the data is safe on the volume.

```bash
kubectl get pv,pvc
```

Now, re-apply the Pod manifest:
```bash
kubectl apply -f persistent-pod.yaml
```

A new Pod will be created. Let's check if our data is still there.

```bash
# Exec into the *new* pod and read the file
kubectl exec -it persistent-storage-pod -- cat /usr/share/nginx/html/index.html
```

You should see the output "My data is safe!". This proves that the data persisted even after the Pod was completely deleted and recreated.

## 2. Dynamic Provisioning with StorageClasses

Manually creating `PersistentVolumes` works for learning, but it doesn't scale. In a large, dynamic environment, you don't want an administrator to have to pre-provision a PV for every storage request.

The preferred method for managing storage in Kubernetes is **dynamic provisioning**, which is enabled by the `StorageClass` object.

### 2.1 What is a StorageClass?

A **StorageClass** provides a way for administrators to define different "classes" or "types" of storage they offer. A class might be defined by its quality of service (e.g., `fast-ssd` vs `slow-hdd`), its backup policies, or by custom parameters specific to the storage system.

When a `StorageClass` is configured, administrators no longer need to create `PersistentVolumes` manually. Instead, a PV is **automatically provisioned** when a `PersistentVolumeClaim` requests that specific class.

### 2.2 How It Works

1. The administrator defines one or more `StorageClass` objects. For a cloud provider like GCP, there might be a `standard` class and a `premium-ssd` class. Minikube comes with a default `standard` StorageClass.
2. A user creates a `PersistentVolumeClaim` and, instead of waiting for a pre-existing PV, they specify the `storageClassName` they want to use.
3. The StorageClass's provisioner sees the PVC, automatically creates a suitable `PersistentVolume` in the underlying infrastructure (e.g., creates a new EBS volume in AWS), and binds the new PV to the PVC.
4. The user's Pod can then use the PVC as before, completely unaware of the dynamic provisioning that happened behind the scenes.

### 2.3 Example of a PVC with a StorageClass

You can check the available StorageClasses in your Minikube cluster:
```bash
kubectl get storageclass
```

You will see one named `standard`.

Here is how you would modify the PVC from the previous lesson to use this `StorageClass` for dynamic provisioning.

Create a file named `dynamic-pvc.yaml`:

```yaml
# dynamic-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-dynamic-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard # We explicitly request the 'standard' class
  resources:
    requests:
      storage: 200Mi
```

If you apply this manifest:
```bash
kubectl apply -f dynamic-pvc.yaml
```

You will see something amazing. A new PVC is created, and almost immediately, a brand new PV is automatically created and bound to it!

```bash
kubectl get pvc,pv
```

This dynamic provisioning is the standard way to handle storage in modern Kubernetes clusters, especially in cloud environments. It provides scalability and abstracts away the underlying infrastructure, allowing developers to request the storage they need on demand.

## Summary

In this module, you've learned about the essential components of Kubernetes storage and persistence:

1. **The Problem**: Container filesystems are ephemeral, making them unsuitable for stateful applications that need to persist data.

2. **PersistentVolumes (PVs)**: Administrator-provisioned storage resources that exist independently of Pod lifecycles, providing a stable storage foundation.

3. **PersistentVolumeClaims (PVCs)**: User requests for storage that abstract away the underlying storage implementation details, allowing applications to request storage without knowing how it's provided.

4. **The Binding Process**: The mechanism by which Kubernetes matches PVCs to suitable PVs, creating a connection between storage requests and available storage resources.

5. **StorageClasses**: A modern approach to storage management that enables dynamic provisioning, automatically creating PVs when PVCs are made, eliminating the need for manual PV pre-provisioning.

These concepts work together to provide a robust, scalable storage solution that supports stateful applications in Kubernetes. By decoupling storage from Pod lifecycles and enabling dynamic provisioning, Kubernetes provides the foundation needed to run databases, message queues, and other stateful workloads reliably in a containerized environment.

Module 6 completes your foundational understanding of Kubernetes, giving you the knowledge to deploy, manage, and persist data for both stateless and stateful applications in a production-ready manner.
