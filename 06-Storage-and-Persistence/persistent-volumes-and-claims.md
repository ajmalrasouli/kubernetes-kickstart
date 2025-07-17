# Providing Persistent Storage with PVs and PVCs

## The Problem: Ephemeral Pods

A container's filesystem is tied to the lifecycle of the container itself. When a container inside a Pod is restarted or when a Pod is deleted, any data written inside that container is lost forever. This is fine for stateless apps, but a disaster for a database.

Kubernetes solves this with a storage model that is inspired by how developers and infrastructure teams work in the real world. It separates the **provisioning** of storage (done by an administrator) from the **consumption** of storage (done by an application developer).

This is achieved using two key Kubernetes objects: `PersistentVolume` and `PersistentVolumeClaim`.

### PersistentVolume (PV)

A **PersistentVolume (PV)** is a piece of storage in the cluster that has been provisioned by an administrator. It is a cluster-level resource, just like a Node. A PV captures the details of the storage implementation, be it a physical hard drive on a node (`hostPath`), an NFS share, or a cloud provider's storage like an AWS EBS volume or a GCP Persistent Disk.

**Analogy**: Think of a PV as a pre-racked server or a pre-configured storage array in a company's data center. The IT administrator sets it up and makes it available for general use.

### PersistentVolumeClaim (PVC)

A **PersistentVolumeClaim (PVC)** is a request for storage by a user or application. The user creating the PVC specifies the required size and the access mode (e.g., can it be mounted by one Pod or by many?). The user doesn't need to know anything about how the storage is actually provided.

**Analogy**: A PVC is like a developer filling out a ticket requesting a server from the IT department. The ticket says, "I need a machine with 2 CPUs and 8GB of RAM." The developer doesn't care which physical machine they get, as long as it meets their requirements.

### How They Work Together: The Binding Process

1.  An administrator creates one or more `PersistentVolumes` and adds them to the cluster's pool of available storage.
2.  A user creates a `PersistentVolumeClaim` requesting a certain amount of storage.
3.  Kubernetes' control plane looks for a PV in the pool that can satisfy the claim's requirements.
4.  If a suitable PV is found, the PVC is **bound** to that PV. The PV is now considered "in use" and cannot be claimed by another PVC.
5.  The application's Pod can then use the PVC as a volume, giving it access to the persistent storage.

## A Practical Example with Minikube

Let's create a PV, claim it with a PVC, and use it in a Pod to see this in action.

### Step 1: Create a PersistentVolume

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
