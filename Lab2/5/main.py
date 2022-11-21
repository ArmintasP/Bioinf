from ete3 import Tree, TreeStyle

root = "MN514967.1-Dromedary-camel-coronavirus-HKU23-isolate-DcCoV-HKU23/camel/Nigeria/NV1385/2016"
tree = Tree("/home/cat/Documents/Bioinformatika/Lab2/py/tree.out", format=1)

ts = TreeStyle()
ts.show_branch_length = True
ts.scale = 6000
ts.branch_vertical_margin = 10

filec = open("tree_not_outgrouped.txt", "w")
print(tree, file = filec)

tree.render("tree_not_outgrouped.png", tree_style=ts)
#tree.show(tree_style=ts)


print("***")

filec = open("tree_outgrouped.txt", "w")
tree.set_outgroup(root)
print(tree, file=filec)

tree.render("tree_outgrouped.png", tree_style=ts)
#tree.show(tree_style=ts)
