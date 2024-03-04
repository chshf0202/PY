import json
import shutil
import os

# 五个参数对应用户偏好：全选、体系结构、应用工程、数理逻辑、编程语言；
# 最后一个参数对应生成的用户专属 node_edge_usr.json文件存储的位置
def genNodeEdgeForUsr(ifAll, ifArch, ifApp, ifMath, ifCode, outDir):
    usrSet = set()

    if ifAll or ifArch:
        with open("../model/node_Arch.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for node in data["nodes"]:
            usrSet.add(node["label"])

    if ifAll or ifApp:
        with open("../model/node_App.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for node in data["nodes"]:
            usrSet.add(node["label"])

    if ifAll or ifMath:
        with open("../model/node_Math.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for node in data["nodes"]:
            usrSet.add(node["label"])

    if ifAll or ifCode:
        with open("../model/node_Code.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for node in data["nodes"]:
            usrSet.add(node["label"])

    nodesLis = list()
    edgesLis = list()

    with open("../model/node_edge.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for node in data["nodes"]:
        if node["label"] in usrSet:
            nodeUsr = {"color": "#97c2fc", "id": node["id"], "label": node["label"], "shape": "dot"}
            nodesLis.append(nodeUsr)
    for edge in data["edges"]:
        if edge["from"] in usrSet and edge["to"] in usrSet:
            edgeUsr = {"from": edge["from"], "to": edge["to"]}
            edgesLis.append(edgeUsr)

    fout = open('node_edge_usr.json', 'w', encoding='utf-8')
    strTo = '{ \"nodes\" : ' + str(nodesLis) + ', \"edges\" : ' + str(edgesLis) + '}'
    strTo = strTo.replace("'", "\"")
    fout.write(strTo)
    fout.close()

    shutil.move('node_edge_usr.json', os.path.join(outDir, 'node_edge_usr.json'))