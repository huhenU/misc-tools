import requests
from RealmsAPIClient import RealmsAPIClient
from Realm import Realm

class RealmsManager:
    def __init__(self, realmClient:RealmsAPIClient):
        self.__realmClient:RealmsAPIClient = realmClient
        self.__realms:list = self.__getRealms()

    @property
    def realms(self) -> list:
        return self.__realms


    def __getRealms(self) -> list:
        url:str = self.__realmClient.baseUrl + 'worlds'
        response:Response = requests.get(url, cookies=self.__realmClient.cookies)
        realmsList:dict = response.json()
        realms:list = []

        for realm in realmsList['servers']:
            realm:Realm = Realm(
                realmID = realm['id'],
                realmClient = self.__realmClient
            )
            realms.append(realm)

        return realms