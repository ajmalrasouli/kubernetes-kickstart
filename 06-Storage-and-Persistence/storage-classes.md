
---

### `06-Storage-and-Persistence/storage-classes.md`

```markdown
# Dynamic Provisioning with StorageClasses

Manually creating `PersistentVolumes` works for learning, but it doesn't scale. In a large, dynamic environment, you don't want an administrator to have to pre-provision a PV for every storage request.

The preferred method for managing storage in Kubernetes is **dynamic provisioning**, which is enabled by the `StorageClass` object.

## What is a StorageClass?

A **StorageClass** provides a way for administrators to define different "classes" or "types" of storage they offer. A class might be defined by its quality of service (e.g., `fast-ssd` vs `slow-hdd`), its backup policies, or by custom parameters specific to the storage system.

When a `StorageClass` is configured, administrators no longer need to create `PersistentVolumes` manually. Instead, a PV is **automatically provisioned** when a `PersistentVolumeClaim` requests that specific class.

## How It Works

1.  The administrator defines one or more `StorageClass` objects. For a cloud provider like GCP, there might be a `standard` class and a `premium-ssd` class. Minikube comes with a default `standard` StorageClass.
2.  A user creates a `PersistentVolumeClaim` and, instead of waiting for a pre-existing PV, they specify the `storageClassName` they want to use.
3.  The StorageClass's provisioner sees the PVC, automatically creates a suitable `PersistentVolume` in the underlying infrastructure (e.g., creates a new EBS volume in AWS), and binds the new PV to the PVC.
4.  The user's Pod can then use the PVC as before, completely unaware of the dynamic provisioning that happened behind the scenes.

## Example of a PVC with a StorageClass

You can check the available StorageClasses in your Minikube cluster:
`kubectl get storageclass`
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
