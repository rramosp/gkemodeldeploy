
## Instructions

### Prerequisites

- Create or select a project
- Enable Kubernetes Engine API
- Create a VPC named 'default', if it does not exist.  
- In IAM -> Organizational policies edit the policy `constraints/compute.vmExternalIpAccess` and add a new rule **Allow all**
- Create a default service account `<project_number>-compute@developer.gserviceaccount.com` with permissions `Kubernetes Engine Cluster Admin` and `Monitoring Admin` if it does not exist, or does not have such permissions.
- Accept licence of the model you want to deploy in Hugging Face and get an access token.
- Enable GKE Enterprise.
- Install locust load generator (`pip install locust`)
**NOTE**: These policies and configurations could be set more restrictive according to particular needs.


### Based on

https://cloud.google.com/kubernetes-engine/docs/tutorials/serve-gemma-gpu-tgi
https://cloud.google.com/kubernetes-engine/docs/tutorials/autoscaling-metrics#custom-metric
https://github.com/GoogleCloudPlatform/k8s-stackdriver/blob/master/custom-metrics-stackdriver-adapter/README.md


## Steps


### 1. Deploy cluster

    > gcloud container clusters create-auto gemma2v3 --project=gemma-test-deployment --region=us-central1 --release-channel=rapid
    > gcloud container clusters get-credentials gemma2v3 --location=us-central1
    > kubectl create secret generic hf-secret --from-literal=hf_api_token=<YOUR_HF_TOKEN>

**sanity checks**

    > gcloud container clusters describe gemma2v3 --zone=us-central1


### 2. Deploy model  

    > alias k=kubeflow
    > k apply -f manifests/01_deployment.yaml
    > k apply -f manifests/02_perrmissions.yaml
    > k apply -f manifests/03_loadbalancer.yaml
    > k apply -f manifests/04_monitor.yaml 

**sanity checks**

After a few minutes you should see at least one pod on one node up and running

    > k get deployments,pods,nodes

    NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/tgi-gemma-deployment   1/1     1            1           26m

    NAME                                        READY   STATUS    RESTARTS   AGE
    pod/tgi-gemma-deployment-7d9f9dcd9d-t4rxv   1/1     Running   0          26m

    NAME                                           STATUS   ROLES    AGE   VERSION
    node/gk3-gemma2v3-nap-1bwi7nsq-ce6f4ef9-bdpr   Ready    <none>   31m   v1.32.2-gke.1182001
    node/gk3-gemma2v3-nap-1wr2jc8m-01e7233c-7btk   Ready    <none>   25m   v1.32.2-gke.1182001

Check pod is working (use the pod id you got above). You should get some text about WW2. It might take a few extra mins since the pod is running to start up the model server.

    > k port-forward pod/tgi-gemma-deployment-7d9f9dcd9d-t4rxv 8000:8000
    > python src/test.py http://localhost:8000

Check pod is keeping metrics. You should see a list of many metrics.

    > curl http://localhost:8000/metrics

Check pod monitoring is scraping the metrics. You should see some information about a recent last scrape.

    > k describe podmonitoring

Check external access is working. Use the external IP from the following command

    > k get services 

    NAME            TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)          AGE
    gemma-service   LoadBalancer   34.118.229.199   35.224.145.17   8000:31481/TCP   46m
    kubernetes      ClusterIP      34.118.224.1     <none>          443/TCP          62m

    > python src/test.py http://35.224.145.17:8000

Generate a load and observe model serving performance

- edit `src/locust.conf`, set your external IP above and `users=50` (or some number you want to test)
- run 

    > locust --config src/locust.conf

- open http://localhost:8089 in a browser and click on the charts tab. You should see requests per second and latency (response times)


### 3. Deploy autoscaling

    > gcloud iam service-accounts add-iam-policy-binding --role \
         roles/iam.workloadIdentityUser --member \
         "serviceAccount:gemma-test-deployment.svc.id.goog[custom-metrics/custom-metrics-stackdriver-adapter]" \
         883536042426-compute@developer.gserviceaccount.com

    > kubectl annotate serviceaccount --namespace custom-metrics \
         custom-metrics-stackdriver-adapter \
         iam.gke.io/gcp-service-account=883536042426-compute@developer.gserviceaccount.com


    kubeflow apply -f 08_hpa.yaml





------

### STEP 1: Deploy cluster

https://cloud.google.com/kubernetes-engine/docs/tutorials/serve-gemma-gpu-tgi

summary of key commands for step 1 (included in the link above):

```
  gcloud container clusters create-auto gemma2 --project=gemma-test-deployment --region=us-central1 --release-channel=rapid



  gcloud container clusters get-credentials gemma2     --location=us-central1
  kubectl create secret generic hf-secret --from-literal=hf_api_token=<YOUR_HF_TOKEN>
  kubectl apply -f tgi-2-2b-it.yaml
```
    
check deployment is finished
```
 kubectl get pods
 kubectl port-forward service/gema 8000:8000
```

tell GCP Managed Prometeus what 




### STEP 2: Deploy gradio UI


```
 kubectl apply -f gradio.yaml
 kubectl port-forward service/gradio 8080:8080
```

open browser at localhost:8080

### STEP 3: Install autoscaling

follow this

https://cloud.google.com/kubernetes-engine/docs/tutorials/autoscaling-metrics#custom-metric
https://github.com/GoogleCloudPlatform/k8s-stackdriver/blob/master/custom-metrics-stackdriver-adapter/README.md

summary of commands

gcloud iam service-accounts add-iam-policy-binding --role \
  roles/iam.workloadIdentityUser --member \
  "serviceAccount:gemma-test-deployment.svc.id.goog[custom-metrics/custom-metrics-stackdriver-adapter]" \
  883536042426-compute@developer.gserviceaccount.com


kubectl annotate serviceaccount --namespace custom-metrics \
  custom-metrics-stackdriver-adapter \
  iam.gke.io/gcp-service-account=883536042426-compute@developer.gserviceaccount.com



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
