===============
SPARTA report ansible plugin
===============

An Ansible plugin for outputting your task as step of your automation test suite runs.

# Usage

Make a directory called `callback_plugins` next to your playbook and put `callback_plugins` contents of this repository inside it.

# Run you test cases structured as various play book files as FEATURE / SCENARIOS:

ansible-playbook -i hosts  application.yml

- `application.yml` should be top level playbook : Starting point of your automation suite.
- `featureX.yml` : create as per need, include in `application.yml`.
- `scenarioX.yml` : create as per need, include in respective `featureX.yml`.
