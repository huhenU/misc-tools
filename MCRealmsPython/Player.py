class Player:
    def __init__(self, uuid:str, name:str, operator:bool, accepted:bool, online:bool, permission:str):

        self.__uuid:str = uuid
        self.__name:str = name
        self.__operator:bool = operator
        self.__accepted:bool = accepted
        self.__online:bool = online
        self.__permission:str = permission

    @property
    def uuid(self) -> str:
        return self.__uuid
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def operator(self) -> bool:
        return self.__operator

    @property
    def accepted(self) -> bool:
        return self.__accepted
    
    @property
    def online(self) -> str:
        return self.__online

    @property
    def permission(self) -> str:
        return self.__permission

    def __str__(self) -> str:
        return f'UUID: {self.__uuid} | Name: {self.__name} | Operator: {self.__operator} | Accepted: {self.__accepted} | Online: {self.__online} | Permission: {self.__permission}'