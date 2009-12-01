#!/usr/bin/python
#Bryan Bishop <kanzure@gmail.com>
#Automated Design Lab
"""
how to test this script:

    #setup directories and symlinks
    mkdir -p ~/adl/repo-recover/
    cd ~/adl/repo-recover/
    mkdir instances
    mkdir components
    ln -s ~/code/skdb/import_tools/repo-recover.py .

    #grab a cfg
    cp -p /home/kanzure/code/graphsynth/input/hydraulic.car.jack.gxml .

    #grab the corresponding fs
    ???

    #grab the .repo file
    ???

    #run the command
    python repo-recover.py --cfg=hydraulic.car.jack.cfg.gxml --fs=hydraulic.car.jack.fs.gxml --delrepo=hydraulic.car.jack.repo --components=componentbasis/ --instances=instances/
"""

#mostly for manipulating file paths
import os

#for serializing and easy human-powered reading/writing
import yaml

#for parsing command line arguments
import optfunc

#make sure graphsynth.py is findable via the PYTHONPATH environment variable
import graphsynth

from copy import copy, deepcopy

#for .repo file parsing
from xml.dom import minidom
from repo_to_yaml import repo_to_yaml

bryan_message = "bryan hasn't got that far yet"

def sanitize(filename):
    '''removes spaces, does wonderful things to turn some random string into a filename'''
    return filename.replace(" ", "_")

def get_file_list(path):
    '''returns a list of files in a directory'''
    assert os.path.isdir(path), "get_file_list: path must be a directory"
    return os.listdir(path)

def fix_node_name(name, debug=True):
    '''strips off numbers at the end, replace '_' with ' ', etc.'''
    original_name = copy(name)
    name = name.replace("_", " ")
    while name[-1].isdigit():
        name = name[:-1]
    name = name.strip()
    if debug: print "fix_node_name: original_name = ", original_name
    if debug: print "fix_node_name: \t\t", name
    return name

def load_cfg(path): return graphsynth.Graph.load_gxml(path)
def load_fs(path): return load_cfg(path)
def load_part(path): return yaml.load(open(path, "r"))
def load_repo(path, debug=False):
    '''takes a path to a .repo file and returns a dictionary of artifact names (keys) and their component basis names (values).'''
    doc = minidom.parse(open(path, "r"))
    #if debug: print "load_repo: doc = ", doc
    system = doc.childNodes[0].nextSibling.childNodes[1]
    #if debug: print "load_repo: system = ", system
    #if debug: print "system.childNodes = ", system.childNodes

    results = {}
    for artifact in system.childNodes:
        if artifact.nodeName == "Artifact":
            #if debug: print "load_repo: found an Artifact"
            artifact_name = artifact.attributes["ArtifactName"].nodeValue
            comp_basis_name = artifact.attributes["ArtifactCBName"].nodeValue
            results[artifact_name] = comp_basis_name
        else: pass #wasn't an artifact
        #if debug: print "artifact.nodeName = ", artifact.nodeName
    return results

def find_function(function_name, function_structures):
    '''given a function name, return the function (so you can get the function labels later) from within a list of function structures
    returns False when a matching function node (within any of the given FS graphs) cannot be found. '''
    for function_structure in function_structures:
        for node in function_structure.nodes:
            if node.name == function_name:
                return node
    return False #error: not found

def repo_recover(cfg=None, fs=None, delrepo=None, instances="instances/", components="componentsbasis/", debug=True):
    '''extracts component basis names from a {.gxml CFG, .gxml FS, .repo} and makes new .gxml files and an skdb-ish folder structure (instances/ and componentbasis/).

    ======== inputs ========
    repo-recover inputs are as follows:
        (1) a CFG in .gxml 2.0 format (--cfg)
        (2) a FS in .gxml 2.0 format (functionCAD has a GraphSynth plugin) (--fs)
        (3) .repo XML files from the design engineering lab repository (--delrepo)
        
    any of those 4 options may be paths to a particular file or to a folder.
    note: you must guarantee that the files are ordered the same way in each directory.
    for instance, cfg/1.gxml and fs/1.gxml must refer to the same graph.

    for instance:
        ./repo-recover.py --cfg=/path/to/swirl-seed.gxml --fs=/path/to/ss-fs.gxml
                           --delrepo=/path/to/del_repo/
        ./repo-recover.py --cfg=squirt-gun-cfg.gxml --fs=squirt-gun-fs.gxml
                           --delrepo=squirt-gun.repo --components=componentbasis/ --instances=instances/
    
    --components=componentbasis/    specify where component basis models are located
    --instances=instances/      specify where instance models are (like the squirt-gun folder)

    ======== output ========
    repo-recover outputs are as follow:
        (1) a CFG in .gxml 2.0 format
        (2) a primitive skdb-like package (folder) with YAML metadata

    ======== caveats ========
    the assumed file extension for FS and CFG files is: .gxml
    no duplicate node names in .gxml files (because of GraphSynth.load_gxml)
    '''
    if debug: print "repo_recover: starting"

    ###################################
    #start with parameter checks
    ###################################
    if debug: print "start with parameter checks"

    if cfg is None: raise ValueError, "repo_recover: no CFG given."
    elif os.path.isdir(cfg): cfg = os.listdir(cfg)
    elif not os.path.isfile(cfg): raise ValueError, "repo_recover: input CFG file does not exist?"
    else: cfg = [cfg]

    if fs is None: raise ValueError, "repo_recover: no FS given."
    elif os.path.isdir(fs): fs = os.listdir(fs)
    elif not os.path.isfile(fs): raise ValueError, "repo_recover: input FS file does not exist?"
    else: fs = [fs]

    if delrepo is None: raise ValueError, "repo_recover: don't know where to find a .repo file."
    elif os.path.isdir(delrepo): delrepo = os.listdir(delrepo)
    elif not os.path.isfile(delrepo): raise ValueError, "repo_recover: DEL .repo files not found?"
    else: delrepo = [delrepo]

    #if parts is None: raise ValueError, "repo_recover: don't know where to find the YAML files."
    #elif os.path.isdir(parts): parts = os.listdir(parts)
    #elif not os.path.isfile(parts): raise ValueError, "repo_recover: YAML file doesn't exist?"
    #else: parts = [parts]
    
    #by default let's say the output should go in ./componentbasis/ and ./del_artifacts/ (or ./instances/)
    if components is None: raise ValueError, "repo_recover: don't know where to put or find components."
    elif os.path.isfile(components): raise ValueError, "repo_recover: components path must not be a file."
    elif not os.path.exists(components): os.mkdir(components)

    #where specific part instances should go (./instances/)
    if instances is None: raise ValueError, "repo_recover: don't know where to put or find instances."
    elif os.path.isfile(instances): raise ValueError, "repo_recover: instances path must not be a file."
    elif not os.path.exists(instances): os.mkdir(instances)

    if debug: print "done with parameter checks"
    ###################################
    #load up the data
    ###################################
    if debug: print "load up the data"

    loaded_cfg = []
    loaded_fs = []
    loaded_repo = []

    for a_cfg in cfg:
        loaded_cfg.append(load_cfg(os.path.abspath(a_cfg)))
    for a_fs in fs:
        loaded_fs.append(load_fs(os.path.abspath(a_fs)))
    for a_repo in delrepo:
        #if debug: print "***************** a_repo is: ", a_repo
        content123 = load_repo(os.path.abspath(a_repo), debug=debug)
        #if debug: print "***************** content123 is: ", content123
        loaded_repo.append(content123)

    assert ( len(loaded_cfg) == len(loaded_fs) ), "repo-recover: there must be as many CFG files as FS files" #i think
    #it's possible that you have 1 FS for 1000 CFGs
    #but what if you have more than 1 FS, and a disproportionate number of CFGs? i dunno, so i haven't implemented that.
    
    #turn all the original information into absolute paths (just in case)
    new_cfg = []
    for a_cfg in cfg:
        new_cfg.append(os.path.abspath(a_cfg))
    cfg = new_cfg

    new_fs = []
    for a_fs in fs:
        new_fs.append(os.path.abspath(a_fs))
    fs = new_fs

    new_repo = []
    for a_repo in delrepo:
        new_repo.append(os.path.abspath(a_repo))
    delrepo = new_repo

    if debug: print "done loading up the data"
    ###################################
    #look at the local labels in loaded_cfg nodes and find corresponding functions in loaded_fs
    #append them to loaded_cfg nodes
    ###################################
    if debug: print "looking at the local labels"

    for cfg in loaded_cfg:
        for node in cfg.nodes:
            #set up the node to have a blank list of functions
            node.functions = []

            for label in node.local_labels:
                #labels that start with "n" refer to node names in the FS graph
                #note: all labels in the input CFG are assumed to reference functions in the FS graphs
                if label[0] == "n":
                    #which_fs corresponds to the FS for the current CFG
                    which_fs = loaded_fs[loaded_cfg.index(cfg)]

                    #find the function with this label in the FS object (of type Graph)
                    the_function = find_function(label, [which_fs])

                    if the_function:
                        if debug: print "function found for node \"%s\" label \"%s\" is: %s" % (node.name, label, the_function)
                        node.functions.append(the_function)
                    elif the_function == False: #no function was found
                        if debug: print "no function was found for node \"%s\" label \"%s\"" % (node.name, label)
                else:
                    if debug: print "unrecognized label on node \"%s\" (value: \"%s\")" % (node.name, label)
                    
    if debug: print "done looking at the local labels"
    ###################################
    #get component basis name from loaded_repo and append to loaded_cfg data
    ###################################
    if debug: print "getting component basis names, attaching URIs"
    loaded_repo = loaded_repo[0]
    if debug: print "loaded_repo is: ", loaded_repo

    for cfg in loaded_cfg:
        for node in cfg.nodes:
            fixed_node_name = fix_node_name(node.name, debug=debug)
            if fixed_node_name in loaded_repo:
                #loaded_repo lets you find the CB name by giving an indexer (artifact name or CFG node name)
                node.component_basis = loaded_repo[fixed_node_name] #wait, that's loaded_repo[] .. so what about the CB name?
                node.uri = "http://adl.serveftp.org/lab/repo-recover/componentbasis/" + node.component_basis + ".yaml"
            else:
                if debug: print "unable to find a component_basis name for the node \"%s\" in the original CFG." % (fixed_node_name)

    if debug: print "done getting component basis names"
    ###################################
    #output the data
    ###################################
    if debug: print "outputting data"

    #parse the output location information and come up with absolute paths
    instances = os.path.abspath(instances)
    components = os.path.abspath(components)

    #step 1) .gxml 2.0 output
    for cfg in loaded_cfg:
        #if instances=instances/ then this should save a cfg named "blah.gxml" at instances/blah/blah.gxml
        pkg_path = os.path.join(instances, cfg.name)
        
        #if it doesn't exist yet, make it
        if not os.path.exists(pkg_path): os.mkdir(pkg_path)

        #modify the cfg so that save_gxml works (there's more info in the CFG in this script than usual)
        temp_cfg = deepcopy(cfg)
        for node in temp_cfg.nodes:
            if not hasattr(node, "component_basis"): continue
            component_basis = node.component_basis
            functions = node.functions

            #transform the list of functions into a list of function names
            new_functions = []
            for function in functions:
                new_functions.append(function.name)
            functions = new_functions

            #make a quick copy of the local labels
            original_local_labels = copy(node.local_labels)
            
            #local label order: CB name, URI, functions, other stuff
            new_local_labels = [component_basis]
            new_local_labels.extend(functions)
            new_local_labels.extend(original_local_labels)

            #set it
            node.local_labels = new_local_labels

        #save the new gxml of the CFG
        temp_cfg.save_gxml(os.path.join(pkg_path, cfg.name) + ".gxml", version=2.0)

        #make a copy of the old cfg
        os.system("cp -p \"%s\" \"%s\"" % (cfg.filename, os.path.join(pkg_path, cfg.name) + ".bak"))
    #step 2) copy the function structures too
    for fs in loaded_fs:
        if debug: print "copying function structure file (%s) into the instance directory (package path)" % (fs.name)
        pkg_path = os.path.join(instances, fs.name)
        #if it doesn't exist yet, make it (but this shouldn't really happen)
        if not os.path.exists(pkg_path):
            os.mkdir(pkg_path)
            print "this shouldn't happen"
        
        #figure the file name and make up a target path
        base_name = os.path.basename(fs.filename)
        target_path = os.path.join(pkg_path, base_name[:-5])

        #copy the fs file to the new location in
        os.system("cp -p \"%s\" \"%s\"" % (fs.filename, target_path))
    
    #######################################
    #step 3) for each component basis name, make a new skeleton .yaml representation for it and put it in instances/

    #make a dictionary of all component basis names and their instance names
    instances_and_cb = {}
    #also a list of all components needed
    all_components_needed = set()
    for cfg in loaded_cfg:
        for node in cfg.nodes:
            if hasattr(node, "component_basis"):
                instances_and_cb[node.name] = node.component_basis
                all_components_needed.add(node.component_basis)

    #there is already an instance file for each part in loaded_cfg, located in the instances/ directory
    #now we need to make the file for the components/ directory
    pre_existing_component_bases = os.listdir(components)
    if debug: print "all_components_needed: ", all_components_needed
    if debug: print "pre_existing_component_bases: ", pre_existing_component_bases
    for cb in all_components_needed:
        #check if it already exists (could also use os.path.exists)
        if (sanitize(cb)+".yaml") not in pre_existing_component_bases:
            #make the file
            #FIXME: what goes in the file?
            fh = open(os.path.join(components, sanitize(cb)+".yaml"), "w")
            fh.write(yaml.dump(None))
            fh.close()
    
    #######################################

    i = 0
    #i think this is broken
    #step 3) yaml skdb package output -- convert to skdb-ish representations
    for cfg in loaded_cfg:
        #find the corresponding .repo file
        corresponding_repo_file = delrepo[i]
        a_repo = corresponding_repo_file
        
        if debug: print "converting .repo into a yaml representation"
        resulting_yaml = repo_to_yaml(repo=a_repo)
        if debug: print "done converting .repo into a yaml representation"

        base_name = os.path.basename(a_repo)
        if debug: print "base_name is: ", base_name
        base_name_scrubbed = base_name[:-5] #get rid of the .repo at the end of the filename
        if debug: print "base_name_scrubbed is: ", base_name_scrubbed
        
        #pkg_path = os.path.join(instances, base_name_scrubbed)
        pkg_path = os.path.join(instances, sanitize(cfg.name))
        yaml_file_path = os.path.join(pkg_path, base_name_scrubbed + ".repo.yaml")

        file_handler = open(yaml_file_path, "w")
        file_handler.write(resulting_yaml)
        file_handler.close()
        i = i + 1

    if debug: "repo_recover: ending"

if __name__ == "__main__":
    optfunc.run(repo_recover)
