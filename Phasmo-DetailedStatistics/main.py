import json
import re
import ES3Decrypt
import platform
import os
import argparse
import csv
import collections

def loadSaveData(args):
    if not args.path:
        if platform.system() == 'Windows':
            saveDir = os.path.join(
                os.path.dirname(os.environ.get('LOCALAPPDATA')),
                'LocalLow', 'Kinetic Games', 'Phasmophobia'
            )
        else:
            homeDir = os.path.expanduser('~')
            saveDir = os.path.join(
                homeDir,
                '.local', 'share', 'Steam', 'steamapps', 'compatdata', '739630',
                'pfx', 'drive_c', 'users', 'steamuser', 'AppData',
                'LocalLow', 'Kinetic Games', 'Phasmophobia'
            )

        savePath = os.path.join(saveDir, 'SaveFile.txt')
    
        if not os.path.exists(savePath):
            raise Exception('SaveFile not in default location. Specify path manually using the --path cli flag')
    
    else:
        savePath = args.path
    
    password = 't36gref9u84y7f43g'
    decryptedBinary = ES3Decrypt.decrypt(savePath, password)
    decryptedText = decryptedBinary.decode('utf-8', errors='ignore')

    # Fix unquoted numeric keys inside playedMaps value
    fixedText = re.sub(r'(\{|,)(\s*)(\d+)(\s*):', r'\1"\3":', decryptedText)
    saveData = json.loads(fixedText)
    return saveData


def generate_stats_rows(saveData):
    # ---Player---
    playerStats = [
        'amountOfBonesCollected','distanceTravelled','sanityLost','sanityGained',
        'phrasesRecognized','timeSpentInvestigating','timeSpentInDark','timeSpentInLight',
        'timeSpentInTruck','timeSpentInGhostsRoom','timeSpentBeingChased','ghostsRepelled',
        'photosTaken','videosTaken','soundsTaken','diedAmount','revivedAmount','moneyEarned',
        'moneySpent','itemsBought','itemsLost','ghostsIdentifiedAmount','ghostsMisidentifiedAmount',
        'objectivesCompleted','amountOfCursedPossessionsUsed','amountOfCursedHuntsTriggered'
    ]
    for stat in playerStats:
        yield ('Player', stat, saveData[stat]['value'])

    # ---Ghost---
    ghostStats = [
        'ghostDistanceTravelled','amountOfGhostInteractions','doorsMoved','objectsUsed',
        'lightsSwitched','fuseboxToggles','amountOfGhostEvents','abilitiesUsed','roomChanged',
        'timeInFavouriteRoom','amountOfGhostHunts','totalHuntTime'
    ]
    for stat in ghostStats:
        yield ('Ghost', stat, saveData[stat]['value'])

    # ---Maps---
    mapIdKeys = {
        '0':'Sunny Meadows Restricted','1':'Sunny Meadows','2':'Bleasdale Farmhouse',
        '3':'Camp Woodwind','4':'Maple Lodge Campsite','5':'42 Edgefield Road',
        '6':'Grafton Farmhouse','7':'Prison','8':'Asylum','9':'10 Ridgeview Court',
        '10':'Brownstone High School','11':'6 Tanglewood Drive','12':'13 Willow Street',
        '13':'Unbekannt','14':'Point Hope'
    }
    for k,v in saveData['playedMaps']['value'].items():
        yield ('Maps', mapIdKeys.get(k,k), v)

    # ---Kills---
    for name,val in saveData['ghostKills']['value'].items():
        yield ('GhostKills', name, val)

    # ---Encounters---
    for name,val in saveData['mostCommonGhosts']['value'].items():
        yield ('GhostEncounters', name, val)

    # ---Bones---
    boneNames = {
        'Bone0':'Femur','Bone1':'Foot','Bone2':'Fibula','Bone3':'Hand',
        'Bone4':'Humerus','Bone5':'Jaw','Bone6':'Pelvis','Bone7':'Ulna',
        'Bone8':'Ribcage','Bone9':'Scapula','Bone10':'Skull','Bone11':'Spine','Bone12':'Radius'
    }
    for k in [key for key in saveData if key.startswith('Bone')]:
        yield ('Bones', boneNames.get(k,k), saveData[k]['value'])

    # ---Cursed Objects---
    objectStatistics = [
        'MusicBoxesFound','MonkeyPawFound','MirrorsFound','SummoningCirclesUsed','VoodoosFound','OuijasFound'
    ]
    for obj in objectStatistics:
        yield ('CursedObjects', obj, saveData[obj]['value'])

    # ---Tarot---
    tarotStatistics = [
        'TarotWheel','TarotDeath','TarotTower','TarotFool','TarotHangedMan',
        'TarotHermit','TarotDevil','TarotMoon','TarotSun','TarotPriestess'
    ]
    totalCards = sum(saveData[card]['value'] for card in tarotStatistics)
    yield ('Tarot', 'TotalCardsDrawn', totalCards)
    for card in tarotStatistics:
        yield ('Tarot', card, saveData[card]['value'])


def printStats(rows):
    grouped = collections.defaultdict(list)
    for cat,name,val in rows:
        grouped[cat].append((name,val))

    for cat in grouped:
        print(f"---{cat}---")
        maxlen = max(len(name) for name,_ in grouped[cat])
        for name,val in grouped[cat]:
            print(f"{name.ljust(maxlen)}   {val}")
        print()

def exportCsv(rows, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Category', 'Name', 'Value'])
        for cat, name, val in rows:
            writer.writerow([cat, name, val])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', help='Export to csv instead of printing')
    parser.add_argument('--path', help='Specify savefile location manually')
    args = parser.parse_args()

    saveData = loadSaveData(args)
    rows = list(generate_stats_rows(saveData))

    if args.csv:
        exportCsv(rows, args.csv)
    else:
        printStats(rows)
    
if __name__ == '__main__':
    main()