import pandas as pd

# Read the CSV files
time_df = pd.read_csv('data/Time.csv', index_col=0)
fare_df = pd.read_csv('data/Fare.csv', index_col=0)

# Get all station names
all_stations = list(time_df.index)

route_data = []

# Define line classifications
kjl_stations = [
    'Gombak', 'Taman Melati', 'Wangsa Maju', 'Sri Rampai', 'Setiawangsa', 
    'Jelatek', "Dato' Keramat", 'Damai', 'Ampang Park', 'KLCC', 'Kampung Baru',
    'Dang Wangi', 'Masjid Jamek (KJL)', 'Pasar Seni (KJL)', 'KL Sentral (KJL)',
    'Bangsar', 'Abdullah Hukum', 'Kerinchi', 'Universiti', 'Taman Jaya',
    'Asia Jaya', 'Taman Paramount', 'Taman Bahagia', 'Kelana Jaya',
    'Lembah Subang', 'Ara Damansara', 'Glenmarie', 'Subang Jaya', 'SS 15',
    'SS 18', 'USJ 7 (KJL)', 'Taipan', 'Wawasan', 'USJ 21', 'Alam Megah',
    'Subang Alam', 'Putra Heights (KJL)'
]

sbk_stations = [
    'Sungai Buloh', 'Kampung Selamat', 'Kwasa Damansara', 'Kwasa Sentral',
    'Kota Damansara', 'Surian', 'Mutiara Damansara', 'Bandar Utama', 'TTDI',
    'Phileo Damansara', 'Pusat Bandar Damansara', 'Semantan', 'Muzium Negara',
    'Pasar Seni (SBK)', 'Merdeka', 'Bukit Bintang', 'Tun Razak Exchange (TRX)',
    'Cochrane', 'Maluri (SBK)', 'Taman Pertama', 'Taman Midah', 'Taman Mutiara',
    'Taman Connaught', 'Taman Suntex', 'Sri Raya', 'Bandar Tun Hussein Onn',
    'Batu 11 Cheras', 'Bukit Dukung', 'Sungai Jernih', 'Stadium Kajang', 'Kajang'
]

# Strategy: Create balanced distribution
# ~33% KJL to KJL, ~33% SBK to SBK, ~34% Multi-line

kjl_count = 0
sbk_count = 0
multi_count = 0

for i, origin in enumerate(all_stations):
    
    # Determine what type of route to create based on current counts
    total_processed = kjl_count + sbk_count + multi_count
    target_kjl = total_processed * 0.33
    target_sbk = total_processed * 0.33
    
    if origin in kjl_stations:
        # For KJL origins, decide destination type
        if kjl_count < target_kjl:
            # Create KJL to KJL route
            if origin == 'Gombak':
                destination = 'KLCC'
            elif origin == 'KLCC':
                destination = 'Subang Jaya'
            elif origin == 'KL Sentral (KJL)':
                destination = 'Bangsar'
            elif origin == 'Subang Jaya':
                destination = 'Putra Heights (KJL)'
            elif origin == 'Putra Heights (KJL)':
                destination = 'KL Sentral (KJL)'
            else:
                # Pick a strategic KJL destination
                destination = 'KLCC'
            kjl_count += 1
        else:
            # Create Multi-line route (KJL to SBK)
            destination = 'Bukit Bintang'
            multi_count += 1
            
    elif origin in sbk_stations:
        # For SBK origins, decide destination type  
        if sbk_count < target_sbk:
            # Create SBK to SBK route
            if origin == 'Kajang':
                destination = 'Bukit Bintang'
            elif origin == 'Sungai Buloh':
                destination = 'Kajang'
            elif origin == 'Bukit Bintang':
                destination = 'TRX'
            elif origin == 'TRX':
                destination = 'Maluri (SBK)'
            else:
                # Pick a strategic SBK destination
                destination = 'Kajang'
            sbk_count += 1
        else:
            # Create Multi-line route (SBK to KJL)
            destination = 'KLCC'
            multi_count += 1
    else:
        # Fallback
        destination = 'KLCC'
        multi_count += 1
    
    # Make sure origin != destination
    if origin == destination:
        if origin == 'KLCC':
            destination = 'Kajang'
        elif origin == 'Kajang':
            destination = 'KLCC'
        else:
            destination = 'KLCC'
    
    # Get time and fare values
    if origin in time_df.index and destination in time_df.columns:
        time_val = time_df.loc[origin, destination]
        fare_val = fare_df.loc[origin, destination]
        
        # Determine line type
        if origin in kjl_stations and destination in kjl_stations:
            line_type = "LRT Kelana Jaya"
        elif origin in sbk_stations and destination in sbk_stations:
            line_type = "MRT Kajang"
        else:
            line_type = "Multi-line"
        
        route_data.append({
            'origin': origin,
            'destination': destination,
            'time': time_val,
            'fare': fare_val,
            'line': line_type
        })

# Convert to JSON format for your scatter plot
json_data = []
for route in route_data:
    json_entry = f'{{"origin": "{route["origin"]}", "destination": "{route["destination"]}", "time": {route["time"]}, "fare": {route["fare"]}, "line": "{route["line"]}"}}'
    json_data.append(json_entry)

# Print all entries for your JSON
for i, entry in enumerate(json_data):
    print(f"            {entry}{',' if i < len(json_data)-1 else ''}")

# Print distribution summary
kjl_routes = sum(1 for route in route_data if route['line'] == 'LRT Kelana Jaya')
sbk_routes = sum(1 for route in route_data if route['line'] == 'MRT Kajang') 
multi_routes = sum(1 for route in route_data if route['line'] == 'Multi-line')

print(f"\nRoute Distribution:")
print(f"LRT Kelana Jaya: {kjl_routes} ({kjl_routes/len(route_data)*100:.1f}%)")
print(f"MRT Kajang: {sbk_routes} ({sbk_routes/len(route_data)*100:.1f}%)")
print(f"Multi-line: {multi_routes} ({multi_routes/len(route_data)*100:.1f}%)")
print(f"Total routes: {len(route_data)}")