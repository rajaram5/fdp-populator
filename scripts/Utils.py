import chevron

class Utils:
    """
    Utils class contents methods to generate resource specific triples
    """

    def add_resource_triples(self, resource, graph):
        """
        This method adds resource specific triples to the RDF graph

        :param resource: Provide resource object
        :param graph: Provide RDF graph
        """
        with open('../templates/resource.mustache', 'r') as f:
            turtle_string = chevron.render(f, {'description': resource.DESCRIPTION, 'title': resource.TITLE,
                                      'parent_url': resource.PARENT_URL,
                                      'publisher_url': resource.PUBLISHER_URL,
                                      'publisher_name': resource.PUBLISHER_URL})
            graph.parse(data=turtle_string, format="turtle")

    def add_language_triples(self, resource, graph):
        """
        This method adds language specific triples about a resource to the RDF graph

        :param resource: Provide resource object
        :param graph: Provide RDF graph
        """
        if resource.LANGUAGE_URL:
            with open('../templates/language.mustache', 'r') as f:
                turtle_string = chevron.render(f, {'language_url': resource.LANGUAGE_URL})
                graph.parse(data=turtle_string, format="turtle")

    def add_licence_triples(self, resource, graph):
        """
        This method adds license specific triples about a resource to the RDF graph

        :param resource: Provide resource object
        :param graph: Provide RDF graph
        """
        if resource.LICENSE_URL:
            with open('../templates/license.mustache', 'r') as f:
                turtle_string = chevron.render(f, {'license_url': resource.LICENSE_URL})
                graph.parse(data=turtle_string, format="turtle")
    
    def list_to_rdf_literals(self, literal_list):
        # Return empty string if None
        if literal_list == None:
            return ""

        # Create literal list
        literal_str = ""
        for literal in literal_list:
            literal_str = literal_str + ' "' + literal + '",'
        literal_str = literal_str[:-1]

        return literal_str

    def list_to_rdf_URIs(self, URI_list):
        # Return empty string if None
        if URI_list == None:
            return ""

        # Create URI list
        URI_str = ""
        for URI in URI_list:
            URI_str = URI_str + " <" + URI + ">,"
        URI_str = URI_str[:-1]

        return URI_str