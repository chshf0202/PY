import json
import shutil
import os

# ���������Ӧ�û�ƫ�ã�ȫѡ����ϵ�ṹ��Ӧ�ù��̡������߼���������ԣ�
# ���һ��������Ӧ���ɵ��û�ר�� node_edge_usr.json�ļ��洢��λ��
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