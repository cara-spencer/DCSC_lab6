import time,os

import googleapiclient.discovery
import google.auth


def create_instance(compute, project, zone, name, tags, metaScripts:dict, snapshot=None):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
                project='ubuntu-os-cloud', family='ubuntu-1804-lts').execute()
    source_disk_image = image_response['selfLink']
    if snapshot is None:
        initial = {'sourceImage': source_disk_image}
    else:
        initial = {'sourceSnapshot': f'global/snapshots/{snapshot}'}
    # Configure the machine
    machine_type = "zones/%s/machineTypes/e2-standard-2" % zone
    metaItems = [{'key':k,'value':open(v,'r').read()} for k,v in metaScripts.items()]
    config = {
        'name': name,
        'machineType': machine_type,
        'tags':{
            'items':tags
        },

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': initial
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': metaItems
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()
        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)


credentials, project = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

projectID = 'lab-6-366616'


''' Create First VM '''
# operation = create_instance(service,projectID,zone='us-west1-a',name='lab6-local',tags=['allow-5000'],
#                             metaScripts={'startup-script':'startup-script.sh'})
# wait_for_operation(service, projectID, 'us-west1-a',operation['name'])

''' Create snapshot '''
# disk = 'lab6-local'
# snapshot_body = {
#     'name':'base-snapshot-lab6',
#     'sourceDisk':disk
# }
# response = service.disks().createSnapshot(project=projectID, zone='us-west1-a', 
#                                          disk=disk, body=snapshot_body).execute()

''' Create All VMs '''
# operation = create_instance(service,projectID,zone='us-west1-a',name='lab6-local',tags=['allow-5000'],
#                             metaScripts={'startup-script':'startup-script.sh'})
# wait_for_operation(service, projectID, 'us-west1-a',operation['name'])
operation = create_instance(service,projectID,zone='us-west1-a',name='lab6-regional',tags=['allow-5000'],
                            metaScripts={'startup-script':'startup-script.sh'})
wait_for_operation(service, projectID, 'us-west1-a',operation['name'])
operation = create_instance(service,projectID,zone='europe-west3-a',name='lab6-remote',tags=['allow-5000'],
                            metaScripts={'startup-script':'startup-script.sh'})
wait_for_operation(service, projectID, 'europe-west3-a',operation['name'])
