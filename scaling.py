import os
import sys
import subprocess
import time
import glob

# parameters: [1] Directory to original input files, [2] job file

# Given directory aggregate all mdp file paths into an array

directory = sys.argv[1]

mdp_files = glob.glob(os.path.join(directory, '*.mdp'))

home_directory = os.path.expanduser('~')

new_directory_name = 'scaling-files'

new_directory_path = os.path.join(home_directory, new_directory_name)

os.makedirs(new_directory_path, exist_ok=True)

print(f"Directory '{new_directory_path}' created successfully.")


# Copy any necessary input files into new location

os.system('cp ' + directory + "*.pdb  " + new_directory_path)
print("Copied any pdb files")

os.system('cp ' + directory + "*.gro  " + new_directory_path)

print("Copied any gro files")

os.system('cp ' + directory + "*.gro96  " + new_directory_path)

print("Copied any gro files")

os.system('cp ' + directory + "*.top  " + new_directory_path)

print("Copied any top files")

os.system('cp ' + directory + "*.itp  " + new_directory_path)

print("Copied any itp files")

os.system('cp ' + directory + "*.tpr  " + new_directory_path)

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
                file.write(f'nsteps      = 5000\n')
            else:
                file.write(line)
    print("Successfully updated " + new_file)


os.chdir(new_directory_path)

# Start batchscripts. 

job = sys.argv[2]
#store commands
commands = []
commands.append('sbatch --nodes=1 --time=00:30:00 --ntasks=128 ' + job)
commands.append('sbatch --nodes=1 --time=00:30:00 --ntasks=64 ' + job)
commands.append('sbatch --nodes=1 --time=00:30:00 --ntasks=32 ' + job)
commands.append('sbatch --nodes=1 --time=00:30:00 --ntasks=16 ' + job)

job_id = []
#Start jobs and store ID

job_id.append(subprocess.check_output(commands[0], shell=True).decode('utf-8').split()[-1])
print("Starting 128 core test " + str(job_id[0]))


data = [{},{},{},{}]

time.sleep(10)

#Store job info once completed

#128 cores

job_status128 = subprocess.check_output('jobinfo ' + job_id[0], shell=True).decode('utf-8')

while job_status128.splitlines()[7].split(': ')[1] != 'COMPLETED':
    time.sleep(0.25)
    job_status128 = subprocess.check_output('jobinfo ' + job_id[0], shell=True).decode('utf-8')

lines = job_status128.splitlines()
for line in lines: 
    line = line.split(': ')
    data[0][line[0].strip()] = line[1].strip()
print("Completed 128 core test")

#64 cores
job_id.append(subprocess.check_output(commands[1], shell=True).decode('utf-8').split()[-1])
print("Starting 64 core test ...  " + str(job_id[1]))

time.sleep(10)

job_status64 = subprocess.check_output('jobinfo ' + job_id[1], shell=True).decode('utf-8')

while job_status64.splitlines()[7].split(': ')[1] != 'COMPLETED':
    time.sleep(0.25)
    job_status64 = subprocess.check_output('jobinfo ' + job_id[1], shell=True).decode('utf-8')

lines = job_status64.splitlines()
for line in lines: 
    line = line.split(': ')
    data[1][line[0].strip()] = line[1].strip()
print("Completed 64 core test")

#32 cores
job_id.append(subprocess.check_output(commands[2], shell=True).decode('utf-8').split()[-1])

print("Starting 32 core test ... " + str(job_id[2]))

time.sleep(10)

job_status32 = subprocess.check_output('jobinfo ' + job_id[2], shell=True).decode('utf-8')

while job_status32.splitlines()[7].split(': ')[1] != 'COMPLETED':
    time.sleep(0.25)
    job_status32 = subprocess.check_output('jobinfo ' + job_id[2], shell=True).decode('utf-8')

lines = job_status32.splitlines()
for line in lines: 
    line = line.split(': ')
    data[2][line[0].strip()] = line[1].strip()
print("Completed 32 core test")


#16 cores

job_id.append(subprocess.check_output(commands[3], shell=True).decode('utf-8').split()[-1])

print("Starting 16 core test ... " + str(job_id[3]))

time.sleep(10)

job_status16 = subprocess.check_output('jobinfo ' + job_id[3], shell=True).decode('utf-8')
while job_status16.splitlines()[7].split(': ')[1] != 'COMPLETED':
    time.sleep(0.25)
    job_status16 = subprocess.check_output('jobinfo ' + job_id[3], shell=True).decode('utf-8')

lines = job_status16.splitlines()
for line in lines: 
    line = line.split(': ')
    data[3][line[0].strip()] = line[1].strip()
print("Completed 16 core test")

walltime_128_used = (int(data[0]['Used walltime'].split(':')[0]) * 3600) + (int(data[0]['Used walltime'].split(':')[1]) * 60) + int(data[0]['Used walltime'].split(':')[2])
walltime_64_used =  (int(data[1]['Used walltime'].split(':')[0]) * 3600) + (int(data[1]['Used walltime'].split(':')[1]) * 60) + int(data[1]['Used walltime'].split(':')[2])
walltime_32_used =  (int(data[2]['Used walltime'].split(':')[0]) * 3600) + (int(data[2]['Used walltime'].split(':')[1]) * 60) + int(data[2]['Used walltime'].split(':')[2])
walltime_16_used =  (int(data[3]['Used walltime'].split(':')[0]) * 3600) + (int(data[3]['Used walltime'].split(':')[1]) * 60) + int(data[3]['Used walltime'].split(':')[2])

print("128 Used wall: " + str(walltime_128_used) + " seconds")
print("64 Used wall: " + str(walltime_64_used) + " seconds")
print("32 Used wall: " + str(walltime_32_used) + " seconds")
print("16 Used wall: " + str(walltime_16_used) + " seconds")