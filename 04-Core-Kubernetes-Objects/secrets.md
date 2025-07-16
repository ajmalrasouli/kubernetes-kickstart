
---

### `04-Core-Kubernetes-Objects/secrets.md`

```markdown
# Managing Sensitive Data with Secrets

## What is a Secret?

Just like ConfigMaps, **Secrets** are Kubernetes objects that let you store and manage data to be used by your Pods. So what's the difference? Secrets are intended exclusively for sensitive information, such as:

*   Passwords
*   OAuth tokens and API keys
*   TLS certificates
*   SSH keys

While ConfigMaps store data in plain text, Kubernetes stores Secrets in base64 encoding. **It's very important to understand that base64 is an encoding, not an encryption.** It is trivial to decode. The true value of Secrets comes from how Kubernetes treats them:

*   **Granular Access Control**: You can use Kubernetes RBAC (Role-Based Access Control) to strictly control which users and service accounts can read a particular Secret.
*   **System-level Safeguards**: Kubernetes avoids writing Secret data to disk where possible (e.g., by using in-memory filesystems) and does not include it in verbose log outputs.
*   **Integration with External Secret Stores**: In production, Secrets can be integrated with external, more secure vaults like HashiCorp Vault or AWS Secrets Manager.

**Rule of thumb: If the data is sensitive, use a Secret. If it's not, use a ConfigMap.**

## Creating a Secret

You can create Secrets in a similar way to ConfigMaps.

### Method 1: From a File

Let's say you have two files, `username.txt` containing `admin` and `password.txt` containing `S3cr3tP@ssw0rd!`.

```bash
# Create the files first
echo -n 'admin' > ./username.txt
echo -n 'S3cr3tP@ssw0rd!' > ./password.txt

# Create the secret from these files
kubectl create secret generic my-db-credentials --from-file=./username.txt --from-file=./password.txt
