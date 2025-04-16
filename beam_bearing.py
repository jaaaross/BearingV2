import streamlit as st
from dataclasses import dataclass
import beam_bearing_module as bbm


# For Later Versions - a 20mm subtraction of bearing width to account for the chamfer that is generally done around corners at connection to simplify CNC
# - the ignoring of remaining column material around the connection when the remaining material is not thick enough to rely on it being there after transport
# - would really like to add a report print function for easy documentation
# - in far future, would like to be able to load in a building from ETABS or similar, have it parse thru member sizes, loads, etc, then either the user adjusts
# bearing lengths or the software determines them to pass the bearing check at a certain percentage. After all of this, I want to print all of this information
# as a table that can be included in design drawings.

st.set_page_config(layout="wide")

st.title("Timber Beam Bearing Calculator V2")

''' The idea here is to speed up the overall process of designing and detailing buildings with many different timber bearing connections. This will
allow the engineer to upload a set of parameters and quickly calculate viable connection designs then print a schedule for their drawing. Please upload
a CSV file in the proper format.'''


import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("See below for your connection parameters! Everything can be edited here.")  

    node_df = st.data_editor(df, num_rows="dynamic")

#if FRR == "0":
#    char_depth = 0
#elif FRR == "1":
#    char_depth = 1.8
#elif FRR == "2":
#    char_depth = 3.2

def run_check(node_df):
    BearingNode = bbm.BearingNode(
        node_df['B1 Width'],
        node_df['B1 Depth'],
        node_df['B1 DL'],
        node_df['B1 LL'],
        node_df['B1 Route Length'],
        node_df['B2 Width'],
        node_df['B2 Depth'],
        node_df['B2 DL'],
        node_df['B2 LL'],
        node_df['B2 Route Length'],
        node_df['C Width'],
        node_df['C Depth'],
        node_df['F_c_perp'],
        3.2
        #if node_df['FRR'] == 0:
        #    return 0
        #elif node_df['FRR'] == 1:
        #    return 1.8
        #elif node_df['FRR'] == 2:
        #    return 3.2
        )

    b1_nonfire, b2_nonfire, b1_fire, b2_fire, loads = BearingNode.call_calculation()

    return b1_nonfire, b2_nonfire, b1_fire, b2_fire, loads 

df_capacity = node_df.apply(run_check, axis=1)

st.write(df_capacity)



capacities_df = node_df.copy()

        

capacities_df.drop(columns=['B1 Width', 'B1 Depth', 'B1 Route Length', 'B2 Width', 'B2 Depth', 'B2 Route Length', 'C Width', 'C Depth', 'B1 DL', 'B1 LL', 'B2 DL', 'B2 LL', 'F_c_perp', 'FRR'], axis=1, inplace=True)

b1_nonfire_capacity = []
b2_nonfire_capacity = []
b1_fire_capacity = []
b2_fire_capacity = []
b1_factored_load = []
b1_unfactored_load = []
b2_factored_load = []
b2_unfactored_load = []
b1_nonfire_ratio = []
b1_fire_ratio = []
b2_nonfire_ratio = []
b2_fire_ratio = []

for row in df_capacity:
    b1_nonfire_capacity.append(row[0][0])
    b2_nonfire_capacity.append(row[1][0])
    b1_fire_capacity.append(row[2][0])
    b2_fire_capacity.append(row[3][0])
    b1_factored_load.append(row[4][0])
    b1_unfactored_load.append(row[4][1])
    b2_factored_load.append(row[4][2])
    b2_unfactored_load.append(row[4][3])


capacities_df.insert(1, "B1 Factored Load", b1_factored_load, True)
capacities_df.insert(2, "B1 Nonfire Case Capacity", b1_nonfire_capacity, True)
capacities_df.insert(3, "Ratio1", capacities_df['B1 Factored Load'] / capacities_df['B1 Nonfire Case Capacity'], True)

capacities_df.insert(4, "B1 Unfactored Load", b1_unfactored_load, True)
capacities_df.insert(5, "B1 Fire Case Capacity", b1_fire_capacity, True)
capacities_df.insert(6, "Ratio2", capacities_df['B1 Unfactored Load'] / capacities_df['B1 Fire Case Capacity'], True)

capacities_df.insert(7, "B2 Factored Load", b2_factored_load, True)
capacities_df.insert(8, "B2 Nonfire Case Capacity", b2_nonfire_capacity, True)
capacities_df.insert(9, "Ratio3", capacities_df['B2 Factored Load'] / capacities_df['B2 Nonfire Case Capacity'], True)

capacities_df.insert(10, "B2 Unfactored Load", b2_unfactored_load, True)
capacities_df.insert(11, "B2 Fire Case Capacity", b2_fire_capacity, True)
capacities_df.insert(12, "Ratio4", capacities_df['B2 Unfactored Load'] / capacities_df['B2 Fire Case Capacity'], True)

st.write(capacities_df)


output_df = node_df.copy()

st.write('Click the checkbox in the far left column.')

event = st.dataframe(
    output_df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    country = output_df.iloc[selected_row]['B1 DL']
    capital = output_df.iloc[selected_row]['B2 DL']

    st.write(country + capital)


'''



BearingNode = bbm.BearingNode(beam1_width,
    beam1_depth,
    beam1_dead_load,
    beam1_live_load,
    beam1_route_length,
    beam2_width,
    beam2_depth,
    beam2_dead_load,
    beam2_live_load,
    beam2_route_length,
    column_width,
    column_depth,
    F_c_perp,
    char_depth
    )


b1_nonfire, b2_nonfire, b1_fire, b2_fire, loads = BearingNode.call_calculation()

ratios = []

ratios.append(round(loads[0]/b1_nonfire[0],3))

if b1_fire[0] == 0:
    ratios.append(100000)
else:
    ratios.append(round(loads[1]/b1_fire[0],3))
    
ratios.append(round(loads[2]/b2_nonfire[0],3))

if b2_fire[0] == 0:
    ratios.append(100000)
else:
    ratios.append(round(loads[3]/b2_fire[0],3))

# NONFIRE CASE
# bx_nonfire = capacity, bearing width, routing length
# loads = b1_f, b1_u, b2_f, b2_u


from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

col1, col2 = st.columns(2)

column_outline = Rectangle([0, 0], column_width, column_depth, angle=0, facecolor='peachpuff', edgecolor='black')
beam1_outline = Rectangle([column_width/2-beam1_width/2, column_depth-beam1_route_length], beam1_width, column_depth*0.8, angle=0, facecolor='green', edgecolor='black')
beam2_outline = Rectangle([column_width/2-beam2_width/2, beam2_route_length], beam2_width, -column_depth*0.8, angle=0, facecolor='blue', edgecolor='black')
column_outline2 = Rectangle([0, 0], column_width, column_depth, angle=0, facecolor='peachpuff', edgecolor='black', fill=False, ls='--')

if column_width >= beam1_width:
    b1_nf_rect_x_pos = column_width/2-beam1_width/2
else:
    b1_nf_rect_x_pos = 0

if column_width >= beam2_width:
    b2_nf_rect_x_pos = column_width/2-beam2_width/2
else:
    b2_nf_rect_x_pos = 0

b1_nf_bearing_area = Rectangle([b1_nf_rect_x_pos, column_depth-b1_nonfire[2]],b1_nonfire[1],b1_nonfire[2], angle=0, facecolor='magenta', edgecolor='red')
b2_nf_bearing_area = Rectangle([b2_nf_rect_x_pos, 0],b2_nonfire[1],b2_nonfire[2], angle=0, facecolor='magenta', edgecolor='red')

fig = Figure()
nf = fig.gca()

nf.add_patch(column_outline)
nf.add_patch(beam1_outline)
nf.add_patch(beam2_outline)
nf.add_patch(b1_nf_bearing_area)
nf.add_patch(b2_nf_bearing_area)
nf.add_patch(column_outline2)

nf.set_xlim(-column_width, column_width * 2)
nf.set_ylim(-column_depth, column_depth * 2)
nf.set_aspect('equal')

nf.text(-column_width*0.6,column_depth*1.9, ('Non-fire Case'), fontsize = 5, ha = 'center')
nf.text(column_width/2, column_depth*1.75, ("Beam 1 Effective Bearing Area = " + str(round(b1_nonfire[1],3)) + " inch wide x " + str(round(b1_nonfire[2],3)) + " inch long."), fontsize = 5, ha = 'center')
nf.text(column_width/2, -column_depth*0.8, ("Beam 2 Effective Bearing Area = " + str(round(b2_nonfire[1],3)) + " inch wide x " + str(round(b2_nonfire[2],3)) + " inch long."), fontsize = 5, ha = 'center')

with col1:
    if beam1_route_length + beam2_route_length > column_depth:
        st.write('Your beam routing is overlapping. Please reduce one side.')

    if ratios[0] > 1:
        st.write("Non-fire capacity is " + str(b1_nonfire[0]) + " lbs. Demand is " + str(loads[0]) + " lbs. Ratio = " + str(ratios[0]) + ". FAIL!")
    else:
        st.write("Non-fire capacity is " + str(b1_nonfire[0]) + " lbs. Demand is " + str(loads[0]) + " lbs. Ratio = " + str(ratios[0]) + ". PASS!")
    if ratios[2] > 1:
        st.write("Non-fire capacity is " + str(b2_nonfire[0]) + " lbs. Demand is " + str(loads[2]) + " lbs. Ratio = " + str(ratios[2]) + ". FAIL!")
    else:
        st.write("Non-fire capacity is " + str(b2_nonfire[0]) + " lbs. Demand is " + str(loads[2]) + " lbs. Ratio = " + str(ratios[2]) + ". PASS!")
    fig


# FIRE CASE

if column_width - char_depth*2 >= beam1_width:
    b1_f_rect_x_pos = column_width/2-beam1_width/2
else:
    b1_f_rect_x_pos = char_depth

if column_width - char_depth*2 >= beam2_width:
    b2_f_rect_x_pos = column_width/2-beam2_width/2
else:
    b2_f_rect_x_pos = char_depth


#repeated code here because it doesn't let you put the same shape on two figures
column_outline = Rectangle([0, 0], column_width, column_depth, angle=0, facecolor='peachpuff', edgecolor='black')
beam1_outline = Rectangle([column_width/2-beam1_width/2, column_depth-beam1_route_length], beam1_width, column_depth*0.8, angle=0, facecolor='green', edgecolor='black')
beam2_outline = Rectangle([column_width/2-beam2_width/2, beam2_route_length], beam2_width, -column_depth*0.8, angle=0, facecolor='blue', edgecolor='black')
column_outline2 = Rectangle([0, 0], column_width, column_depth, angle=0, facecolor='peachpuff', edgecolor='black', fill=False, ls='--')

b1_f_bearing_area = Rectangle([b1_f_rect_x_pos, column_depth-beam1_route_length],b1_fire[1],b1_fire[2], angle=0, facecolor='magenta', edgecolor='black')
b2_f_bearing_area = Rectangle([b2_f_rect_x_pos, char_depth],b2_fire[1],b2_fire[2], angle=0, facecolor='magenta', edgecolor='black')

column_char_outline = Rectangle([char_depth,char_depth], column_width - char_depth*2, column_depth-char_depth*2, angle=0, edgecolor='red', fill = False)

fig = Figure()
f = fig.gca()

f.add_patch(column_outline)
f.add_patch(beam1_outline)
f.add_patch(beam2_outline)
f.add_patch(column_outline2)

f.add_patch(b1_f_bearing_area)
f.add_patch(b2_f_bearing_area)

f.add_patch(column_char_outline)

f.set_xlim(-column_width, column_width * 2)
f.set_ylim(-column_depth, column_depth * 2)
f.set_aspect('equal')

f.text(-column_width*0.6,column_depth*1.9, (FRR + ' Fire Case'), fontsize = 5, ha = 'center')
f.text(column_width/2, column_depth*1.75, ("Beam 1 Effective Bearing Area = " + str(round(b1_fire[1],3)) + " inch wide x " + str(round(b1_fire[2],3)) + " inch long."), fontsize = 5, ha = 'center')
f.text(column_width/2, -column_depth*0.8, ("Beam 2 Effective Bearing Area = " + str(round(b2_fire[1],3)) + " inch wide x " + str(round(b2_fire[2],3)) + " inch long."), fontsize = 5, ha = 'center')


with col2:
    if ratios[1] == 100000:
        st.write("After " + FRR + " fire, beam 1 has no bearing material remaining. Increase bearing length.")
    elif ratios[1] > 1:
        st.write(FRR + " fire capacity is " + str(b1_fire[0]) + " lbs. Demand is " + str(loads[1]) + " lbs. Ratio = " + str(ratios[1]) + ". FAIL!")
    else:
        st.write(FRR + " fire capacity is " + str(b1_fire[0]) + " lbs. Demand is " + str(loads[1]) + " lbs. Ratio = " + str(ratios[1]) + ". PASS!")
    if ratios[3] == 100000:
        st.write("After " + FRR + " fire, beam 2 has no bearing material remaining. Increase bearing length.")
    elif ratios[3] > 1:
        st.write(FRR + " fire capacity is " + str(b2_fire[0]) + " lbs. Demand is " + str(loads[3]) + " lbs. Ratio = " + str(ratios[3]) + ". FAIL!")
    else:
        st.write(FRR + " fire capacity is " + str(b2_fire[0]) + " lbs. Demand is " + str(loads[3]) + " lbs. Ratio = " + str(ratios[3]) + ". PASS!")
    fig



'''




