# fdp-populator
The FAIR Data Point Populator Populator FDPs with metadata entries from an excel template. It uses a GitHub action to automatically read the template, and publish the entries in a FAIR Data Point.



## Usage
1. Download the [template](https://github.com/ejp-rd-vp/resource-metadata-schema/blob/master/template/EJPRD%20Resource%20Metadata%20template.xlsx) from [here](https://github.com/ejp-rd-vp/resource-metadata-schema) and follow the instructions for filling it in.

2. Upload the filled in template to a folder in the repository linked to the FDP of choice, or ask the administrator of the repository to do this and the following steps.

3. Change the config.yml file to point to the target Excel template and FDP catalog.

4. Press the run workflow button in the GitHub actions tab.
