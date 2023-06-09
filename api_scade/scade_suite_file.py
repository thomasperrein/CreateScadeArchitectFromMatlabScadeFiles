"""
Object Scade Suite file and its content
"""

import api_scade.path_gestion
import scade.model.suite, scade.model.project
import scade_env
import typing

from abc import ABC
import re

class ScadeFile(ABC):
    """ Scade file """
    def __init__(self, path:str) -> None:
        scade_env.load_project(path)
        session = scade.model.suite.get_roots()[0]
        self.session = session
        self.path = session.descriptor.model_file_name
        self.model = session.model
        self.id = session._id_
        self.descriptor = session.descriptor
        

    def close(self):
        self.session.unload()


    def open(self,path):
        self.session.load2(path)


class ScadeFileSuite(ScadeFile):
    """ Specific suite file """
    def __init__(self, path) -> None:
        super().__init__(path)
        self.scade_file_type = 'suite'
    

    def data_of_diagram(self, number:int = 0):
        out = {}
        for librarie in Model(self.model).get_libraries(number):
            model_temp = Model(librarie)
            for operator in model_temp.get_operators():
                out[model_temp.get_name_of_operator(operator)] = {}
                for diagram in model_temp.get_diagrams_from_operator(operator):
                    output_list = re.findall(r'\b[V]\w*\s*=', diagram.to_string())
                    input_list = re.findall(r'=\s*\b[V]\w*', diagram.to_string())
                    # Supprimer le signe égal et les espaces en trop
                    output_list = [s.strip(' =') for s in output_list]
                    input_list = [s.strip('= ') for s in input_list]
                    out[model_temp.get_name_of_operator(operator)][model_temp.get_name_of_diagram(diagram)] = {'inputs': input_list, 'outputs': output_list}
        return out


    def data_of_nodes(self):
        out = {}
        model_temp = Model(self.model)
        for node in model_temp.get_nodes():
            out[model_temp.get_node_name(node)] = {'inputs': model_temp.get_inputs_of_nodes(node,'name'), 'outputs': model_temp.get_outputs_of_nodes(node,'name')}
        return out


class Model():
    """ classe model herité de scade """
    def __init__(self,model:scade.model.suite.suite.Model) -> None:
        self.nodes = model.nodes
        self.operators = model.operators
        self.libraries = model.libraries

    def get_nodes(self):
        return self.nodes

    
    def get_operators(self):
        return self.operators


    def get_libraries(self, number:int = 0) -> typing.List[scade.model.suite.suite.Model]:
        """ get the last {number} of object librairies, default take all the librairies """
        return self.libraries[-number:]


    def get_name_of_operator(self,operator):
        return operator.name


    def get_diagrams_from_operator(self,operator):
        if operator in self.get_operators():
            return self.operators[self.operators.index(operator)].diagrams
        else:
            return
    

    def get_name_of_diagram(self,diagram):
        return diagram.name


    def get_inputs_of_diagram(self, diagram):
        return diagram.data_def.inputs


    def get_outputs_of_diagram(self, diagram):
        return diagram.data_def.outputs


    def get_inputs_of_nodes(self, node, format='object'):
        if format == 'object':
            return node.inputs
        elif format == 'name':
            return [input.name for input in node.inputs]
        else:
            raise ValueError("the format is not correct : allowed values are {'object'|'name'}")

    
    def get_outputs_of_nodes(self, node, format='object'):
        if format == 'object':
            return node.outputs
        elif format == 'name':
            return [output.name for output in node.outputs]
        else:
            raise ValueError("the format is not correct : allowed values are {'object'|'name'}")


    def get_node_name(self,node):
        return node.name