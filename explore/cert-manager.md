## Explore Cert Manager

The manifest for [cert-manager](https://cert-manager.io) is very big and the
functionality not very well explained. More specifically the docs talk about
how to use cert-manager but not how cert-manager works. This is a tour on how
I went about to explore the innner workings.

First thing, instead of blindly installing it I will just download the yaml.
Then I will check manually what' inside it and go from there.

```sh
# https://cert-manager.io/docs/installation/kubectl/
$ curl -LO https://github.com/cert-manager/cert-manager/releases/download/v1.15.1/cert-manager.yaml
$ cat cert-manager.yaml # massive wall of configuration
$ wc -l cert-manager.yaml # 9350 explore/cert-manager.yaml
```

As the command above shows, the file is massive and there is almost no point in
trying to stare at it. Instead we will explore it programmaticaly using python.

```py
import yaml
with open('./cert-manager.yaml') as f: docs = list(yaml.safe_load_all(f))
print('len(docs)', len(docs)) # 52 manifests
docs = [d for d in docs if d is not None]
print('len(docs)', len(docs)) # 46 manifests
for doc in docs: print(doc['kind'], '--', doc.get('apiVersion'), '--', doc.get('metadata.name'))
# ...
```

To help out the process I'll create two utility functions that manipulate yaml.

```py
def get_resource(docs, kind, name):
  for doc in docs:
    is_kind = doc.get('kind') == kind
    is_name = doc.get('metadata', {}).get('name') == name
    if is_kind and is_name: return doc
  return None

def remove_description(doc):
  if isinstance(doc, dict):
    new_doc = {}
    for key, value in doc.items():
      if key != 'description':
        new_doc[key] = remove_description(value)
    return new_doc
  elif isinstance(doc, list):
    return [remove_description(item) for item in doc]
  else:
    return doc
```

```sh
$ kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.1/cert-manager.yaml
# ...
$ kubectl get pods --namespace cert-manager
# NAME                                       READY   STATUS    RESTARTS   AGE
# cert-manager-5798486f6b-v7ps9              1/1     Running   0          40s
# cert-manager-cainjector-7666685ff5-59bg2   1/1     Running   0          41s
# cert-manager-webhook-5f594df789-6kknx      1/1     Running   0          40s
$ kubectl apply -f ./manifests/_issuer.yml
```