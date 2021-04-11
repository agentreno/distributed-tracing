## Prometheus setup in Minikube

### Description

A full setup of Prometheus (via the Operator) and Grafana with node exporter,
alertmanager, adapter for metrics API and kube-state-metrics. The idea is to
learn more about Prometheus and metrics observability as well as distributed
tracing.

## Setup

As per the instructions in https://github.com/prometheus-operator/kube-prometheus

1. `minikube delete && minikube start --kubernetes-version=v1.20.0 --memory=6g --bootstrapper=kubeadm --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook --extra-config=scheduler.address=0.0.0.0 --extra-config=controller-manager.address=0.0.0.0 && minikube addons disable metrics-server`

2. `git clone https://github.com/prometheus-operator/kube-prometheus`

3. 
```
cd kube-prometheus
kubectl create -f manifests/setup
until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
kubectl create -f manifests/
```

4. When finished:

`kubectl delete --ignore-not-found=true -f manifests/ -f manifests/setup`
