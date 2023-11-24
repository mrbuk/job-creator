import yaml, sys
from kubernetes import client, config, utils

def main():
    if len(sys.argv) < 3:
        print("usage: {} NAME INT_N".format(sys.argv[0]))
        sys.exit(1)

    name = sys.argv[1]
    date = sys.argv[2]

    job_definition = []
    with open("job.yaml", "r") as stream:
        try:
            job_definition = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    # replace the job with a specific parameter
    job_definition["metadata"]["name"] = name
    job_definition["spec"]["template"]["spec"]["containers"][0]["command"][3] = "print bpi({})".format(date)

    # load_config should load a local kubeconfig if it exists
    # and in cases where is does not will try to use incluster
    config.load_config()
    k8s_client = client.ApiClient()

    utils.create_from_dict(k8s_client,data=job_definition,verbose=True)

if __name__ == "__main__":
    main()