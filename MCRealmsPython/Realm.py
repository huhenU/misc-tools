import requests
import json
import time
from RealmsAPIClient import RealmsAPIClient
from Player import Player

class Realm:
    def __init__(self, realmID:int, realmClient:RealmsAPIClient):

        self.__realmID:int = str(realmID)
        self.__realmClient:RealmsAPIClient = realmClient

        details:dict = self.__fetchDetails()
        self.__owner:str = details.get('owner')
        self.__ownerUUID:str = details.get('ownerUUID')
        self.__name:str = details.get('name')
        self.__motd:str = details.get('motd')
        self.__state:str = details.get('state')
        self.__maxPlayers:int = details.get('maxPlayers')
        self.__activeSlot:int = details.get('activeSlot')
        self.__member:bool = details.get('member')
        self.__isHardcode:bool = details.get('isHardcore')

        #Gets populated when "joining" a server
        self.__networkProtocol:str = None
        self.__address:str = None
        self.__pendingUpdate:bool = False
        self.__regionName:str = None
        self.__serviceQuality:int = None

        self.__playerList:list = self.__getPlayerList()
        self.__onlinePlayers:list = self.__getOnlinePlayers()
        

    @property
    def owner(self) -> str:
        return self.__owner

    @property
    def ownerUUID(self) -> str:
        return self.__ownerUUID

    @property
    def realmID(self) -> int:
        return self.__realmID

    @property
    def name(self) -> str:
        return self.__name

    @property
    def motd(self) -> str:
        return self.__motd
    
    @property
    def state(self) -> str:
        return self.__state

    @property
    def maxPlayers(self) -> int:
        return self.__maxPlayers

    @property
    def activeSlot(self) -> int:
        return self.__activeSlot
    
    @property
    def member(self) -> bool:
        return self.__member
    
    @property
    def isHardcore(self) -> bool:
        return self.__isHardcode

    @property
    def playerList(self) -> bool:
        return self.__playerList

    @property
    def onlinePlayers(self) -> list:
        return self.__onlinePlayers

    @property
    def networkProtocol(self) -> str:
        return self.__networkProtocol

    @property
    def address(self) -> str:
        return self.__address
    
    @property
    def pendingUpdate(self) -> bool:
        return self.__pendingUpdate

    @property
    def regionName(self) -> str:
        return self.__regionName
    
    @property
    def serviceQuality(self) -> int:
        return self.__serviceQuality


    def __getPlayerList(self) -> list:
        details:dict = self.__fetchDetails()
        playerDetails:dict = details['players']
        players:list = []


        # Add "artificial" owner player. Online-status cannot be gotten this way for the owner -> return False TODO: Find a better way to handle this
        owner:Player = Player(
            uuid = self.ownerUUID,
            name = self.owner,
            operator = True,
            accepted = True,
            online = False,
            permission = 'OWNER'
        )
        players.append(owner)

        for player in playerDetails:
            player:Player = Player(
                uuid = player['uuid'],
                name = player['name'],
                operator = player['operator'],
                accepted = player['accepted'],
                online = player['online'],
                permission = player['permission']
            )
            players.append(player)

        return players

    def __fetchDetails(self) -> dict:
        url:str = self.__realmClient.baseUrl + 'worlds/' + self.__realmID
        response:Response = requests.get(url, cookies=self.__realmClient.cookies)
        details = response.json()

        return details

    def __getOnlinePlayers(self) -> list:
        url:str = self.__realmClient.baseUrl + 'activities/liveplayerlist'
        response:Response = requests.get(url, cookies=self.__realmClient.cookies)
        onlinePlayersInRealms:dict = response.json()
        onlinePlayers:list = []

        for realm in onlinePlayersInRealms['lists']:
            if realm['serverId'] == int(self.__realmID):
                onlinePlayerlist:list = json.loads(realm['playerList'])
                for onlinePlayer in onlinePlayerlist:
                    for invitedPlayer in self.__playerList:
                        if onlinePlayer['playerId'] == invitedPlayer.uuid:
                            onlinePlayers.append(invitedPlayer)

        return onlinePlayers


    def join(self, shouldWait:bool) -> None:
        url:str = self.__realmClient.baseUrl + 'worlds/' + self.__realmID + '/join'
        response:Response = requests.get(url, cookies=self.__realmClient.cookies)
        while response.text == 'Retry again later' and shouldWait:
            time.sleep(10)
            response:Response = requests.get(url, cookies=self.__realmClient.cookies)

        try: 
            joinDetails:dict = response.json()

            self.__networkProtocol = joinDetails['networkProtocol']
            self.__address = joinDetails['address']
            self.__pendingUpdate = joinDetails['pendingUpdate']
            self.__regionName = joinDetails['sessionRegionData']['regionName']
            self.__serviceQuality = joinDetails['sessionRegionData']['serviceQuality']
        
        except json.decoder.JSONDecodeError:
            pass


    def updateOnlinePlayers(self) -> None:
        self.__onlinePlayers:list = self.__getOnlinePlayers()


    def updatePlayerList(self) -> None:
        self.__playerList:list = self.__getPlayerList()
        