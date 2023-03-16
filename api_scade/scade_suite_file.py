"""
Object Scade Suite file and its content
"""

import api_scade.path_gestion
import scade.model.suite, scade.model.project
import typing

from abc import ABC
import re

class ScadeFile(ABC):
    """ Scade file """
    def __init__(self, session: scade.model.suite.Session) -> None:
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
    def __init__(self, session) -> None:
        super().__init__(session)
        self.scade_file_type = 'suite'
    

    def data_of_interest(self, number:int = 0):
        out = {}
        for librarie in Model(self.model).get_libraries(number):
            model_temp = Model(librarie)
            for operator in model_temp.get_operators():
                out[model_temp.get_name_of_operator(operator)] = {}
                for diagram in model_temp.get_diagrams_from_operator(operator):
                    output_list = re.findall(r'\bV\w*\s*=', diagram.to_string())
                    input_list = re.findall(r'=\s*\bV\w*', diagram.to_string())
                    # Supprimer le signe égal et les espaces en trop
                    output_list = [s.strip(' =') for s in output_list]
                    input_list = [s.strip('= ') for s in input_list]
                    out[model_temp.get_name_of_operator(operator)][model_temp.get_name_of_diagram(diagram)] = {'inputs': input_list, 'outputs': output_list}
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

