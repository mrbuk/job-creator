from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import yaml, sys
from kubernetes import client, config, utils

class JobDefinition(BaseModel):
    name: str
    date: str

app = FastAPI()

@app.post("/job/")
async def create_job(job: JobDefinition):
    try:
        create_kubernetes_job(job)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"{err=}")
    return job

def create_kubernetes_job(job: JobDefinition):
    job_definition = []
    stream = open("job.yaml", "r")
    job_definition = yaml.safe_load(stream)

    # replace the job with a specific parameter
    job_definition["metadata"]["name"] = job.name
    job_definition["spec"]["template"]["spec"]["containers"][0]["command"][3] = "print bpi({})".format(job.date)

    # load_config should load a local kubeconfig if it exists
    # and in cases where is does not will try to use incluster
    config.load_config()
    k8s_client = client.ApiClient()

    utils.create_from_dict(k8s_client,data=job_definition,verbose=True)
