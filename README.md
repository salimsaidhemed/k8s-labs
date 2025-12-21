# Kubernetes Hands-On Labs (CKA-Focused)

This repository contains a **structured, hands-on lab environment** for mastering Kubernetes concepts through **practice-first exercises**, supported by **custom-built container images** that make Kubernetes behavior *observable and intuitive*.

The labs are designed primarily for:
- **CKA exam preparation**
- Building strong mental models of Kubernetes primitives
- Reproducible local experimentation using kind, k3s, or lightweight clusters
- Understanding rollout behavior, failures, probes, and configuration changes



## Philosophy

This is **not** a theory repository.

Each concept follows the same pattern:
1. **Short explanation** (why it exists)
2. **Lab objective** (what you must achieve)
3. **Minimal manifests**
4. **Verification steps**
5. **Intentional failure scenarios**

Custom container images are used to **visibly demonstrate changes** such as:
- Rolling updates
- Canary deployments
- Readiness / liveness failures
- Configuration vs image changes
- Traffic distribution

If you can *see* it, you understand it.



## Repository Structure

k8s-labs/
  README.md

  docs/                # Notes and explanations
  labs/                # Hands-on exercises
  images/              # Custom lab container images
  scripts/             # Cluster helpers (kind/k3s)
  .github/workflows/   # CI for building & pushing images

### docs/ 
Concept-focused notes aligned with the labs:
Namespaces & contexts
- Pods, Services, DNS
- Deployments, StatefulSets, Jobs
- Networking & Ingress
- Security (RBAC, ServiceAccounts)
- Observability (probes, resources)

These are concise and practical, not textbook-style.

### labs/ 
Each lab is self-contained and follows a predictable structure:
  lab-XX-topic/
  README.md            # Objective & steps
  manifests/           # Kubernetes YAML
  verify/              # How to validate success

Labs are grouped by topic:
- Core primitives
- Workloads
- Networking
- Security
- Observability

### images/ – Custom Lab Containers

This repo includes purpose-built container images hosted on GHCR.

They are intentionally simple and predictable.

**echo-info** : Shows pod identity, version, build SHA, headers
**echo-color** : Visual rollout testing (color-based responses)
**echo-flaky** : Simulates probe failures & unstable apps
**http-tester** : Debug pod for DNS / service testing

All images:
- Expose HTTP on port 8080
- Display build metadata (BUILD_SHA, BUILD_TIME)
- Are rebuilt automatically via GitHub Actions
- Are ideal for deployment and rollout labs

### CI Container Registry
All images are:
- Built via GitHub Actions
- Pushed to GitHub Container Registry (GHCR)
- Tagged with:
    - :latest
	- :sha-<short-sha>

This allows:
- Immutable GitOps-style deployments
- Easy rollback testing
- Clear visibility during rollouts


## Supported Lab Environments

These labs are designed to work on:
- kind (recommended)
- k3s
- Lightweight cloud clusters (VPS-based)

You do not need:
- A managed Kubernetes service
- Helm (unless explicitly stated in a lab)
- External ingress controllers (initial labs)

## Prerequisites
- Basic Linux CLI familiarity
- kubectl
- Docker or Podman
- One local Kubernetes cluster (kind recommended)

Scripts are provided to create and reset clusters quickly.

## How to Use This Repo
1.	Create or start your cluster
2.	Pick a lab from labs/
3.	Read the lab README
4.	Apply manifests manually
5.	Observe behavior
6.	Break things on purpose
7.	Fix them

Repeat until it feels boring — that’s mastery.- 

By completing these labs, you should be comfortable with:
- Kubernetes core resources
- Debugging broken workloads
- Understanding rollout mechanics
- Reading YAML under pressure
- Reasoning about cluster behavior

This repo favors **depth over breadth** — exactly what the CKA rewards

## Roadmap

Planned additions:
- Advanced rollout labs (canary, blue/green)
- NetworkPolicy scenarios
- RBAC troubleshooting labs
- Resource pressure & eviction demos
- Minimal GitOps-style workflows
---
## Disclaimer

This repository is not affiliated with the CNCF or the CKA exam.
It is a personal learning and practice environment designed to build real understanding.