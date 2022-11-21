from ete3 import Tree
root = "MN514967.1-Dromedary-camel-coronavirus-HKU23-isolate-DcCoV-HKU23/camel/Nigeria/NV1385/2016"
tree = Tree("/home/cat/Documents/Bioinformatika/Lab2/py/tree.out", format=1)

filec = open("tree_not_outgrouped.txt", "w")

print(tree, file = filec)


print("***")

filec = open("tree_outgrouped.txt", "w")
tree.set_outgroup(root)
print(tree, file=filec)

tree.show(0)
