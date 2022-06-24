from yamale import YamaleError
import yamale
from pathlib import Path
import ruamel.yaml
import sys
import yaml
import argparse

#argsparser
parser = argparse.ArgumentParser() 
parser.add_argument('-c', '--config_path',action='store', dest='title', nargs='*', type=str,  help="Enter the folder path",required=True)
args = parser.parse_args()
string_version = "".join(args.title)
print(string_version)
"""
Validation function validates the input conditions with schema as the reference.
"""
def validation():
    #Create a schema object
    client_interface_schema = yamale.make_schema(string_version+'/config/fam_client_interface_schema.yaml', parser='ruamel')
    memory_server_schema = yamale.make_schema(string_version+'/config/fam_memoryserver_schema.yml', parser='ruamel')
    metadata_schema = yamale.make_schema(string_version+'/config/fam_metadata_schema.yaml', parser='ruamel')
    pe_schema = yamale.make_schema(string_version+'/config/fam_pe_schema.yaml', parser='ruamel')
    # Create a Data object
    try:
        client_interface_data = yamale.make_data(string_version+'/config/fam_client_interface_config.yaml', parser='ruamel')
        memory_server_data = yamale.make_data(string_version+'/config/fam_memoryserver_config.yaml', parser='ruamel')
        metadata_data= yamale.make_data(string_version+'/config/fam_metadata_config.yaml', parser='ruamel')
        pe_data = yamale.make_data(string_version+'/config/fam_pe_config.yaml', parser='ruamel')
        print ('The client interface data is :'+'\n'.join(map(str, client_interface_data)))
        print('')
        print('The memory server data is:'+'\n'.join(map(str, memory_server_data)))
        print('')
        print('The metadata is:'+'\n'.join(map(str, metadata_data)))
        print('')
        print('The fam_pe data is:'+'\n'.join(map(str, pe_data)))
        print('')
    except Exception as s: #This line shows an exception if two memory_server_ids are same.
        print('The error is\n%s' % str(s))
    #To validate
    try:
        yamale.validate(client_interface_schema, client_interface_data)
        yamale.validate(memory_server_schema,memory_server_data)
        yamale.validate(metadata_schema,metadata_data)
        yamale.validate(pe_schema,pe_data)
        print('Validation success! 👍')
    except ValueError as e:
        print('Validation failed!\n%s' % str(e))
"""
Compare block checks the conditions
"""
def compare():
    host_port = {}
    fam_path_list = {}
    libabric_port_list ={}
    file_in = Path(r'C:\Users\User\OneDrive\Desktop\toold\fam_memoryserver_config.yaml')
    yaml = ruamel.yaml.YAML(typ='safe')  
    data = yaml.load(file_in)
    for machine, config in data['Memservers'].items():
            if 'rpc_interface' not in config: 
                print(f'machine {machine} has no "rpc_interface"');
                sys.exit(1)
            else:
                host_port.setdefault(config['rpc_interface'], set()).add(machine)
                fam_path_list.setdefault(config['fam_path'], set()).add(machine)
                libabric_port_list.setdefault(config['libfabric_port'], set()).add(machine)
    # check if host_port has any values that have more than one machine
    print('The conditions are checked and validated')
    for hp, machine_nrs in host_port.items():
        if len(machine_nrs) == 1:
            continue
        j=[str(x) for x in machine_nrs]
        print(f'Found {hp} in machines: {", ".join(j)}')
   
    for hp, machine_nrs in fam_path_list.items():
        if len(machine_nrs) == 1:
            continue
        k=[str(x) for x in machine_nrs]
        print(f'Found {hp} in machines: {", ".join(k)}')

    for hp, machine_nrs in libabric_port_list.items():
        if len(machine_nrs) == 1:
           continue
        l=[str(x) for x in machine_nrs]
        print(f'Found {hp} in machines: {", ".join([str(x) for x in machine_nrs])}')

    def removeElements(j, k):
        return ', '.join(map(str, j)) in ', '.join(map(str, k))

    if (removeElements(j, k)==True) :
        print(f'The memory servers {j}, have the same fam_path, hence Validation failed!')
    else:
        print('Only the rpc_interface of the machines are same, hence Validation failed!')
 

    def removeElements(j, l):
        return ', '.join(map(str, j)) in ', '.join(map(str, l))

    if (removeElements(j, l)==True) :
        print(f'The memory servers {j}, have the same libfabric_port, hence Validation failed!')
        
    else:
        print('Only the rpc_interface of the machines are same, hence Validation failed!')

validation()
compare()