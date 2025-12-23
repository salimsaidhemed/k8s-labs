# Lab 01 — Pods, Labels, and Basic Connectivity (Solution)

This document records the **reference solution** for **Lab 01**.  
It is intended for **review and reinforcement**, not first-time learning.

---

## Objectives Covered

- Define Kubernetes workloads (**Pods**)
- Understand Pod identity and ephemerality
- Understand basic Pod-to-Pod connectivity
- Understand why controllers and Services exist
- Establish mental models required for Deployments and Services

---

## Exercise 1 — Namespace

### Implementation

A dedicated namespace was created to isolate lab resources and clearly mark them as disposable.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: lab01-ns
  labels:
    purpose: lab01
    safeToDelete: "true"
```
### Context Handling

Namespaces are not automatically selected after creation.
To avoid repeatedly specifying -n, the current context can be updated:

```bash
kubectl config set-context --current --namespace=lab01-ns
```
This modifies the kubeconfig and reduces error risk during labs and exams.

-

## Exercise 2 — Single Pod Definition

### Implementation

A single Pod was created explicitly using YAML (no generators or shortcuts).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: lab01-pod
  namespace: lab01-ns
  labels:
    app: lab01-app
    env: lab
spec:
  containers:
    - name: echo-info
      image: ghcr.io/salimsaidhemed/k8s-labs/echo-info:latest
      ports:
        - containerPort: 8080
```

### Observation

- 	The Pod reaches Running
- 	Logs are accessible
-   kubectl describe pod reveals:
	- 	Assigned node
	- 	Pod IP
	- 	Labels

This demonstrates that a Pod is a single, unmanaged workload unit.

## Exercise 3 — Pod Identity

## Findings

From inside the Pod:
- Hostname equals Pod name
- Pod IP matches kubectl describe output

Key conclusions:
- Pod IP is ephemeral
    - Changes if the Pod is recreated
- Hostname defaults to Pod name
    - Stable only as long as the Pod name remains unchanged
    - Controllers typically generate new Pod names

This reinforces why Pods are not suitable as stable endpoint.

--

## Exercise 4 — Intra-Cluster Connectivity (Without Services)

### Debug Pod

A temporary debug Pod was used to test direct Pod connectivity.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: http-tester
  namespace: lab01-ns
  labels:
    app: http-tester
    env: lab
spec:
  containers:
    - name: http-tester
      image: ghcr.io/salimsaidhemed/k8s-labs/http-tester:latest
```
### Connectivity Test

From the debug Pod:

```bash
curl <pod-ip>:8080
```
### Observations
- Direct Pod-to-Pod communication works
- Response includes hostname and build metadata
- Connectivity breaks immediately if the Pod is deleted or rescheduled

This demonstrates:
- Pod IPs are not stable
- Services are required for durable connectivity
- DNS without Services is insufficient for real applications

## Exercise 5 — Labels and Selectors

### Verification

Pods were queried using label selectors:

```bash
kubectl get pods --selector app=lab01-app
```

### Key Takeaways
- Labels are the primary grouping mechanism in Kubernetes
- Names are human-oriented; labels are system-oriented
- Services, Deployments, NetworkPolicies, and HPAs all rely on selectors

Labels are foundational to Kubernetes design.

## Exercise 6 — Failure and Self-Healing

### Test

The Pod was manually deleted:

```bash
kubectl delete pod lab01-pod
```

### Result
- Pod was not recreated
- Application became unavailable

### Explanation
- No controller was managing desired state
- Pods do not self-heal
- No replicas existed
- No reconciliation loop was present

### Why This Is Unacceptable in Production
- Single point of failure
- No automatic recovery
- No scaling
- No upgrade strategy

This directly motivates the use of:
- ReplicaSets
- Deployments


## Final Conclusions

After completing this lab, the following concepts should be fully internalized:
- Pods are ephemeral
- Pod IPs are not stable
- Direct Pod addressing does not scale
- Labels enable grouping and selection
- Controllers are required for:
    - Self-healing
    - Scaling
    - Declarative desired state
