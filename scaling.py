import os
import glob

# Given directory aggregate all mdp file paths into an array

directory = '/home/x-nkodkani/gromacs-files'
mdp_files = glob.glob(os.path.join(directory, '*.mdp'))

home_directory = os.path.expanduser('~')

new_directory_name = 'scaling-files'

new_directory_path = os.path.join(home_directory, new_directory_name)

os.makedirs(new_directory_path, exist_ok=True)

print(f"Directory '{new_directory_path}' created successfully.")

os.system('cp ' + directory + "/*.pdb  " + new_directory_path)

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

#print(mdp_files)
