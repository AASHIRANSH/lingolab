import json
# from pathlib import Path
# paths = sorted(Path("database/games/levels/").iterdir(), key=os.path.getmtime)
# levels = os.listdir("database/games/levels/")

# lv_780 = []
# for x in range(1,781):
#     with open("database/games/levels/lv ("+str(x)+").json") as f:
#         lv = json.load(f)
#         for y in lv.values():
#             lv_780.append(y)
with open("database/games/lvs.json") as f:
    lvs = json.load(f)

# levs = []
# for x,y in enumerate(lvs):
#     if "c" in y.keys():
#         levs.append([
#             x+1,
#             y["b"],
#             [y["c"],y["d"]],
#             y["e"]
#         ])
# with open("database/games/lvs_2.json","w+") as f:
#     json.dump(levs,fp=f,indent=4)
