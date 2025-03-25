import argparse
import subprocess
from IPython.display import clear_output
from datetime import datetime
from joblib import Parallel, delayed
from loguru import logger
from time import sleep
import numpy as np
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--endpoint", help="the url endpoint, such as http://localhost:8000")
parser.add_argument("--metrics", help="a comma separated list of metrics")
args = parser.parse_args()

url = args.endpoint

if args.metrics is not None:
    metrics = [i.strip() for i in args.metrics.split(',')]
else:
    metrics = None

class Pods:

    def __init__(self):
        self.get_pods()
        logger.info(f'found {len(self.podnames)} pods')
        
    def get_pods(self):
        logger.info('getting pods')
        getpods_command = 'kubectl get pods'
        
        s = subprocess.run(getpods_command.split(), capture_output=True).stdout.decode()
        self.podnames = [i.split()[0] for i in s.split('\n') if not i.startswith('NAME') and len(i.split())>0]

    def run_cmd(self, cmd):
        def _run_cmd(podname, cmd):
            formatted_cmd = cmd.format(podname=podname)
            return subprocess.run(formatted_cmd.split(), capture_output=True).stdout.decode().strip()
        
        r = Parallel(n_jobs=-1)(delayed(_run_cmd)(podname, cmd) for podname in self.podnames)    
        return {k:v for k,v in zip(self.podnames, r)}
    
    def gpu_usage(self):
        gpusage_command = 'kubectl exec -it {podname} --  nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader'
        return self.run_cmd(gpusage_command)

    def run_loop(self, method, wait_seconds=1):
        while True:
            r = method()

            
            clear_output()
            current_dateTime = datetime.now()    
            logger.info (f'{"pod":50s}    {"gpu usage"}')
            for k,v in r.items():
                logger.info (f'  {k:48s}    {v}')

            logger.info('')
            if metrics is not None:
                s = requests.get(f'{url}/metrics')
                m = [[si for si in str(s.text).split('\n') if si.startswith(metric)] for metric in metrics]
                logger.info('end point metrics')
                if len(m)==0:
                    logger.error (f'metric {metric} not found')
                else:
                    for mi in m:
                        logger.info ('  '+'\n'.join(mi))
                print ('', flush=True)   
            sleep(wait_seconds)

            if np.random.randint(10)==0:
                self.get_pods()


pods = Pods()
pods.run_loop(pods.gpu_usage)
