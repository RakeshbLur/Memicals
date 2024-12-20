import random as rand
import subprocess as sp
from datetime import datetime
import os
import sys

data_pattern = (
    "12341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234",
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
    "00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff",
    "f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0",
    "fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98fedcba98",
    "cafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeefcafebeef",
    "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
    "11235813111235813111235813111235813111235813111235813111235813111235813111235813111235813111235813111235813111235813111235813111",
    "abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123f0",
    "5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa",
    "0f0e0d0c0b0a090807060504030201000f0e0d0c0b0a090807060504030201000f0e0d0c0b0a090807060504030201000f0e0d0c0b0a09080706050403020100",
    "99999999bbbbbbbbccccccccddddddddeeeeeeeeffffffff88888888aaaaaaaaffffffffbbbbbbbb99999999ddddddddcccccccc88888888eeeeeeee11111111",
    "24682468246824682468246824682468246824682468246824682468246824682468246824682468246824682468246824682468246824682468246824682468",
    "13571357135713571357135713571357135713571357135713571357135713571357135713571357135713571357135713571357135713571357135713571357",
    "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    "8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff8888ffff",
    "abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321abcd4321",
    "77777777777777779999999999999999888888888888888855555555555555554444444444444444333333333333333322222222222222221111111111111111",
    "a102030405060708090a0b0c0d0e0f10a112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f40",
    "ffffffff00000000eeeeeeee11111111dddddddd22222222cccccccc33333333bbbbbbbb44444444aaaaaaaa55555555aaaaaaaa55555555bbbbbbbb44444444",
    "aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555aaaa5555",
    "aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55aa55",
    "a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5",
    "12345678123456781234567812345678123456781234567812345678123456781234567812345678123456781234567812345678123456781234567812345678",
    "12345678876543211234567887654321123456788765432112345678876543211234567887654321123456788765432112345678876543211234567887654321",
    "11223344556677881122334455667788112233445566778811223344556677881122334455667788112233445566778811223344556677881122334455667788",
    "0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff",
    "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789",
)

#data_pattern = (
#    "a102030405060708090a0b0c0d0e0f10a112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f40",
#)

def read_memory_data(address):
    # Convert the address to a hexadecimal string
    address_hex = hex(address)
    
    # Define the command to be executed
    command = ["m", "dd", address_hex]
    
    try:
        # Execute the command
        result = sp.run(command, check=True, stdout=sp.PIPE, stderr=sp.PIPE)
        # Parse the output of the command
        address_data_dict = {}
        lines = result.stdout.decode(errors='ignore').strip().split('\n')
        for i in range(0, len(lines), 4):
            combined_data = ""
            for j in range(4):
                if i + j < len(lines):
                    parts = lines[i + j].strip().split()
                    #if len(parts) >= 2:
                    combined_data += ''.join(parts[1:-1])
            if combined_data:
                address_data_dict[hex(address + i * 16)] = combined_data
        
        address_data_dict.popitem()
        return address_data_dict
        
    except sp.CalledProcessError as e:
        # Return the error message if the command fails
        return f"Error for address {address_hex}: {e.stderr.decode(errors='ignore')}"
        
def data_verification(pattern, address_range):
    
    err     = 0
    pattern = transform_pattern(pattern)
    # Loop through the address range
    #print(address_range)
    for address in address_range:
        # Read memory data
        data_dict = read_memory_data(address)
        #print(data_dict)
        
        # Check if the data_dict is a dictionary
        if isinstance(data_dict, dict):
            for addr, data in data_dict.items():
                # Compare the data with the pattern
                if pattern != data:
                    print(f"Address {addr}: Data does not match the pattern.")
                    print(f"Pattern: {pattern}")
                    print(f"Data   : {data}")
                    print("\n")
                    err = -1
                    break
                else:
                    print(f"Address {addr}: Data match the pattern.")
                    #print(f"Address {addr}: Data matched the pattern.")
                    #continue
        else:
            print(data)  # Print the error message
    return err
            

def transform_pattern(pattern, chunk_size=8):
    # Calculate the number of chunks
    num_chunks = len(pattern) // chunk_size

    # Split the pattern into chunks
    chunks = [pattern[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]

    # Reverse the order of chunks
    chunks = chunks[::-1]

    # Join the chunks back into a single string
    transformed_pattern = ''.join(chunks)

    return transformed_pattern
    
def find_address(start_address, ways, gran, size):
    address_range = []
    # Ensure start_address is an integer
    start_address = int(start_address, 16) if isinstance(start_address, str) else start_address
    gran = int(gran, 16) if isinstance(gran, str) else gran

    for way in range(ways):
        for i in range(0, size, 0x40):
            address = start_address + gran * way + i
            address_range.append(address)
            print(hex(address))
        #print(hex(address))
    
    return address_range
        
def get_interleave_way(value):
    switcher = {
        0: 0,
        1: 2,
        2: 4,
        3: 8,
        4: 16,
        8: 3,
        9: 6,
       10: 12
    }
    return switcher.get(value, "Reserved")

def get_interleave_granularity(value):
    switcher = {
        0: 256,
        1: 512,
        2: 1024,
        3: 2048,
        4: 4096,
        5: 8192,
        6: 16384
    }
    return switcher.get(value, "Reserved")

        
def find_memory_targets():
    
    # Execute the shell command
    result = sp.run(['cat', '/sv/memoryTargets'], stdout=sp.PIPE, text=True)
    # Capture the output
    output = result.stdout
    # Process the output to find the specific values
    memory_targets = []  # Use a list to store values
    for line in output.splitlines():
        if 'hdm' in line.lower():
            first_arg  = line.split(',')[0]
            start, end = first_arg.split('-')
            start      = start + "000"
            end        = end + "000"
            if start not in memory_targets:  # Check for uniqueness
                memory_targets.append(start)  # Add the start value to the list
            if end not in memory_targets:  # Check for uniqueness
                memory_targets.append(end)  # Add the start value to the list
    
    print(memory_targets)
    return list(memory_targets)  # Convert the set to a list
	
def main(IW,IG):

    #Pass the granularity and the ways in the command line argument as per what is set in the LCD registers
    if len(sys.argv) !=4:
        print("\nExpecting 3 argument, first argument Interleaving Granularity, second argument Interleaving Ways, Third argument Time in minutes") 

    #IG                           = int(sys.argv[1])
    #IW                           = int(sys.argv[2])
    Minutes                      = 120
    
    #Working directory is chosen for saving the logs, Manage if you need a diff path
    cwd                          = os.getcwd()

    #Pass the log path to archive the run logs
    log_path                     = "-logPath="   + cwd
    #Algorithm to picked for writing the data pattern
    algorithm                    = "-algorithm=" + "cacheline" #Can be replaced with randomness, this is algo name dont confuse with -cacheline in datapattern
    
    current_time_at_start        = datetime.now()
    current_time_at_start_hr     = current_time_at_start.hour
    current_time_at_start_mn     = current_time_at_start.minute
    
    print("\nStart Time")
    print(current_time_at_start)
    
    data_verification_flag       = 0
    
    while True: 
    
        #Call CacheFlush before any memical operation is done
        result                       = 0
        result                       = sp.call("cache_flush")
        
        if(result != 0):
            print("Cache Flush failed")
            return result
        
        #Random data pattern to be written (Add the needed pattern in data_pattern to add new one)
        data_pattern_chosen          = rand.choice(data_pattern)
        
        #Pass the datapattern chose in the cmdline
        cacheline_data_to_be_Written = "-cacheline=" + data_pattern_chosen
        
        #Select one CPU-Thread to be binded
        cpu_path                     = 'find /sv/socket* -iname "local-cpu*" | grep -v "core"'
        cpu_bind_list                = sp.Popen(cpu_path, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = cpu_bind_list.communicate()
        cpu_thread_binded            = "-bind="+ str(rand.choice(stdout.decode('utf-8').splitlines())) 
        
        #Select one HDM to be binded
        HDM_path                     = 'find /sv/* -iname "*local-cxlhdm*"'
        HDM_targ_list                = sp.Popen(HDM_path, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = HDM_targ_list.communicate()
        target_address_list          = find_memory_targets()
        size                         = hex(rand.randrange(0x80, (IG + 0x1), 0x80))
        Node_Path                    = str(rand.choice(stdout.decode('utf-8').splitlines()))

        if "socket0" in Node_Path:
            target_address = target_address_list[0]
            end_address    = target_address_list[1]
        else:
            target_address = target_address_list[2]
            end_address    = target_address_list[3]

        print("\nTarget Address Base  0x",target_address)
        # Convert target_address to an integer
        target_address_int           = int(target_address, 16)
        end_address_int              = int(end_address,16)

        # Generate a random address within the specified range
        target_end_Address           = end_address_int
        target_address               = hex(rand.randrange(target_address_int,target_end_Address - (IG * IW), (0x4000*IW)))
        
        #target_address               = "0x5880000000"
        #target_address               = hex(rand.randrange(target_address, target_end_Address - IG, IG))
        print("\nTarget Address       ",target_address)
        
        HDM_target_selected          = "-target="+ Node_Path + "/cxlhdm/write-back:" + target_address + ":" + size            
        #HDM_target_selected           = "-target=/sv/socket0/bus2/pciExpress2/local-cxlhdm-00/cxlhdm/interleaved/write-back:0x5880000000:0x300"     
        
        #Sample command
        #memical_command = ["memicals","-algorithm=cacheline","-bind=/sv/socket0/local-cpu-00","-target=/sv/socket0/bus2/pciExpress2/local-cxlhdm-00/cxlhdm/interleaved/write-back:0x5880000000:0x100","-count=1","-iterations=1",cacheline_data_to_be_Written,log_path,"-writeOnce"]
        
        result                       = 0
        #Actual memicals command
        memical_command              = ["memicals",algorithm,cpu_thread_binded,HDM_target_selected,"-count=1","-iterations=1",cacheline_data_to_be_Written,log_path,"-writeOnce"]

        result                       = sp.call(memical_command)
        
        if 0!=result:
            print("\nCall to memicals failed")
            break
        
        #ways                         = get_interleave_way(IW)
        #gran                         = get_interleave_granularity(IG)
        # Create the address range
        #address_range                = find_address(target_address,ways,gran,range_length)
        address_ranges                = find_address(target_address,IW,IG,int(size,16))
        
    
        data_verification_flag  = data_verification(data_pattern_chosen, address_ranges)
        
        current_time_at_run        = datetime.now()
        current_time_at_run_hr     = current_time_at_run.hour
        current_time_at_run_mn     = current_time_at_run.minute

        if(0 != data_verification_flag):
            print("\nCurrent Time")
            print(current_time_at_run)
            print("\n TEST FAILED")
            break
            
        if(current_time_at_run_hr < current_time_at_start_hr):
            current_time_at_run_hr = current_time_at_run_hr + 24
        
        if((((current_time_at_run_hr * 60) + current_time_at_run_mn) - ((current_time_at_start_hr * 60) + current_time_at_start_mn)) >= Minutes):
            print("\nCurrent Time")
            print(current_time_at_run)
            print("\nTimer Elapsed")
            print("\n TEST PASSED")
            break
        

    #debug
    #print(data_pattern_chosen)
    #print(cwd)
    #print(cacheline_data_to_be_Written)
    #print(log_path)
    #print(memical_command)
    #print(result)
    #print(cpu_thread_binded)
    #print(HDM_target_selected)
    #print(HDM_targ_list)
    #print(Node_Path)
    #print(target_address_list)
    return result
    

if __name__ == "__main__":
    #tc_name, IG,IW,0x ways_gran
    comb = [
    ["tc2008", 512, 3, 0x81],
    ["tc2010", 512, 6, 0x91],
    ["tc2012", 512, 12, 0xa1],    
    ["tc2015", 1024, 3, 0x82],
    ["tc2017", 1024, 6, 0x92],
    ["tc2019", 1024, 12, 0xa2],
    ["tc2022", 2048, 3, 0x83],
    ["tc2024", 2048, 6, 0x93],
    ["tc2026", 2048, 12, 0xa3],
    ["tc2001", 256, 3, 0x80],
    ["tc2003", 256, 6, 0x90],
    ["tc2005", 256, 12, 0xa0], 
    ]
    
    # Iterate over the combinations
    for tc, ig, iw, value in comb:    
        # Create the directory if it doesn't exist
        if not os.path.exists(tc):
            os.makedirs(tc)
        
        # Change the current working directory to the new folder
        os.chdir(tc)
        
        # Format the command string
        command = f"regacc /sv/cxl-*/cxl_dcoh.hdm_dec_ctrl={hex(value)}"
        
        # Execute the command
        result = sp.run(command, shell=True, check=True, stdout=sp.PIPE, stderr=sp.PIPE)
       
        # Call the main function with iw and ig
        with open("console.log", "w") as log_file:
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            sys.stdout = log_file
            sys.stderr = log_file
            print("ways=",iw, "Granularity=",ig)
            try:
                main(iw, ig)
            finally:
                sys.stdout = original_stdout
                sys.stderr = original_stderr
        
        # Change back to the original directory
        os.chdir("..")

