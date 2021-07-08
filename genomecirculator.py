#!/usr/bin/env python
import sys
from Bio import SeqIO

if len(sys.argv) < 3: 
    sys.stderr.write("Usage: genomecirculator.py chromosome_start[f|r] chromosome_cut [plasmid1_start[f|r] plasmid1_cut ...] genome.fasta\n")
    sys.stderr.write("    OR genomecirculator.py replicon_cut genome.fasta")
    sys.exit(1)
else:
    file = sys.argv[len(sys.argv)-1]
    records = SeqIO.parse(file, "fasta")
    circ = open(file.replace(".fasta", "_circ.fasta").replace(".fsa", "_circ.fsa").replace(".fna", "_circ.fna"), "w")
    #Cut-Mode if only two CL arguments are provided (backwards compatibility to old GenomeCirculator)
    #Note that in Cut-Mode only the first fasta-entry is handled and cut
    if len(sys.argv) == 3:
        cutSite = int(sys.argv[1]) 
        cutSite -= 1 #correction (BLAST values are given +1)
        record = records.next()
        print(record.id + ":")
        print("Cutting replicon to " + str(cutSite) + " bp (given site is cut off)")
        print("CHECK: Cutsite: " +  record.seq[cutSite-12:cutSite].upper())
        record.seq = record.seq[0:cutSite]
        SeqIO.write(record, circ, "fasta")
    #Replicon circ as usual with given start and cut position
    #NEW:Circularization of all replicons at once WITH handling of reverse complement rep genes
    elif len(sys.argv) >= 4:
        #hold start and cut positions in different lists
        starts = [] #list of start positions of rep genes
        start_oris_fwd = [] #list of forward/reverse rep gene orientations (boolean)
        cuts = [] #list of cut_positions
        for i in range(1,len(sys.argv)-1,2):
            start = int(sys.argv[i].replace("fwd","").replace("rev","").replace("f","").replace("r","")) 
            fwd = True #set forward orientation of rep gene
            if "r" in sys.argv[i]:
                fwd = False
            cut = int(sys.argv[i+1]) - 1 #correction (BLAST values are given +1)
            starts.append(start - 1) #correction (BLAST values are given +1)
            start_oris_fwd.append(fwd)
            cuts.append(cut)
        for record in records:
            #only those records are handled, where positions are given
            if len(starts) > 0:            
                start = starts.pop(0)
                fwd = start_oris_fwd.pop(0)
                cut = cuts.pop(0)
                #if cutposition set to 0 perform no cut at all
                if (cut <= 0):
                    cut = len(record.seq)
                assert(start < cut),"ERROR: Start position has to be smaller than cut position!"
                print(record.id + ":")
                if fwd:
                    print("Start of rep gene is set to " + str(start+1) + " bp (given site is begin of start codon)");
                    print("CHECK: First 12 bp of rep gene: " + record.seq[start:start+12].upper());
                    print("Cutting replicon to " + str(cut) + " bp (given site is cut off)");
                    print("CHECK: Cutsite: " + record.seq[cut-12:cut].upper() + record.seq[0:12].lower());
                    record.seq = record.seq[start:cut] + record.seq[0:start] #only this command performs the final circularization ;)
                else:
                    print("Switching to revcomp mode!")
                    print("Start of rep gene is set to " + str(start+1) + " bp (given site is begin of start codon)");
                    print("CHECK: First 12 bp of rep gene: " + record.seq[start-11:start+1].reverse_complement().upper());
                    print("Cutting replicon to " + str(cut) + " bp (given site is cut off)");
                    print("CHECK: Cutsite: " + record.seq[cut-12:cut].upper() + record.seq[0:12].lower());
                    #this method ensures alway right-hand cut (where assemblies are assumed to have poor qualities)
                    record.seq = record.seq[0:start+1].reverse_complement() + record.seq[start+1:cut].reverse_complement()  #only this command performs the final circularization ;)            
                SeqIO.write(record, circ, "fasta")
    circ.close()
