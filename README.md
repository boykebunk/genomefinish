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
