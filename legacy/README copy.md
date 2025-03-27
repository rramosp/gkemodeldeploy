
## Instructions

### Prerequisites

- Create or select a project
- Enable Kubernetes Engine API
- Create a VPC named 'default', if it does not exist.  
- In IAM -> Organizational policies edit the policy `constraints/compute.vmExternalIpAccess` and add a new rule **Allow all**
- Create a default service account `<project_number>-compute@developer.gserviceaccount.com` with permissions `Kubernetes Engine Cluster Admin` and `Monitoring Admin` if it does not exist, or does not have such permissions.
- Enable GKE Enterprise
**NOTE**: These polocies and configurations could be set more restrictive according to particular needs.

### STEP 1: Deploy cluster

https://cloud.google.com/kubernetes-engine/docs/tutorials/serve-gemma-gpu-tgi

summary of key commands for step 1 (included in the link above):

```
  gcloud container clusters create-auto gemma2 --project=gemma-test-deployment --region=us-central1 --release-channel=rapid



  gcloud container clusters get-credentials gemma2     --location=us-central1
  kubectl create secret generic hf-secret --from-literal=hf_api_token=<YOUR_HF_TOKEN>
  kubectl apply -f deployment.yaml
```
    
check deployment is finished
```
 kubectl get pods
 kubectl port-forward pod/<POD_ID>> 8000:8000
 python test.py
```

also, open localhost:8000/metrics to check metrics are being gathered

tell GCP Managed Prometeus what pods to look for
kubectl apply -f monitor.yaml

inspect what api services are running
    k get apiservices




### STEP 2: Deploy gradio UI


```
 kubectl apply -f gradio.yaml
 kubectl port-forward service/gradio 8080:8080
```

open browser at localhost:8080

### STEP 3: Install autoscaling

helm install prometheus-adapter prometheus-community/prometheus-adapter -n default

helm install prometheus prometheus-community/prometheus -n default


### STEP 3: Enable TGI/LLM dashboard

https://cloud.google.com/stackdriver/docs/managed-prometheus/exporters/tgi

summary of key commands for step 3:

```
 kubectl apply -f tgi-monitor.yaml
 kubectl apply -f default-sa-role.yaml
 kubectl apply -f default-sa-rolebinding.yaml
```

check metrics are being collected openning  http://localhost:8000/metrics once you forward port 8000 from any pod. Replace <ANY_POD> with the pod id you get from `kubectl get pods`


```
kubectl port-forward <ANY_POD> 8000:8000
```


then make a few request (curl or gradio), go to https://console.cloud.google.com/monitoring/dashboards and check some doashboards, in particular:

- GKE, for a global overview of the cluster
- NVIDIA GPU Monitoring
- TGI Prometheus overview, for LLM specific metrics

 https://console.cloud.google.com/monitoring/dashboards 


## STEP 4: Scale manually

set the total number of pods you want

    kubectl scale deployment tgi-gemma-deployment --replicas 3

check their status 



manually ssh and inspect their load

```
 > kubectl get pods

 NAME                                    READY   STATUS    RESTARTS   AGE
 gradio-594969d66b-7jbsz                 1/1     Running   0          9h
 tgi-gemma-deployment-7d9f9dcd9d-kx5pp   1/1     Running   0          10h
 tgi-gemma-deployment-7d9f9dcd9d-xjg2x   0/1     Pending   0          2s


 >  kubectl exec -it tgi-gemma-deployment-7d9f9dcd9d-kx5pp -- /bin/bash

 root@tgi-gemma-deployment-7d9f9dcd9d-kx5pp:/usr/src# nvidia-smi -l 1
 ...
 root@tgi-gemma-deployment-7d9f9dcd9d-kx5pp:/usr/src# CTRL-C
 root@tgi-gemma-deployment-7d9f9dcd9d-kx5pp:/usr/src# exit
```

**Commands
to add monitoring
create default service account: projectnumber-...computeengine....

k apply default*role*.yaml

# for debugging
k apply -f enable-target-status.yaml 



**Dashboards

https://console.cloud.google.com/monitoring/metrics-explorer
