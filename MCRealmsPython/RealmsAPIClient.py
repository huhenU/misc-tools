class RealmsAPIClient:
    def __init__(self, accessToken:str, playerUUID:str, username:str, version:str):
        self.__accessToken:str = accessToken
        self.__playerUUID:str = playerUUID
        self.__username:str = username
        self.__version:str = version

        self.__baseUrl:str = 'https://java.frontendlegacy.realms.minecraft-services.net/'
        self.__cookies:dict = self.__setCookies()

    @property
    def cookies(self) -> dict:
        return self.__cookies

    @property
    def baseUrl(self) -> str:
        return self.__baseUrl

    def __setCookies(self) -> dict:
        return {
            'sid': f'token:{self.__accessToken}:{self.__playerUUID}',
            'user': self.__username,
            'version': self.__version
        }
