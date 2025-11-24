# Project 4 — Kubernetes on kind with Kustomize

This project showcases deploying a Dockerized Flask app (`flask-hello`) to a local Kubernetes cluster using **kind** and **Kustomize**. It focuses on basic manifests, overlays for dev/prod, and simple observability using `kubectl` commands and probes.

## Features

- Local Kubernetes cluster via kind
- Kustomize `base` + `overlays` (dev and prod)
- Flask app deployed as a Deployment + Service
- Readiness and liveness probes
- Basic observability with `kubectl get/describe/logs`

## Structure

```text
04-kubernetes-kind/
  k8s/
    base/
      deployment.yaml
      service.yaml
      kustomization.yaml
    overlays/
      dev/kustomization.yaml
      prod/kustomization.yaml
  kind-config.yaml
  README.md
