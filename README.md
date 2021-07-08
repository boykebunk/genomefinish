# genomefinish
Genome Finishing Programs

1) contigcoveragecorrector.jar
- correct PacBio assemblies from chimeric contigs by their coverage and reduce contig names
- required assembly.fasta & asembly_coverage.bed
- input: java -jar contigcoveragecorrector.jar MinimumCoverageThreshold(required) MaximumCoverage(optional) assembly.fasta assembly_coverage.bed
- output: assembly_cor.fasta

2) contigcreator.jar
- split sequcence file (also multifasta) at positions with N and discard contigs smaller than indicated threshold (clip ends)
- input: java -jar contigcreator.jar  contigThreshold(variable) name_sequence.fasta 
- output: name_contig_sequence.fasta

3) genomecirculator.jar
- delete overlapping back end of sequence identified for instance via NCBI blast in singlefasta and optinally align to indicated position e.g. replication system
- input:  java -jar genomecirculator.jar alignPostion(optional) cutposition(required, first overlapping sequence position) single_sequence.fasta
- output: single_sequence_circ.fasta

4) genomecirculator.py
- Rewritten version of the genomecirculator.jar with additional features. Run: genomecirculator.py chromosome_start chromosome_cut chromosome.fasta
NEW: Add "r" or "rev" to your call if your alignment orientation of your replication gene is reverse complement to your genome, e. g. use "12345r" as chromosome_start.
NEW: Want to include plasmids as well? Use on the multifasta: genomecirculator.py chromosome_start chromosome_cut plasmid1_start plasmid1_cut chromosome.fasta
NEW: Circularity has been already detected, e.g. in SMRTlink? Give 0 as cut-position fur the respective replicon.

- Program returns automatically the first 12 bp after the replication gene. Check that they are the same as the begin of dnaA.fasta
- Program returns automatically the sequence of the cutsite, before and after the cut
