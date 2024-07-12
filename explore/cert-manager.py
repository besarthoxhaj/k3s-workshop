# %%
import yaml

# %%
with open('./cert-manager.yaml') as f: docs = list(yaml.safe_load_all(f))
print('len(docs)', len(docs)) # 52 manifests
docs = [d for d in docs if d is not None]
print('len(docs)', len(docs)) # 46 manifests
for doc in docs: print(doc['kind'], '--', doc.get('apiVersion'), '--', doc.get('metadata').get('name'))
# ...


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

# %%
# resource = get_resource(docs, 'Deployment', 'cert-manager-cainjector')
# resource = get_resource(docs, 'Deployment', 'cert-manager')
# resource = get_resource(docs, 'Deployment', 'cert-manager-webhook')
resource = get_resource(docs, 'CustomResourceDefinition', 'issuers.cert-manager.io')
# resource = remove_description(resource)
with open('./debug.tmp.yaml', 'w') as d: d.write(yaml.dump(resource))

# %%
