#!/usr/bin/env python3

import copy
import random


def CreatePlayers(numPlayers: int) -> list:
    players = [i for i in range(1, numPlayers+1)]
    if numPlayers % 2 != 0:
        players.append(0)
    return players


def GenerateMatchRounds(players: list, matchesPerPlayer: int) -> list:
    matchesTotal = []
    matchesRound = []

    # Init first round.
    pairs = len(players) // 2
    for i in range(0, pairs):
        matchesRound.append([players[i], players[-(i+1)]])
    matchesTotal.append(copy.deepcopy(matchesRound))

    # Generate next rounds.
    for i in range(1, len(players)-1):
        ind = players.index(matchesRound[0][0])
        for j in range(1, pairs):
            matchesRound[pairs-j][1] = players[ind]
            ind = (ind+1) % (len(players)-1)
        for j in range(0, pairs):
            matchesRound[j][0] = players[ind]
            ind = (ind+1) % (len(players)-1)
        matchesTotal.append(copy.deepcopy(matchesRound))

    return matchesTotal


def DeleteDummyMatches(matchesTotal: list):
    # Delete dummpy matches.
    if matchesTotal[0][0][-1] == 0:
        for matchesRound in matchesTotal:
            matchesRound.pop(0)


def DeleteMatches(matchesTotal: list, numPlayers: int, numDel: int) -> list:
    matchesPlayer = {}
    for i in range(1, numPlayers+1):
        matchesPlayer[i] = numDel * 2 // numPlayers

    matchesAll = copy.deepcopy(matchesTotal)
    rounds = len(matchesAll)
    for i in range(0, numDel):
        times = numPlayers * 100
        while True:
            if times <= 0:
                return None
            round = random.randint(0, rounds-1)
            matchesRound = matchesAll[round]
            pairs = len(matchesRound)
            if pairs == 0:
                times -= 1
                continue
            ind = random.randint(0, pairs-1)
            match = matchesRound[ind]
            if matchesPlayer[match[0]] * matchesPlayer[match[-1]] == 0:
                times -= 1
                continue
            matchesPlayer[match[0]] -= 1
            matchesPlayer[match[-1]] -= 1
            matchesRound.pop(ind)
            break

    return matchesAll


def CheckMachesNum(matchesTotal: list,
                   numPlayers: int, matchesPerPlayer: int) -> bool:
    matchesPlayer = {}
    for i in range(1, numPlayers+1):
        matchesPlayer[i] = 0

    for matchesRound in matchesTotal:
        for match in matchesRound:
            matchesPlayer[match[0]] += 1
            matchesPlayer[match[-1]] += 1

    for v in matchesPlayer.values():
        if v != matchesPerPlayer:
            return False

    return True


def Draw(numPlayers: int, matchesPerPlayer: int) -> list:
    players = CreatePlayers(numPlayers)
    matchesTotal = GenerateMatchRounds(players, matchesPerPlayer)
    numDel = (numPlayers-1-matchesPerPlayer) * numPlayers // 2
    if numDel != 0:
        DeleteDummyMatches(matchesTotal)
        while True:
            matchesAll = DeleteMatches(matchesTotal, numPlayers, numDel)
            if matchesAll is not None:
                break
        if not CheckMachesNum(matchesAll, numPlayers, matchesPerPlayer):
            print("Error!")
        matchesTotal = matchesAll

    return matchesTotal


if __name__ == "__main__":
    names = input("请输入选手姓名列表（以英文,分隔）：").split(",")
    print("选手人数为{}，现重新排序。".format(len(names)))
    random.shuffle(names)
    matchesPerPlayer = int(input("请输入每人循环的场数："))
    if len(names) * matchesPerPlayer % 2 != 0:
        print("选手人数为奇数时，每人循环的场数必须为偶数。错误退出！")
        exit(1)

    matchesTotal = Draw(len(names), matchesPerPlayer)

    print("\n========--------  轮次场次表  --------========")
    for i, r in enumerate(matchesTotal):
        print("第{:2d}轮\t".format(i+1), end="")
        for m in r:
            name1 = names[m[0]-1]
            name2 = names[m[-1]-1] if m[-1] != 0 else "轮空"
            print("{}-{}\t".format(name1, name2), end="")
        print("")

    print("\n========--------  选手计分表  --------========")
    for i, name in enumerate(names):
        print("{}-\t\t".format(name), end="")
        id = i+1
        for r in matchesTotal:
            for m in r:
                if m[-1] == 0:
                    continue
                if m[0] == id or m[-1] == id:
                    peer = m[-1] if m[0] == id else m[0]
                    print("{}\t".format(names[peer-1]), end="")
        print("")

    print("")
