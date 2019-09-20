# seldon-pytorch-example
Example of using Seldon Core in Kubernetes cluster for serving PyTorch models

## Basic usage
### Prerequisites
* A kubernetes cluster with
  * kubectl
  * Helm
  * [k8s-device-plugin](https://github.com/NVIDIA/k8s-device-plugin)
  * Docker repository (here I used my own docker repo)
   * Note that if you use a private repo, you need to have proper credentials on every node in your cluster
  * Ambassador gateway
### Installation
1. Train a model
2. Pickle it
3. Change `Model.py` to unpickle _your_ file
4. `sudo make build`
5. `sudo docker push ${YOUR_IMAGE_NAME}`
6. `kubectl create -f sdep*`

### Testing
To test if the model is working, you should send a request to your server. To find out what's the external IP of your cluster with something along the lines of:
```
HOST=http://$(kubectl get svc | grep 'LoadBalancer' | sed 's/  \+/ /g' | cut -d " " -f 4);
URL=${HOST}/seldon/seldon/seldon-model/api/v0.1/predictions;
echo $URL;
```

and then send a curl request using the test payloads with:

```
curl -X POST -H "Content-Type: application/json" --data @Desktop/test_mnist_9.json $URL
```

or with Python3:

```
from torchvision.datasets import MNIST
import json
import requests
from PIL import Image
API_URL = 'http://YOUR_ENDPOINT/seldon/seldon/seldon-model/api/v0.1'
ENDPOINT = '/predictions'
mnist_test = MNIST(root=DATASET_ROOT, download=False, train=False)

def test_endpoint(i):
    a = mnist_test[i][0]
    a = np.array(a)round(a, decimals=3)
    payload = a
    test_json = json.dumps({"data":{"ndarray": payload.tolist()}})
    print(len(test_json.encode('utf-8')) // 1024, "KB")
    headers = {"Content-Type": "application/json"}
    return requests.post(API_URL+ENDPOINT, headers=headers, data=test_json)

test_endpoint(42) # Returns <Response 200> ... hopefully.

# One can also use multithreading to stress test seldon server
import concurrent.futures as cf
with cf.ThreadPoolExecutor(max_workers=128) as executor:
    for future in cf.as_completed([executor.submit(test_endpoint, i) for i in range(128)]):
        print(future)
```
## TODOs
Helm chart is not finished. JSON template should be translated to YAML template according to `sdep-test-model.yaml` deployment file, and various constants should be refactored from the template to `values.yaml` for configuration.
