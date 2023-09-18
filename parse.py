import pandas as pd
import os
from math import sqrt

# get all files from results directory
files = os.listdir('results')

# create empty list to store values
values = []

# loop through files
for file in files:
    tcp_bitrate = []
    tcp_bitrate_sdev = 0
    tcp_bitrate_uncertainty = 0
    
    tcp_retries = []
    tcp_retries_sdev = 0
    tcp_retries_uncertainty = 0
    
    udp_bitrate = []
    udp_bitrate_sdev = 0
    udp_bitrate_uncertainty = 0
    
    udp_jitter = []
    udp_jitter_sdev = 0
    udp_jitter_uncertainty = 0
    
    udp_loss = []
    udp_loss_sdev = 0
    udp_loss_uncertainty = 0
    
    min_rtt = []    
    avg_rtt = []
    avg_rtt_sdev = 0
    avg_rtt_uncertainty = 0
    max_rtt = []
    
    tcp_svc_bitrate = []
    tcp_svc_bitrate_sdev = 0
    tcp_svc_bitrate_uncertainty = 0
    
    tcp_svc_retries = []
    tcp_svc_retries_sdev = 0
    tcp_svc_retries_uncertainty = 0
        
    udp_svc_bitrate = []
    udp_svc_bitrate_sdev = 0
    udp_svc_bitrate_uncertainty = 0
    
    udp_svc_jitter = []
    udp_svc_jitter_sdev = 0
    udp_svc_jitter_uncertainty = 0
    
    udp_svc_loss = []
    udp_svc_loss_sdev = 0
    udp_svc_loss_uncertainty = 0    
    
    with open('results/' + file, 'r') as f:
        lines = f.readlines()
        
        # parse first 5 lines of file
        for line in lines[:5]:
            line = line.strip().split(' ')
            tcp_bitrate += [float(line[0])]
            tcp_retries += [float(line[1])]
        avg = sum(tcp_bitrate) / 5
        tcp_bitrate_sdev =  sqrt(sum([(x - avg)**2 for x in tcp_bitrate]) / (len(tcp_bitrate) - 1))
        tcp_bitrate_uncertainty = tcp_bitrate_sdev / sqrt(len(tcp_bitrate))
        tcp_bitrate_sdev = round(tcp_bitrate_sdev, 2)
        tcp_bitrate_uncertainty = round(tcp_bitrate_uncertainty, 2)
        tcp_bitrate = round(sum(tcp_bitrate) / 5, 2)
        
        avg = sum(tcp_retries) / 5
        tcp_retries_sdev = sqrt(sum([(x - avg)**2 for x in tcp_retries]) / (len(tcp_retries) - 1))
        tcp_retries_uncertainty = tcp_retries_sdev / sqrt(len(tcp_retries))
        tcp_retries_sdev = round(tcp_retries_sdev, 2)
        tcp_retries_uncertainty = round(tcp_retries_uncertainty, 2)
        tcp_retries = round(sum(tcp_retries) / 5, 2)
    
        # parse second 5 lines of file       
        for line in lines[5:10]:
            line = line.strip().split(' ')
            udp_bitrate += [float(line[0])]
            udp_jitter += [float(line[1])]
            udp_loss += [float(line[2].strip('(').strip(')').strip('%'))]
            
        avg = sum(udp_bitrate) / 5
        udp_bitrate_sdev = sqrt(sum([(x - avg)**2 for x in udp_bitrate]) / (len(udp_bitrate) - 1))
        udp_bitrate_uncertainty = udp_bitrate_sdev / sqrt(len(udp_bitrate))
        udp_bitrate_sdev = round(udp_bitrate_sdev, 2)
        udp_bitrate_uncertainty = round(udp_bitrate_uncertainty, 2)
        udp_bitrate = round(sum(udp_bitrate) / 5, 2)
        
        avg = sum(udp_jitter) / 5
        udp_jitter_sdev = sqrt(sum([(x - avg)**2 for x in udp_jitter]) / (len(udp_jitter) - 1))
        udp_jitter_uncertainty = udp_jitter_sdev / sqrt(len(udp_jitter))
        udp_jitter_sdev = round(udp_jitter_sdev, 3)
        udp_jitter_uncertainty = round(udp_jitter_uncertainty, 3)
        udp_jitter = round(sum(udp_jitter) / 5, 3)
        
        avg = sum(udp_loss) / 5
        udp_loss_sdev = sqrt(sum([(x - avg)**2 for x in udp_loss]) / (len(udp_loss) - 1))
        udp_loss_uncertainty = udp_loss_sdev / sqrt(len(udp_loss))
        udp_loss_sdev = round(udp_loss_sdev, 2)
        udp_loss_uncertainty = round(udp_loss_uncertainty, 2)        
        udp_loss = round(sum(udp_loss) / 5, 2)
        
        # parse third 5 lines of file       
        for line in lines[10:15]:
            line = line.strip().split('/')
            min_rtt += [float(line[0])]
            avg_rtt += [float(line[1])]
            max_rtt += [float(line[2])]
        
        min_rtt = min(min_rtt)
        avg = sum(avg_rtt) / 5
        avg_rtt_sdev = sqrt(sum([(x - avg)**2 for x in avg_rtt]) / (len(avg_rtt) - 1))
        avg_rtt_uncertainty = avg_rtt_sdev / sqrt(len(avg_rtt))
        avg_rtt_sdev = round(avg_rtt_sdev, 2)
        avg_rtt_uncertainty = round(avg_rtt_uncertainty, 2)
        avg_rtt = round(sum(avg_rtt) / 5, 2)
        max_rtt = max(max_rtt)
        
        # parse fourth 5 lines of file
        for line in lines[15:20]:
            line = line.strip().split(' ')
            tcp_svc_bitrate += [float(line[0])]
            tcp_svc_retries += [float(line[1])]

        avg = sum(tcp_svc_bitrate) / 5
        tcp_svc_bitrate_sdev = sqrt(sum([(x - avg)**2 for x in tcp_svc_bitrate]) / (len(tcp_svc_bitrate) - 1))
        tcp_svc_bitrate_uncertainty = tcp_svc_bitrate_sdev / sqrt(len(tcp_svc_bitrate))
        tcp_svc_bitrate_sdev = round(tcp_svc_bitrate_sdev, 2)
        tcp_svc_bitrate_uncertainty = round(tcp_svc_bitrate_uncertainty, 2)
        tcp_svc_bitrate = round(sum(tcp_svc_bitrate) / 5, 2)
        
        avg = sum(tcp_svc_retries) / 5
        tcp_svc_retries_sdev = sqrt(sum([(x - avg)**2 for x in tcp_svc_retries]) / (len(tcp_svc_retries) - 1))
        tcp_svc_retries_uncertainty = tcp_svc_retries_sdev / sqrt(len(tcp_svc_retries))
        tcp_svc_retries_sdev = round(tcp_svc_retries_sdev, 2)
        tcp_svc_retries_uncertainty = round(tcp_svc_retries_uncertainty, 2)
        tcp_svc_retries = round(sum(tcp_svc_retries) / 5, 2)
        
        # parse last 5 lines of file
        for line in lines[20:25]:
            line = line.strip().split(' ')
            udp_svc_bitrate += [float(line[0])]
            udp_svc_jitter += [float(line[1])]
            udp_svc_loss += [float(line[2].strip('(').strip(')').strip('%'))]
            
        avg = sum(udp_svc_bitrate) / 5
        udp_svc_bitrate_sdev = sqrt(sum([(x - avg)**2 for x in udp_svc_bitrate]) / (len(udp_svc_bitrate) - 1))
        udp_svc_bitrate_uncertainty = udp_svc_bitrate_sdev / sqrt(len(udp_svc_bitrate))
        udp_svc_bitrate_sdev = round(udp_svc_bitrate_sdev, 2)
        udp_svc_bitrate_uncertainty = round(udp_svc_bitrate_uncertainty, 2)
        udp_svc_bitrate = round(sum(udp_svc_bitrate) / 5, 2)
        
        avg = sum(udp_svc_jitter) / 5
        udp_svc_jitter_sdev = sqrt(sum([(x - avg)**2 for x in udp_svc_jitter]) / (len(udp_svc_jitter) - 1))
        udp_svc_jitter_uncertainty = udp_svc_jitter_sdev / sqrt(len(udp_svc_jitter))
        udp_svc_jitter_sdev = round(udp_svc_jitter_sdev, 3)
        udp_svc_jitter_uncertainty = round(udp_svc_jitter_uncertainty, 3)
        udp_svc_jitter = round(sum(udp_svc_jitter) / 5, 3)
        
        avg = sum(udp_svc_loss) / 5
        udp_svc_loss_sdev = sqrt(sum([(x - avg)**2 for x in udp_svc_loss]) / (len(udp_svc_loss) - 1))
        udp_svc_loss_uncertainty = udp_svc_loss_sdev / sqrt(len(udp_svc_loss))
        udp_svc_loss_sdev = round(udp_svc_loss_sdev, 2)
        udp_svc_loss_uncertainty = round(udp_svc_loss_uncertainty, 2)
        udp_svc_loss = round(sum(udp_svc_loss) / 5, 2)
    
    if file.split('.')[0] == 'bare-metal':
        values.insert(0, [file.split('.')[0], 
                   tcp_bitrate, tcp_bitrate_uncertainty, tcp_bitrate_sdev, 
                   tcp_retries, tcp_retries_uncertainty, tcp_retries_sdev, 
                   udp_bitrate, udp_bitrate_uncertainty, udp_bitrate_sdev, 
                   udp_jitter, udp_jitter_uncertainty, udp_jitter_sdev, 
                   udp_loss, udp_loss_uncertainty, udp_loss_sdev, 
                   min_rtt, avg_rtt, avg_rtt_uncertainty, avg_rtt_sdev, max_rtt,
                   tcp_svc_bitrate, tcp_svc_bitrate_uncertainty, tcp_svc_bitrate_sdev, 
                   tcp_svc_retries, tcp_svc_retries_uncertainty, tcp_svc_retries_sdev, 
                   udp_svc_bitrate, udp_svc_bitrate_uncertainty, udp_svc_bitrate_sdev, 
                   udp_svc_jitter, udp_svc_jitter_uncertainty, udp_svc_jitter_sdev, 
                   udp_svc_loss, udp_svc_loss_uncertainty, udp_svc_loss_sdev])
    else:
        values.append([file.split('.')[0], 
                   tcp_bitrate, tcp_bitrate_uncertainty, tcp_bitrate_sdev, 
                   tcp_retries, tcp_retries_uncertainty, tcp_retries_sdev, 
                   udp_bitrate, udp_bitrate_uncertainty, udp_bitrate_sdev, 
                   udp_jitter, udp_jitter_uncertainty, udp_jitter_sdev, 
                   udp_loss, udp_loss_uncertainty, udp_loss_sdev, 
                   min_rtt, avg_rtt, avg_rtt_uncertainty, avg_rtt_sdev, max_rtt,
                   tcp_svc_bitrate, tcp_svc_bitrate_uncertainty, tcp_svc_bitrate_sdev, 
                   tcp_svc_retries, tcp_svc_retries_uncertainty, tcp_svc_retries_sdev, 
                   udp_svc_bitrate, udp_svc_bitrate_uncertainty, udp_svc_bitrate_sdev, 
                   udp_svc_jitter, udp_svc_jitter_uncertainty, udp_svc_jitter_sdev, 
                   udp_svc_loss, udp_svc_loss_uncertainty, udp_svc_loss_sdev])
    #print(f"{file}: {tcp_bitrate}, {tcp_retries}, {udp_bitrate}, {udp_jitter}, {udp_loss}, {min_rtt}, {avg_rtt}, {max_rtt}")
    
# add to dataframe
df = pd.DataFrame(values, columns=['CNI-Protocol', 
                                   'TCP Bitrate', '+-', 'TCP Bitrate SDev', 
                                   'TCP Retries', '+-', 'TCP Retries SDev',
                                   'UDP Bitrate', '+-', 'UDP Bitrate SDev', 
                                   'UDP Jitter', '+-', 'UDP Jitter SDev', 
                                   'UDP Loss', '+-', 'UDP Loss SDev',
                                   'Min RTT', 'Avg RTT', '+-', 'Avg RTT SDev', 'Max RTT', 
                                   'TCP SVC Bitrate', '+-', 'TCP SVC Bitrate SDev',
                                   'TCP SVC Retries', '+-', 'TCP SVC Retries SDev',
                                   'UDP SVC Bitrate', '+-', 'UDP SVC Bitrate SDev',
                                   'UDP SVC Jitter', '+-', 'UDP SVC Jitter SDev',
                                   'UDP SVC Loss', '+-', 'UDP SVC Loss SDev'])

# save to csv
df.to_csv('results.csv')   