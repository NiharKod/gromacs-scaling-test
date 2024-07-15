import os
import subprocess
import glob

# parameters: [1] Directory to original input files, [2] job file

# Given directory aggregate all mdp file paths into an array

directory = '/home/x-nkodkani/gromacs-files'
mdp_files = glob.glob(os.path.join(directory, '*.mdp'))

home_directory = os.path.expanduser('~')

new_directory_name = 'scaling-files'

new_directory_path = os.path.join(home_directory, new_directory_name)

os.makedirs(new_directory_path, exist_ok=True)

print(f"Directory '{new_directory_path}' created successfully.")


# Copy any necessary input files into new location

os.system('cp ' + directory + "/*.pdb  " + new_directory_path)
print("Copied any pdb files")

os.system('cp ' + directory + "/*.gro  " + new_directory_path)

print("Copied any gro files")

os.system('cp ' + directory + "/*.gro96  " + new_directory_path)

print("Copied any gro files")

os.system('cp ' + directory + "/*.top  " + new_directory_path)

print("Copied any top files")

os.system('cp ' + directory + "/*.itp  " + new_directory_path)

print("Copied any itp files")

os.system('cp ' + directory + "/*.tpr  " + new_directory_path)

print("Copied any tpr files")

# loop through all files and change number of steps to 100

for file_path in mdp_files:
    # Store the lines of a given file in lines array
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    file_name = os.path.basename(file_path)
    
    new_file = new_directory_path + '/' + file_name
    
    with open(new_file, "w") as file:
        for line in lines:
            if line.startswith('nsteps'):
                file.write(f'nsteps      = 150\n')
            else:
                file.write(line)
    print("Successfully updated " + new_file)


# Start batchscripts. 

job = 'gromacsjob.sh'

os.system('sbatch --nodes=1 --time=00:30:00 --ntasks=128 ' + job)

os.system('sbatch --nodes=1 --time=00:59:00 --ntasks=64 ' + job)

os.system('sbatch --nodes=1 --time=00:59:00 --ntasks=32 ' + job)

os.system('sbatch --nodes=1 --time=00:59:00 --ntasks=16 ' + job)

#print(mdp_files)
