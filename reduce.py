# Copyright (c) 2021 Christian Balbin
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import csv
import json
import os
from scipy import stats
import numpy as np
from collections import defaultdict
import pickle
#from epitopedia.app import config
#from epitopedia.viz.figure import plot_dist
from figure import plot_dist

def reduce_results(path):
    with open(path) as input_handle:
        data = json.load(input_handle)

    basename = os.path.basename(path).rstrip(".json")

    motif_dict = defaultdict(list)
    #print(data)
    #paramters = data["parameters"]

    data = data["results"]

    data = [dat for datum in data for dat in datum if dat]

    for hit in data:

        if hit == None:
            continue
        print(hit)
        blasthit = hit["blasthit"]
        epitope = hit["hitepitopedata"]
        motifs = hit["pdb_motif_hits"]

        for pdb_hit in motifs:
            for motif_type in pdb_hit:
                # print(motif_type["motif_seq"])
                if motif_type["TMalign_RMSD"] == " NaN":

                    continue
                #print(motif_type["TMalign_RMSD"])
                #x = input()
                motif_type["TMalign_RMSD"] = float(motif_type["TMalign_RMSD"].split(',')[0])
                motif_dict[motif_type["motif_seq"]].append(
                    {
                        "SeqBMM Input Struc Res Nums": motif_type["motif_res_nums_query"],
                        "SeqBMM Acc": motif_type["query_acc_motif"],
                        "EPI_PDB Epi Source Acc": motif_type["query"],
                        "EPI_PDB Rep PDB": motif_type["target"],
                        "EPI_PDB Qcov": motif_type["qcov"],
                        "EPI_PDB Pident": motif_type["pident"],
                        "EPI_PDB Evalue": motif_type["evalue"],
                        "mmCIF_SEQ Rep Res": motif_type["seqres"],
                        "mmCIF_SEQ Rep Solv": motif_type["seqsolv"],
                        "mmCIF_SEQ Rep Num": motif_type["seqnums"],
                        #"mmCIF_SEQ lplddt": motif_type["lplddt"],
                        #"mmCIF_SEQ gplddt": motif_type["gplddt"],
                        "mmCIF_SEQ motif lplddt": motif_type["avg_motif_lplddt"],
                        #"mmCIF_SEQ title": motif_type["pdb_title"],
                        #"mmCIF_SEQ species": motif_type["pdb_species"],
                        #"mmCIF_SEQ AF": motif_type["isAF"],
                        "EPI_PDB Rep Res Nums": motif_type["motif_res_nums_target"],
                        "EPI_PDB Input Dice Path": motif_type["query_struc_dice_path"],
                        "EPI_PDB Rep Dice Path": motif_type["target_struc_dice_path"],
                        "EPI_PDB TMalign RMSD": motif_type["TMalign_RMSD"],
                        "EPI_PDB Epi Score": (1/float(motif_type["TMalign_RMSD"])*len(motif_type["motif_seq"]) if float(motif_type["TMalign_RMSD"]) else 1/float(0.01)*len(motif_type["motif_seq"])),
                        #"EPI_PDB Epi Score": if float(motif_type["TMalign_RMSD"]) (1/float(motif_type["TMalign_RMSD"])*len(motif_type["motif_seq"])) else 1/float(0.01)*len(motif_type["motif_seq"])),
                        "EPI_PDB TMalign TMscore": motif_type["TMalign_TMscore"],
                        "EPI_PDB Epi Score Z Score": False,
                        "EPI_PDB TMalign RMSD Z Score": False,
                        "EPI_PDB TMalign PDB": os.path.basename(motif_type["TMalign_PDB_file"]),
                        "EPI_PDB Rep Acc": motif_type["target_acc_motif"],
                        "EPI_PDB Input Motif Perc Acc": motif_type["query_perc_acc"],
                        "EPI_PDB Rep Motif Perc Acc": motif_type["target_perc_acc"],
                        "EPI_PDB Perc Acc Agree": motif_type["perc_acc_agree"],
                        "IEDB_FILT Epitope ID": epitope["epitope_id"],
                        "IEDB_FILT Epitope Seq": epitope["linear_peptide_seq"],
                        "IEDB_FILT Source Seq Acc": epitope["source_antigen_accession"],
                        "IEDB_FILT Start Pos": epitope["starting_position"],
                        "IEDB_FILT Stop Pos": epitope["ending_position"],
                        "IEDB_FILT Source DB": epitope["database"],
                        "IEDB_FILT Source Title": epitope["name"],
                        "IEDB_FILT Source Taxid": epitope["organism_id"],
                        "IEDB_FILT Source Org": epitope["organism_name"],
                        "IEDB_FILT Source Seq": epitope["sequence"],
                        "IEDB_FILT Iacc": epitope["internal_source_seq_acc"],
                        #"EPI_SEQ Input Structure": blasthit["query_accession"],
                        #"EPI_SEQ Epitope ID": blasthit["subject_accession"],
                        #"EPI_SEQ Input Structure Seq Start Pos": blasthit["query_start"],
                        #"EPI_SEQ Input Structure Seq Stop Pos": blasthit["query_end"],
                        #"EPI_SEQ Epitope Start Pos": blasthit["subject_start"],
                        #"EPI_SEQ Epitope End Pos": blasthit["subject_end"],
                        #"EPI_SEQ Aln Input Struc Seq": blasthit["aln_query_seq"],
                        #"EPI_SEQ Aln Epitope Seq": blasthit["aln_subject_seq"],
                        #"EPI_SEQ Evalue": blasthit["evalue"],
                        #"EPI_SEQ Qcov": blasthit["qcovs"],
                        #"EPI_SEQ Pident": blasthit["pident"],
                        #"EPI_SEQ Epitope Taxid": blasthit["staxid"],
                        #"EPI_SEQ Span Ranges": blasthit["match_ranges"],
                        #"EPI_SEQ Aln Cigar": blasthit["cigar"],
                        #"EPI_SEQ Span Lengths": blasthit["match_lengths"],
                        #"EPI_SEQ Span Seqs": blasthit["submatch_seqs"],
                        #"PDB_DSSP Input Struc ASA": blasthit["acc_seq"],
                        #"mmCIF_SEQ Input Struc Solv Seq": blasthit["pdb_seqsolv"],
                        #"mmCIF_SEQ Input Struc Res Nums": blasthit["pdb_seqnums"],
                    }
                )
                try:
                #if (float(motif_type["TMalign_RMSD"])):
                   motif_dict[motif_type["motif_seq"]][len(motif_dict[motif_type["motif_seq"]])-1]["EPI_PDB Epi Score"] = 1/float(motif_type["TMalign_RMSD"])*len(motif_type["motif_seq"])
                #else:
                except:
                   motif_dict[motif_type["motif_seq"]][len(motif_dict[motif_type["motif_seq"]])-1]["EPI_PDB Epi Score"] = 1/float(0.01)*len(motif_type["motif_seq"])

    for motif, data in motif_dict.items():
        motif_dict[motif] = sorted(data, key=lambda x: x["EPI_PDB TMalign RMSD"])

    motif_dict = {k: v for k, v in sorted(motif_dict.items(), key=lambda item: item[1][0]["EPI_PDB TMalign RMSD"])}

    with open(f"{basename}_ranked.tsv", "w") as outhandle:
        outhandle.write("SeqBMM Motif\t")
        #print(motif_dict.items())
        w = csv.DictWriter(outhandle, list(motif_dict.items())[0][1][0].keys(), delimiter="\t")
        w.writeheader()
        for motif, data in motif_dict.items():

            for dat in data:
                outhandle.write(f"{motif}\t")
                w.writerow(dat)



    with open(f"{basename}.json", "w") as output_handle:
        #json.dump({"parameters": paddramters, "results": motif_dict}, output_handle)
        json.dump({"results": motif_dict}, output_handle)

    for key, instances in motif_dict.items():
        filtered_instacnes = []
        acc_visited = []
        for instance in instances:
            i_acc = int(instance["IEDB_FILT Iacc"])
            if i_acc in acc_visited:
                continue
            else:
                acc_visited.append(i_acc)
                filtered_instacnes.append(instance)

        motif_dict[key] = filtered_instacnes

    # all dicts are ordered dicts in 3.7 +, this breaks if using lower version of python.

    with open(f"{basename}_best.tsv", "w") as outhandle:
        outhandle.write("SeqBMM Motif\t")
        w = csv.DictWriter(outhandle, list(motif_dict.items())[0][1][0].keys(), delimiter="\t")
        w.writeheader()
        for motif, data in motif_dict.items():

            for dat in data:
                outhandle.write(f"{motif}\t")
                w.writerow(dat)








    #generate viz

    epi_scores = []
    rmsds = []
    lens = []
    for key, instances in motif_dict.items():
        for instance in instances:
            epi_scores.append(instance["EPI_PDB Epi Score"])
            rmsds.append(float(instance["EPI_PDB TMalign RMSD"]))
            lens.append(len(key))

    epi_scores_z_dist = stats.zscore(epi_scores)
    rmsds_z_dist = stats.zscore(rmsds)

    # print(epi_scores_z_dist)
    # print(rmsds_z_dist)
    with open(f"{basename}_exp.pickle", "wb") as outhandle:
        pickle.dump({"epi_scores":epi_scores,"rmsds":rmsds,"epi_scores_z_dist":epi_scores_z_dist,"rmsds_z_dist":rmsds_z_dist,"lens":lens},outhandle)


    if (True):
        print("[bold green]Generating z-dist plots")
        index = 0
        for key, instances in motif_dict.items():
            for instance_index, instance in enumerate(instances):
                instance["EPI_PDB Epi Score Z Score"] = epi_scores_z_dist[index]
                instance["EPI_PDB TMalign RMSD Z Score"] = rmsds_z_dist[index]
                

                plot_dist(rmsds, rmsds_z_dist[index], f"rmsd_{key}_{instance_index}.png", label="RMSD (Å)")
                plot_dist(epi_scores, epi_scores_z_dist[index], f"episcore_{key}_{instance_index}.png", label="Epi Score (residues/Å)")
                index += 1
                
            # the more residues you have without reducing the angstrom value the better
            
    
    
    with open(f"{basename}_best.json", "w") as output_handle:
        json.dump({"results": motif_dict}, output_handle)
