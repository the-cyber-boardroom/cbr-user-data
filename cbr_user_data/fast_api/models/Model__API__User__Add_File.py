from dataclasses                        import dataclass
from osbot_utils.base_classes.Type_Safe import Type_Safe

@dataclass
class Model__API__User__Add_File(Type_Safe):
    file_name  : str
    file_bytes : bytes
    folder_id  : str = None                                  # todo: find way to make Random_Guid work here

