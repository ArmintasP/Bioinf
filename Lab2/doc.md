---
title: 2 Homework Assignment
author: Armintas Pakenis
affiliation: Vilnius University
email: armintas.pakenis@mif.stud.vu.lt
date: 2022-11-18
abstract: Phylogenetic trees of Betacoronaviruses genomes related to NC_045512
lang: en
...

# Introduction

Phylogenetic trees were generated following homework instructions. Outputs of some inner steps can be found [here](https://github.com/ArmintasP/Bioinf/tree/main/Lab2). The results consist of two trees: one without an outgroup and the other with MN514967.7 as an outgroup.

# Methodology
The following sequences were collected from[NCBI](https://www.ncbi.nlm.nih.gov/):
- Betacoronaviruses relating to NC_045512 with coverage better than 50%.
- NC_045512 sequence itself.
- MN514967.1 (camel coronavirus).

Genomes of organisms beloning to SARS-CoV-2 were explicitly excluded to isolate the subset of interest and avoid unnecessary clustering caused by other human coronavirus variants (as NC_045512 will be more closer to them).

# Results
Phylogenetic trees are scaled to emphasize differences between different sequences.

Phylogenetic tree without an outgroup can be found [here](https://raw.githubusercontent.com/ArmintasP/Bioinf/main/Lab2/5/tree_outgrouped.png).

Phylogenetic tree with an outgroup can be found [here](https://raw.githubusercontent.com/ArmintasP/Bioinf/main/Lab2/5/tree_outgrouped.png).

# Conclusion
### Evolution of Covid-19

Judging by the results of both trees, NC_045512 closely clustered with sarbecoviruses, bat coronaviruses. Pangolin coronaviruses are not far away from that cluster.

### Outgrouping MN514967.1

Camel coronavirus had the largest distance and was not close to any cluster in the phylogenetic tree. Hence, it became sound to make a tree with camel coronavirus outgrouped to get more accurracy. The result of outgrouping is evident - there are 3 major clusters, while before there were more than 6.

Nonetheless, the interpretation of NC_045512 hosts' chain would not differ a lot even, except for the case that camel coronavirus would have a common ancestor as NC_045512.

### Evolution of Urbani SARS

Urbani SARS viruses have same came from the same parent as bat coronavirus (KP886808.1). In addition, their ancestor is close to the family of bat coronaviruses. That family of bat coronaviruses is more distant from bat coronaviruses family clustered next to NC_045512. The relationship between NC_045512 and Urbani viruses is relatively miniscule.


### The Origin of Palm Civet viruses

The origin of Palm Civet viruses remain unknown as it was not included after applying various filtering criteria.