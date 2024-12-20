# 1. Data preprocessing
import pandas as pd

### Prepare the bike data ###
# Import bike trip data
bike = pd.read_csv('Austin_MetroBike_Trips_20240916.csv')
bike.head(5) # Display first 5 rows of the bike data

# Select data for April 2024
bike_2024 = bike[bike['Year'] == 2024] # 141,144 rows
bike_2024['Month'].value_counts() # April 2024 has the most data
bike_apr_2024 = bike_2024[bike_2024['Month'] == 4] # 33,203 rows
bike_apr_2024 = bike_apr_2024[['Trip ID', 'Checkout Date', 'Checkout Time', 'Checkout Kiosk', 'Return Kiosk', 'Trip Duration Minutes']] # Select relevant columns for analysis
bike_apr_2024['Checkout Kiosk'] = bike_apr_2024['Checkout Kiosk'].str.strip() # Remove leading/trailing spaces from 'Checkout Kiosk' column


### Prepare the kiosk data for merging ###
# Import kiosk data
kiosk = pd.read_csv("Austin_MetroBike_Kiosk_Locations.csv") # 102 rows
kiosk['Kiosk ID'] = kiosk['Kiosk ID'].astype('object')

# Check unique kiosk names
unique_bike = pd.DataFrame(sorted(bike_apr_2024['Checkout Kiosk'].unique()), columns=['Unique Checkout Kiosk'])
unique_kiosk = pd.DataFrame(sorted(kiosk['Kiosk Name'].unique()), columns=['Unique Checkout Kiosk'])
unique_names = pd.concat([unique_bike, unique_kiosk], axis=1) # Concatenate the two DataFrames

# Replace ' & ' with '/' in the 'Kiosk Name' column of the kiosk data
kiosk['Kiosk Name'] = kiosk['Kiosk Name'].str.replace(' & ', '/', regex=False)

# Replace 'Kiosk Name' column using the dictionary
replacement_dict = {
    'Capitol Station / Congress/11th' : '11th/Congress @ The Texas Capitol',
    'State Capitol Visitors Garage @ San Jacinto/12th' : '12th/San Jacinto @ State Capitol Visitors Garage',
    '13th/Trinity' : '13th/Trinity @ Waterloo Greenway',
    'Guadalupe/21st' : '21st/Guadalupe',
    '21st/Speedway @PCL' : '21st/Speedway @ PCL',
    '22nd 1/2/Rio Grande' : '22.5/Rio Grande',
    #'' : '23rd/Pearl', # 30.287329976401352, -97.74632802031869 location driven from app
    'Nueces/26th' : '26th/Nueces',
    'Rio Grande/28th' : '28th/Rio Grande',
    'City Hall / Lavaca/2nd' : '2nd/Lavaca @ City Hall',
    'Nueces @ 3rd' : '3rd/Nueces',
    'Nueces/3rd' : '3rd/Nueces',
    'Convention Center / 3rd/Trinity' : '3rd/Trinity @ The Convention Center',
    'Lavaca/6th' : '6th/Lavaca',
    'Trinity/6th Street' : '6th/Trinity',
    'West/6th St.' : '6th/West',
    'Red River/8th Street' : '8th/Red River',
    'San Jacinto/8th Street' : '8th/San Jacinto',
    'Henderson/9th' : '9th/Henderson',
    'Palmer Auditorium' : 'Barton Springs/Bouldin @ Palmer Auditorium',
    'Barton Springs @ Kinney Ave' : 'Barton Springs/Kinney',
    'Congress/Cesar Chavez' : 'Cesar Chavez/Congress',
    #'' : 'Dean Keeton/Park Place', # 30.287836617190724, -97.72845870365327
    'East 11th St./San Marcos' : 'East 11th/San Marcos',
    'East 11th St. at Victory Grill' : 'East 11th/Victory Grill',
    'Capital Metro HQ - East 5th at Broadway' : 'East 5th/Broadway @ Capital Metro HQ',
    'Medina/East 6th' : 'East 6th/Medina',
    'East 6th/Pedernales St.' : 'East 6th/Pedernales',
    'East 6th at Robert Martinez' : 'East 6th/Robert T. Martinez',
    'Pfluger Bridge @ W 2nd Street' : 'Electric Drive/Sandra Muraida Way @ Pfluger Ped Bridge',
    'UT West Mall @ Guadalupe' : 'Guadalupe/West Mall @ University Co-op',
    'Lake Austin Blvd @ Deep Eddy' : 'Lake Austin Blvd/Deep Eddy',
    'Lakeshore @ Austin Hostel' : 'Lakeshore/Austin Hostel',
    'Nash Hernandez @ RBJ South' : 'Nash Hernandez/East @ RBJ South',
    #'' : 'One Texas Center', # 30.25767062481796, -97.74897583987295
    'Rainey St @ Cummings' : 'Rainey/Cummings',
    'ACC - Rio Grande/12th' : 'Rio Grande/12th',
    'Riverside @ S. Lamar' : 'Riverside/South Lamar',
    'Long Center @ South 1st/Riverside' : 'South 1st/Riverside @ Long Center',
    'South Congress/Barton Springs at the Austin American-Statesman' : 'South Congress/Barton Springs @ The Austin American-Statesman',
    'Sterzing at Barton Springs' : 'Sterzing/Barton Springs',
    'MoPac Pedestrian Bridge @ Veterans Drive' : 'Veterans/Atlanta @ MoPac Ped Bridge'
}
kiosk['Kiosk Name'] = kiosk['Kiosk Name'].replace(replacement_dict)

# Select specific columns from the 'kiosk' DataFrame
kiosk = kiosk[['Kiosk ID', 'Kiosk Name', 'Lat', 'Lon', 'Number of Docks']]

# Create a DataFrame with additional kiosk information to add
add_kiosk = pd.DataFrame({
    'Kiosk Name': ['23rd/Pearl', 'Dean Keeton/Park Place', 'One Texas Center'],
    'Lat': [30.287329976401352, 30.287836617190724, 30.25767062481796],
    'Lon': [-97.74632802031869, -97.72845870365327, -97.74897583987295]
})

# Concatenate the new kiosks (add_kiosk) to the existing kiosk DataFrame
kiosk = pd.concat([kiosk, add_kiosk], ignore_index=True) # 105 rows

# 'Number of Docks' retrieved from the Bikeshare app and assign 'Kiosk ID'
kiosk.loc[kiosk['Kiosk Name'] == '3rd/Nueces', ['Number of Docks', 'Kiosk ID']] = [8, 2]
kiosk.loc[kiosk['Kiosk Name'] == '6th/Lavaca', ['Number of Docks', 'Kiosk ID']] = [6, 3]
kiosk.loc[kiosk['Kiosk Name'] == 'Dean Keeton/Park Place', ['Number of Docks', 'Kiosk ID']] = [13, 4]
kiosk.loc[kiosk['Kiosk Name'] == 'East 7th/Pleasant Valley', ['Number of Docks', 'Kiosk ID']] = [8, 5]
kiosk.loc[kiosk['Kiosk Name'] == 'One Texas Center', ['Number of Docks', 'Kiosk ID']] = [13, 6]

# Remove rows without dock information in the Bikeshare app
kiosks_to_remove = [
    '23rd/Pearl',
    '5th/San Marcos',
    '6th/Navasota St.',
    '8th/Guadalupe',
    'ACC - West/12th Street',
    'Bullock Museum @ Congress/MLK',
    'OFFICE/Main/Shop/Repair',
    'Pease Park',
    'Rainey @ River St',
    'Red River/LBJ Library',
    'Republic Square',
    'Rio Grande/12th',
    'State Capitol @ 14th/Colorado',
    'State Parking Garage @ Brazos/18th',
    'Toomey Rd @ South Lamar',
    'Waller/6th St.',
    'Zilker Park West'
]

# Remove rows where 'Kiosk Name' matches any in the list
kiosk = kiosk[~kiosk['Kiosk Name'].isin(kiosks_to_remove)] # 88 rows

# Drop duplicates based on the 'Kiosk Name' column to keep unique kiosks only
kiosk = kiosk.drop_duplicates(subset='Kiosk Name') # 86 rows
kiosk.to_csv('kiosk.csv', index = False)


### Merge bike and kiosk data ###
merged_co = pd.merge(bike_apr_2024, kiosk, left_on = 'Checkout Kiosk', right_on = 'Kiosk Name') # 32,035 rows
merged_co = merged_co[['Checkout Date', 'Checkout Time', 'Checkout Kiosk', 'Kiosk ID', 'Number of Docks']]

# Rename columns
merged_co = merged_co.rename(columns={
    'Kiosk ID': 'CO ID',
    'Number of Docks': 'CO Docks',
})

merged_rt = pd.merge(bike_apr_2024, kiosk, left_on = 'Return Kiosk', right_on = 'Kiosk Name', how = 'left')
merged_rt = merged_rt[['Return Kiosk', 'Kiosk ID', 'Number of Docks']]
merged_rt = merged_rt.rename(columns={
    'Kiosk ID': 'RT ID',
    'Number of Docks': 'RT Docks',
})

merged_df = pd.concat([merged_co, merged_rt], axis=1)


### Split the data into weekday and weekend ###
merged_df['Checkout Date'] = pd.to_datetime(merged_df['Checkout Date']) # convert to date type
merged_df['Day of Week'] = merged_df['Checkout Date'].dt.weekday # assign weekday and weekend

weekday_df = merged_df[merged_df['Day of Week'] < 5]
weekday_df = weekday_df.dropna(subset=['CO ID', 'RT ID']) # select weekday 22,662 rows

weekend_df = merged_df[merged_df['Day of Week'] >= 5] 
weekend_df = weekend_df.dropna(subset=['CO ID', 'RT ID']) # select weekend 8,074 rows

weekday_df.to_csv('weekday_df.csv', index = False)
weekend_df.to_csv('weekend_df.csv', index = False)


########################################################################################################################

# 2. Identify communities
from collections import Counter
import pandas as pd

def count_flow(infile, col1, col2, outfile):
    flow_count_dict = {} # Create a dictionary to store counts of flows between zone pairs
    id_list = [] # Create a list to store unique zone IDs
    bigfile = open(infile) # Open file
    bigfile.readline() # Skip the header
    for lineno, line in enumerate(bigfile):
        # If the value in column col1 is empty, return the id_list and flow_count_dict
        if line.split(',')[col1] == '':
            return id_list, flow_count_dict

        # Get the zone1_id and zone2_id
        zone1_id = int(line.split(',')[col1])
        zone2_id = int(line.split(',')[col2])
        
        # Skip if the zone1_id and zone2_id are the same
        if zone1_id == zone2_id:
            continue
        
        # Add zone1_id and zone2_id to id_list if it isn't already present
        if zone1_id not in id_list:
            id_list.append(zone1_id)
        if zone2_id not in id_list:
            id_list.append(zone2_id)
        
        # Create pairs of zone1 and zone2
        zone_pair = (zone1_id, zone2_id)
        zone_pair_reverse = (zone2_id, zone1_id)

        # Add the flow count for each zone pair
        if zone_pair in flow_count_dict:
            flow_count_dict[zone_pair] += 1
        elif zone_pair_reverse in flow_count_dict:
            flow_count_dict[zone_pair_reverse] += 1
        else:
            flow_count_dict[zone_pair] = 1 # Assign 1 if the zone pair doesn't exist

        # Print the line number
        print(str(lineno)) 

    # Export outfile
    with open(outfile, "w") as output:
        for k, v in flow_count_dict.items():
            output.write(str(k) + '\t' + str(v) + '\n')
    return id_list, flow_count_dict

# Analyze data
col1 = 3  # checkout kiosk id
col2 = 6  # return kiosk id
infile = "weekday_df.csv"
outfile = "weekday_df.txt"
result = count_flow(infile, col1, col2, outfile)

# Creat a dataframe from outfile
result_list = result[1]
result_df = pd.DataFrame(list(result_list.items()), columns=['Points', 'Value'])
result_df[['id1', 'id2']] = pd.DataFrame(result_df['Points'].tolist(), index=result_df.index)
result_df = result_df[['id1', 'id2', 'Value']]

# Sort ascending or descending frequency by Value
result_df.sort_values(by='Value', ascending=False)

# analyze community detection
import igraph as ig
from igraph import *
from functools import reduce # Python3

# Get vertices and flow_count_dict by using count_flow function
vertices, flow_count_dict = count_flow(infile, col1, col2, outfile)

g = Graph(directed=False) # Create an undirected graph

# Create lists to store edge and weight
edge_list = []
weight_list = []

# Add the edge and weight lists
for k, v in flow_count_dict.items():
    edge_list.append(k)
    weight_list.append(v)

g.add_vertices(vertices) # Add the vertices to graph

# Convert zone pairs in edge_list to vertex indices in edge_list_index
edge_list_index = []
for pair in edge_list:
    # Find the index of each zone in the vertices list and add the pair of indices to edge_list_index
    edge_list_index.append((vertices.index(pair[0]),vertices.index(pair[1])))
g.add_edges(edge_list_index)

# Assign weight and label the weight
g.es['weight'] = weight_list
g.es['label'] = weight_list

# Detect community using multilevel methodology
community = g.community_multilevel(weights = weight_list)
print(community.membership)

# Write a result file
with open("community_weekday.txt", "w") as output: # remember to change this file name for May data
    for i in range (len(vertices)):
        output.write(str(vertices[i]) +'\t'+ str(community.membership[i])+'\n')

########################################################################################################################

# Accessibility
import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString, Point

# STEP 1
# Import kiosk point
kiosk_point = gpd.read_file('kiosk_point.shp') # 86 rows

# Import kiosk buffer
kiosk_buffer = gpd.read_file('kiosk_SA.shp')
kiosk_buffer['name'] = [name.split(' :')[0] for name in kiosk_buffer['Name']]
kiosk_buffer['name'] = kiosk_buffer['name'].astype(str)
kiosk_point['Kiosk ID'] = kiosk_point['Kiosk ID'].astype(str)

# Join kiosk to kiosk buffer
kiosk_buffer = gpd.GeoDataFrame(kiosk_buffer[['name', 'geometry']]).merge(kiosk_point[['Kiosk ID', 'Kiosk Name', 'Number of']], left_on='name', right_on='Kiosk ID', how='inner')
kiosk_buffer = gpd.GeoDataFrame(kiosk_buffer, geometry='geometry')

# Import population
census_point = gpd.read_file('census_tract_point.shp') # 311 rows
census_point = census_point.to_crs(kiosk_buffer.crs)
#census_point = census_point.to_crs(fac_buffer.crs)

# Spatial join
result = gpd.sjoin(kiosk_buffer, census_point, how="inner", predicate="intersects") 
sum_pop_rate = result.groupby('name')['POP'].sum().reset_index()
sum_pop_rate.rename(columns={'POP': 'pop_sum'}, inplace=True)
kiosk_buffer['pop_sum'] = kiosk_buffer['name'].map(sum_pop_rate.set_index('name')['pop_sum']).fillna(0)

# Join kiosk buffer to kiosk
kiosk_point = gpd.GeoDataFrame(kiosk_buffer[['name', 'pop_sum']]).merge(kiosk_point[['Kiosk ID', 'Number of', 'geometry']], left_on='name', right_on='Kiosk ID', how='inner')
kiosk_point = gpd.GeoDataFrame(kiosk_point, geometry='geometry')


# Step 2

# Import pop buffer
pop_buffer = gpd.read_file('census_tract_SA.shp')
pop_buffer['pop_name'] = [name.split(' :')[0] for name in pop_buffer['Name']]

# Join pop to pop buffer
pop_buffer = pop_buffer[['pop_name', 'geometry']].merge(census_point[['Name_12', 'POP']], left_on='pop_name', right_on='Name_12', how='inner')
pop_buffer.drop(columns=['Name_12'], inplace=True)

# Spatial join
result = gpd.sjoin(pop_buffer, kiosk_point, how="inner", predicate="intersects") 
sum_ProToPop = result.groupby('pop_name')['pop_sum'].sum().reset_index()
sum_ProToPop.rename(columns={'pop_sum': 'sfca'}, inplace=True)
pop_buffer['sfca'] = pop_buffer['pop_name'].map(sum_ProToPop.set_index('pop_name')['sfca']).fillna(0)

# Divide by mean
pop_buffer['spar'] = pop_buffer['sfca'] / pop_buffer['sfca'].mean()

# Join 2SFCA value to census tract shp file
census_tract = gpd.read_file('census_tract.shp')
spar = census_tract[['Name_12', 'geometry']].merge(pop_buffer[['pop_name', 'POP', 'sfca', 'spar']], left_on='Name_12', right_on='pop_name', how='left')
spar.drop(columns=['Name_12'], inplace=True)
spar.to_file('spar.shp')
