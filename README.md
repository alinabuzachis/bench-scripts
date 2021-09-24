# Benchmark Scripts for community.okd Collection

This repository contains some automation scripts to assist with performance testing for some aspects of the [community.okd collection](https://github.com/ansible-collections/community.okd), e.g., testing the benefits of Turbo mode on some k8s objects creation.

## Running the tests on a Provision Red Hat OpenShift Cluster on AWS

A set of roles and playbooks to provision and deprovision an Red Hat OpenShift Cluster on AWS can be found in this repository [openshift-cluster-setup repository](https://github.com/alinabuzachis/openshift-cluster-setup). See the [openshift-cluster-setup README](https://github.com/alinabuzachis/openshift-cluster-setup/README.md) for further details.

## Running the tests
  1. Prepare the environment `ansible-playbook prepare_env.yml`
  2. Start the experiment `~/env/bin/ansible-playbook main.yml`

**Note:** For testing the collections using Turbo mode you have to use the following command instead `ENABLE_TURBO_MODE=1 ~/env/bin/ansible-playbook main.yml`  

Then the `main.yml` playbook deploys the amount of Namespaces and ConfigMaps defined by `obj_count` in `config.yml` into the OpenShift cluster. At the end of the playbook, Ansible's ARA callback plugins report back the timings of all the tasks.

## Plot the results
Results can be plotted with `python plot/plot.py`.
