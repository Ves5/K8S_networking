import pandas as pd
import os

# get all files from results directory
files = os.listdir('results')

# create empty list to store values
values = []

# loop through files
for file in files:
    tcp_bitrate = 0
    tcp_retries = 0
    
    udp_bitrate = 0
    udp_jitter = 0
    udp_loss = 0
    
    min_rtt = []
    avg_rtt = 0
    max_rtt = []
    
    tcp_svc_bitrate = 0
    tcp_svc_retries = 0
    
    udp_svc_bitrate = 0
    udp_svc_jitter = 0
    udp_svc_loss = 0
    
    with open('results/' + file, 'r') as f:
        lines = f.readlines()
        
        # parse first 5 lines of file
        for line in lines[:5]:
            line = line.strip().split(' ')
            tcp_bitrate += float(line[0])
            tcp_retries += float(line[1])
        tcp_bitrate = round(tcp_bitrate / 5, 2)
        tcp_retries = round(tcp_retries / 5, 2)
    
        # parse second 5 lines of file       
        for line in lines[5:10]:
            line = line.strip().split(' ')
            udp_bitrate += float(line[0])
            udp_jitter += float(line[1])
            udp_loss += float(line[2].strip('(').strip(')').strip('%'))
        udp_bitrate = round(udp_bitrate / 5, 2)
        udp_jitter = round(udp_jitter / 5, 3)
        udp_loss = round(udp_loss / 5, 2)
        
        # parse third 5 lines of file       
        for line in lines[10:15]:
            line = line.strip().split('/')
            min_rtt += [float(line[0])]
            avg_rtt += float(line[1])
            max_rtt += [float(line[2])]
        min_rtt = min(min_rtt)
        avg_rtt = round(avg_rtt / 5, 2)
        max_rtt = max(max_rtt)
        
        # parse fourth 5 lines of file
        for line in lines[15:20]:
            line = line.strip().split(' ')
            tcp_svc_bitrate += float(line[0])
            tcp_svc_retries += float(line[1])
        tcp_svc_bitrate = round(tcp_svc_bitrate / 5, 2)
        tcp_svc_retries = round(tcp_svc_retries / 5, 2)
        
        # parse last 5 lines of file
        for line in lines[20:25]:
            line = line.strip().split(' ')
            udp_svc_bitrate += float(line[0])
            udp_svc_jitter += float(line[1])
            udp_svc_loss += float(line[2].strip('(').strip(')').strip('%'))
        udp_svc_bitrate = round(udp_svc_bitrate / 5, 2)
        udp_svc_jitter = round(udp_svc_jitter / 5, 3)
        udp_svc_loss = round(udp_svc_loss / 5, 2)
    
    values.append([file.split('.')[0], tcp_bitrate, tcp_retries, udp_bitrate, udp_jitter, udp_loss, min_rtt, avg_rtt, max_rtt, tcp_svc_bitrate, tcp_svc_retries, udp_svc_bitrate, udp_svc_jitter, udp_svc_loss])
    #print(f"{file}: {tcp_bitrate}, {tcp_retries}, {udp_bitrate}, {udp_jitter}, {udp_loss}, {min_rtt}, {avg_rtt}, {max_rtt}")
    
# add to dataframe
df = pd.DataFrame(values, columns=['CNI-Protocol', 
                                   'TCP Bitrate', 'TCP Retries', 
                                   'UDP Bitrate', 'UDP Jitter', 'UDP Loss', 
                                   'Min RTT', 'Avg RTT', 'Max RTT', 
                                   'TCP SVC Bitrate', 'TCP SVC Retries', 
                                   'UDP SVC Bitrate', 'UDP SVC Jitter', 'UDP SVC Loss'])

# save to csv
df.to_csv('results.csv')   