
class API_Base_Connector:
    def __init__(self, documentation_home) -> None:
        self.documentation_home = documentation_home
        pass
    
    def get_docs(self):
        return self.documentation_home