# Benchmark Scripts for community.okd Collection

This repository contains some automation scripts to assist with performance testing for some aspects of the [community.okd collection](https://github.com/ansible-collections/community.okd).
## Running the tests
  1. Prepare the environment `ansible-playbook prepare_env.yml`
  2. Start the experiment `~/env/bin/ansible-playbook main.yml`

**Note:** For testing the collections using the Turbo mode you have to use the following command instead `ENABLE_TURBO_MODE=1 ~/env/bin/ansible-playbook main.yml`  

Then the `main.yml` playbook deploys the amount of Namespaces and ConfigMaps defined by `obj_count` in `config.yml` into the cluster. At the end of the playbook, Ansible's ARA callback plugins report back the timings of all the tasks.

## Plot the results
Results can be plotted with `python plot/plot.py`.
