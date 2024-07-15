#!/bin/bash
# FILENAME:  gromacsjob

#SBATCH -A myallocation # Allocation name (run 'mybalance' command to find) 
#SBATCH -p shared    #Queue (partition) name
#SBATCH --nodes=1 # Total # of nodes 
#SBATCH --ntasks=128 # Total # of MPI tasks 
#SBATCH --time=0:20:00 # Total run time limit (hh:mm:ss) 
#SBATCH --job-name myjob # Job name 
#SBATCH -o myjob.o%j    # Name of stdout output file
#SBATCH -e myjob.e%j    # Name of stderr error file

# Manage processing environment, load compilers and applications.
module --force purge
module load gcc/11.2.0
module load openmpi/4.0.6
module load gromacs/2021.2
module list

# Launch md jobs
#energy minimizations
grep -v HOH 1aki.pdb > 1AKI_clean.pdb
echo "15" | mpirun -np 1 gmx_mpi pdb2gmx -f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce
mpirun -np 1 gmx_mpi editconf -f 1AKI_processed.gro -o 1AKI_newbox.gro -c -d 1.0 -bt cubic
mpirun -np 1 gmx_mpi solvate -cp 1AKI_newbox.gro -cs spc216.gro -o 1AKI_solv.gro -p topol.top
mpirun -np 1 gmx_mpi grompp -f ions.mdp -c 1AKI_solv.gro -p topol.top -o ions.tpr
echo "13" | mpirun -np 1 gmx_mpi genion -s ions.tpr -o 1AKI_solv_ions.gro -p topol.top -pname NA -nname CL -neutral
mpirun -np 1 gmx_mpi grompp -f minim.mdp -c 1AKI_solv_ions.gro -p topol.top -o em.tpr
mpirun gmx_mpi mdrun -deffnm em
mpirun -np 1 gmx_mpi grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
mpirun gmx_mpi mdrun -deffnm nvt
mpirun -np 1 gmx_mpi grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
mpirun gmx_mpi mdrun -deffnm npt
mpirun -np 1 gmx_mpi grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_1.tpr
mpirun gmx_mpi mdrun -deffnm md_0_1