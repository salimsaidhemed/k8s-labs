# LAB 02 — ReplicaSets and Deployments (Self-Healing & Rollouts)

This lab introduces **controllers** and **desired state**, the core mechanisms that make Kubernetes suitable for production workloads.

You will replace unmanaged Pods with **Deployments**, observe **self-healing**, and perform **rolling updates and rollbacks**.

⚠️ **No solutions are provided in this document.**

---

## CKA Objectives Covered

- Define Kubernetes workloads (Pods, ReplicaSet, Deployment)
- Understand self-healing mechanisms
- Perform rolling updates and rollbacks
- Understand desired state reconciliation
- Observe differences between Pods and controllers

---

## Prerequisites

- Completion of **Lab 01**
- A working Kubernetes cluster
- Access to the `echo-info` image
- Namespace from Lab 01 (or a new lab namespace)

---

## Constraints

- Use **YAML manifests only**
- Do **not** use `kubectl run`, `kubectl create deployment`, or generators
- No Helm
- Do not skip steps
- Observe cluster behavior carefully

---

## Exercise 1 — Create a Deployment

### Objective

Create a Deployment that manages the `echo-info` application.

### Requirements

- Deployment must:
  - Run **2 replicas**
  - Use a **label selector**
  - Expose port `8080`
- Pod template labels must match the selector
- Use the same namespace as previous labs

### Validation

- Deployment reports `Available`
- Two Pods are created
- Pod names are different from Lab 01
- ReplicaSet is automatically created

---

## Exercise 2 — Observe Self-Healing

### Objective

Understand how Kubernetes maintains desired state.

### Tasks

- Manually delete **one** Pod created by the Deployment
- Observe:
  - Replica count
  - Pod recreation
  - Events on the Deployment and ReplicaSet

### Validation

- Replica count returns to desired value
- A new Pod appears automatically
- The Deployment remains healthy

### Reflection

- Which component recreated the Pod?
- Why did this not happen in Lab 01?

---

## Exercise 3 — Scale the Deployment

### Objective

Change desired state and observe reconciliation.

### Tasks

- Scale the Deployment to **3 replicas**
- Observe:
  - New Pods being created
  - Pod distribution across nodes (if applicable)

### Validation

- Desired replicas = actual replicas
- All Pods are `Running`

---

## Exercise 4 — Rolling Update (Image Change)

### Objective

Trigger a rolling update using an image change.

### Tasks

- Update the Deployment to use:
  - A different image tag (e.g. a new `sha-*` tag)
- Observe:
  - Pod termination order
  - Pod creation order
  - Old vs new Pods during rollout

### Validation

- Old Pods are gradually replaced
- Application remains available
- New Pods run the updated image

### Reflection

- Why are Pods replaced gradually instead of all at once?
- What guarantees availability during the update?

---

## Exercise 5 — Rollback

### Objective

Undo a bad rollout.

### Tasks

- Roll back the Deployment to the previous version
- Observe:
  - Pod recreation
  - Revision history

### Validation

- Deployment returns to previous image
- Pods reflect the old version
- No manual Pod deletion required

---

## Exercise 6 — Deployment Strategy Awareness

### Objective

Understand rollout strategies conceptually.

### Tasks

- Inspect the Deployment strategy configuration
- Identify:
  - Max unavailable Pods
  - Max surge Pods
- Consider how changing these values would affect availability

### Reflection

- What happens if maxUnavailable is too high?
- What happens if maxSurge is zero?

---

## Exercise 7 — Failure at the Node Level (Conceptual)

### Objective

Reason about high availability.

### Tasks

- Identify where Pods are scheduled
- Consider what happens if a node fails

### Reflection

- What protects the application?
- What does **not** protect the application yet?
- Which Kubernetes primitives are still missing?

---

## Completion Checklist

You should now be able to explain:

- The role of Deployments vs ReplicaSets
- How desired state is enforced
- How self-healing works
- How rolling updates avoid downtime
- Why Pods should not be managed manually

If any concept feels unclear, **do not proceed**.

---

## What Comes Next

**LAB 03 — Services & Stable Networking**
- ClusterIP
- DNS-based discovery
- Decoupling Pods from consumers
- Service selectors and endpoints

This will directly solve the problems observed in Lab 01 and Lab 02.

---