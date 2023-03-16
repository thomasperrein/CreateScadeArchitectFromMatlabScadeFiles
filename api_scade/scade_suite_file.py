"""
Object Scade Suite file and its content
"""

import path_gestion
import scade_env
import scade.model.suite, scade.model.project

from abc import ABC
import re

class ScadeFile(ABC):
    """ Scade file """
    def __init__(self, path) -> None:
        self.path = path
        scade_env.load_project(path)
        self.env = scade.model.suite.get_roots()
        self.model = scade.model.suite.get_roots()[0].model
        self.id = scade.model.suite.get_roots()[0]._id_
        self.descriptor = scade.model.suite.get_roots()[0].descriptor

    def close(self):
        pass

class ScadeFileSuite(ScadeFile):
    """ Specific suite file """
    def __init__(self, path) -> None:
        super().__init__(path)
        self.scade_file_type = 'suite'
    
    
    def get_nodes(self):
        return self.model.nodes

    
    def get_operators(self):
        return self.model.operators


    def get_name_of_operator(self,operator):
        return operator.name

    def get_diagrams_from_operator(self,operator):
        if operator in self.get_operators():
            return self.model.operators[self.model.operators.index(operator)].diagrams
        else:
            return
    

    def get_name_of_diagram(self,diagram):
        return diagram.name


    def get_inputs_of_diagram(self,diagram):
        return diagram.data_def.inputs


    def get_outputs_of_diagram(self,diagram):
        return diagram.data_def.outputs


    def data_of_interest(self):
        out = {}
        for operator in self.get_operators():
            out[self.get_name_of_operator(operator)] = {}
            for diagram in self.get_diagrams_from_operator(operator):
                output_list = re.findall(r'V\w*\s*=', diagram.to_string())
                input_list = re.findall(r'=\s*V\w*', diagram.to_string())
                # Supprimer le signe égal et les espaces en trop
                output_list = [s.strip(' =') for s in output_list]
                input_list = [s.strip('= ') for s in input_list]
                out[self.get_name_of_operator(operator)][self.get_name_of_diagram(diagram)] = {'inputs': input_list, 'outputs': output_list}
                # out[self.get_name_of_operator(operator)][self.get_name_of_diagram(diagram)] = {'inputs':self.get_inputs_of_diagram(diagram),
                                                        #  'outputs':self.get_outputs_of_diagram(diagram)}
        return out