# LAB 01 — Pods, Labels, and Basic Connectivity

## CKA objectives covered (foundational layer):

- Define Kubernetes workloads (Pods)
- Understand connectivity between Pods
- Understand primitives used for self-healing (intro)
- Prepare ground for Services, Deployments, ConfigMaps

## Scenario

You are deploying a very small internal service inside a Kubernetes cluster.
At this stage, you are not concerned with availability, only with understanding:
- How Pods are created
- How they are identified
- How they communicate
- What breaks when things are done “the naive way”

You will use the custom lab image:

```text
echo-info => ghcr.io/salimsaidhemed/k8s-labs/echo-info:latest
```

## Constraints (important)

- Work in a dedicated namespace
- Do not use Deployments yet
- Do not create Services yet
- Do not use kubectl shortcuts (run, expose)
- Everything must be explicit YAML

This lab is intentionally “manual”.

## Exercise 1 — Create a Namespace

### Objective

Create a namespace dedicated to labs.

### Requirements

- Namespace Must Clearly Indicate:
    - It is a lab
    - It is safe to delete

### Validation

- You can list the namespace
- You can set it as the current Context

## Exercise 2 — Create a Single Pod

### Objective

Run a single Pod using the echo-info image.

### Requirements
- Pod name must be explicit and meaningful
    - Listen on port 8080
    - Have a label identifying its role
- No restart tricks
- No probes yet

### Validation
- Pod reaches Running
- You can retrieve logs
- You can describe the Pod and understand:
    - Node placement
    - IP assignment
    - Labels

## Exercise 3 — Inspect Pod Identity

### Objective

Understand what makes a Pod unique inside the cluster.

### Tasks
- Exec into the Pod
- Identify:
	- Hostname
	- Pod IP
- Compare:
	- Pod name
	- Hostname
	- IP

Reflection questions (do not answer yet)
- Is hostname guaranteed to match Pod name?
- Is Pod IP stable?

## Exercise 4 — Test Intra-Cluster Connectivity (Without Services)

### Objective

Confirm that Pods can communicate directly.

### Tasks
1. Create a temporary debug Pod using the http-tester image
2. From inside that Pod:
    - Reach the echo-info Pod using its Pod IP
    - Observe the response

### Validation
- You receive a valid HTTP response
- Response shows:
	- Hostname
	- Build information
	- Headers

### Reflection questions
- What breaks if the Pod restarts?
- What breaks if the Pod is rescheduled?

## Exercise 5 — Labels and Selection

## Objective

Understand why labels matter before Services and Deployments exist.

### Tasks
- Add at least two labels to the Pod:
    - One identifying the app
    - One identifying the environment
- Verify labels using:
    - Pod listing
    - Label selectors

### Reflection questions
- Why does Kubernetes rely on labels instead of names?
- How would this scale to multiple Pods?

## Exercise 6 — Manual Failure and “Self-Healing” (or Lack Thereof)

### Objective

Observe what happens without controllers.

### Tasks
- Delete the Pod
- Observe cluster state

### Validation
- Confirm whether the Pod comes back
- Understand why it does or does not

### Reflection questions
- What Kubernetes primitive is missing?
- Why is this unacceptable for production?

## Lab Completion Checklist

You should now be able to confidently explain:
- What a Pod is (and is not)
- Why Pods are ephemeral
- How Pods get IPs
- Why Pod IPs are not a stable interface
- Why labels are foundational to Kubernetes design

If anything here feels fuzzy — do not move on.

## What Comes Next (do not start yet)

LAB 02 — ReplicaSets and Deployments
- Why controllers exist
- ReplicaSet vs Deployment
- Declarative state
- Self-healing in action
- Rolling updates (first exposure)

We will:
- Replace manual Pods
- Introduce controlled reconciliation
- Make failures boring
