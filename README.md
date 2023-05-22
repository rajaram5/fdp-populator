# FDP Populator
## Introduction
The FDPP was created to help people not very familiar with FAIR, to create metadata in Excel sheets, and have these published in a FAIR Data Point (https://www.fairdatapoint.org/). The FDPP is a GitHub workflow, that reads the metadata from the repository, transforms this into RDF, and then publishes this on a FAIR Data Point.

## Set up
* If there is no FDP yet, set one up locally (https://fairdatapoint.readthedocs.io/en/latest/deployment/local-deployment.html) or online (https://fairdatapoint.readthedocs.io/en/latest/deployment/production-deployment.html).
* Make a metadata repository like https://github.com/LUMC-BioSemantics/ejprd-wp13-metadata. This repository is connected to the FAIR Data Point Populator GitHub repository.
* Connect the metadata repository to a FAIR Data Point by setting the GitHub secrets in the metadata repository.
	* FDP URL
	* FDP Persistant URL
	* Username
	* password

## Use
* The **user** fills in the [FPD](https://github.com/LUMC-BioSemantics/EJP-RD-WP13-FDP-template) or [EJPRD](https://github.com/ejp-rd-vp/resource-metadata-schema/blob/master/template/EJPRD%20Resource%20Metadata%20template.xlsx) template.
* The **user** uploads the template to the metadata repository (or hands it over to the administrator for the administrator to upload).
* The **administrator** checks the metadata.
* The **administrator** sets the target metadata and target catalog in the config.yml file, and starts the workflow using the start workflow button.
* The **FDPP** converts the metadata from the Excel sheet into RDF documents.
* The **FDPP** publishes the RDF into the connected FAIR Data Point.

## EJPRD
The EJPRD version of the tool is being prepared for users, and is in the VP branch of this repository.
