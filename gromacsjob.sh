#!/bin/bash
# FILENAME:  gromacsjob

#SBATCH -A myallocation # Allocation name (run 'mybalance' command to find) 
#SBATCH -p shared    #Queue (partition) name
#SBATCH --nodes=1 # Total # of nodes 
#SBATCH --ntasks=16 # Total # of MPI tasks 
#SBATCH --time=0:10:00 # Total run time limit (hh:mm:ss) 
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
mpirun -np 1 gmx_mpi grompp -f minim.mdp -c myjob.gro -p topol.top -o em.tpr
mpirun gmx_mpi mdrun -v -deffnm em
#nvt run 
mpirun -np 1 gmx_mpi grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
mpirun gmx_mpi mdrun -deffnm nvt
#npt run 
mpirun -np 1 gmx_mpi grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
mpirun gmx_mpi mdrun -deffnm npt
#md run
mpirun -np 1 gmx_mpi grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
mpirun gmx_mpi mdrun -deffnm md