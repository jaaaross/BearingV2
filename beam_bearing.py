import streamlit as st
from dataclasses import dataclass
import beam_bearing_module as bbm

from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


st.set_page_config(layout="wide")

st.title("Timber Beam Bearing Calculator V2")

''' The idea here is to speed up the overall process of designing and detailing buildings with many different timber bearing connections. This will
allow the engineer to upload a set of parameters and quickly calculate viable connection designs. Please upload
a CSV file in the proper format. See below for the proper CSV format:

Label,B1 Width,B1 Depth,B1 Route Length,B1 DL,B1 LL,B2 Width,B2 Depth,B2 Route Length,B2 DL,B2 LL,C Width,C Depth,F_c_perp,Char Depth

BC1,10,20,4,8000,6000,8,18,3.5,8000,6000,12,12,400,3.2

BC2,8,20,5,8000,6000,9,18,4,8000,6000,12,12,400,1.8

BC3,8,20,4.5,8000,6000,10,18,5,8000,6000,12,12,400,0.9

[I realize its not pretty or elegant but I wanted to get it built at 90% and in because I believe its the end of the course!]'''


import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("See below for your connection parameters! Everything can be edited here.")  

    node_df = st.data_editor(df, num_rows="dynamic")


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
        node_df['Char Depth']
        )

    b1_nonfire, b2_nonfire, b1_fire, b2_fire, loads = BearingNode.call_calculation()

    return b1_nonfire, b2_nonfire, b1_fire, b2_fire, loads 

calculation = node_df.apply(run_check, axis=1)

capacities_df = node_df.copy()

calc_df = node_df.copy()
        

capacities_df.drop(columns=['B1 Width', 'B1 Depth', 'B1 Route Length', 'B2 Width', 'B2 Depth', 'B2 Route Length', 'C Width', 'C Depth', 'B1 DL', 'B1 LL', 'B2 DL', 'B2 LL', 'F_c_perp', 'Char Depth'], axis=1, inplace=True)

b1_nonfire_capacity = []
b2_nonfire_capacity = []
b1_fire_capacity = []
b2_fire_capacity = []

b1_nonfire_bearing_width = []
b2_nonfire_bearing_width = []
b1_nonfire_bearing_length = []
b2_nonfire_bearing_length = []

b1_fire_bearing_width = []
b2_fire_bearing_width = []
b1_fire_bearing_length = []
b2_fire_bearing_length = []
    
b1_factored_load = []
b1_unfactored_load = []
b2_factored_load = []
b2_unfactored_load = []

b1_nonfire_ratio = []
b1_fire_ratio = []
b2_nonfire_ratio = []
b2_fire_ratio = []

for row in calculation:
    b1_nonfire_capacity.append(row[0][0])
    b2_nonfire_capacity.append(row[1][0])
    b1_fire_capacity.append(row[2][0])
    b2_fire_capacity.append(row[3][0])

    b1_nonfire_bearing_width.append(row[0][1])
    b2_nonfire_bearing_width.append(row[1][1])
    b1_nonfire_bearing_length.append(row[0][2])
    b2_nonfire_bearing_length.append(row[1][2])

    b1_fire_bearing_width.append(row[2][1])
    b2_fire_bearing_width.append(row[3][1])
    b1_fire_bearing_length.append(row[2][2])
    b2_fire_bearing_length.append(row[3][2])
    
    b1_factored_load.append(row[4][0])
    b1_unfactored_load.append(row[4][1])
    b2_factored_load.append(row[4][2])
    b2_unfactored_load.append(row[4][3])


capacities_df.insert(1, "B1 Factored Load", b1_factored_load, True)
capacities_df.insert(2, "B1 Nonfire Case Capacity", b1_nonfire_capacity, True)
capacities_df.insert(3, "B1 NF Ratio", capacities_df['B1 Factored Load'] / capacities_df['B1 Nonfire Case Capacity'], True)

capacities_df.insert(4, "B1 Unfactored Load", b1_unfactored_load, True)
capacities_df.insert(5, "B1 Fire Case Capacity", b1_fire_capacity, True)
capacities_df.insert(6, "B1 F Ratio", capacities_df['B1 Unfactored Load'] / capacities_df['B1 Fire Case Capacity'], True)

capacities_df.insert(7, "B2 Factored Load", b2_factored_load, True)
capacities_df.insert(8, "B2 Nonfire Case Capacity", b2_nonfire_capacity, True)
capacities_df.insert(9, "B2 NF Ratio", capacities_df['B2 Factored Load'] / capacities_df['B2 Nonfire Case Capacity'], True)

capacities_df.insert(10, "B2 Unfactored Load", b2_unfactored_load, True)
capacities_df.insert(11, "B2 Fire Case Capacity", b2_fire_capacity, True)
capacities_df.insert(12, "B2 F Ratio", capacities_df['B2 Unfactored Load'] / capacities_df['B2 Fire Case Capacity'], True)

calc_df.insert(1, 'B1 Nonfire Bearing Width', b1_nonfire_bearing_width, True)
calc_df.insert(2, 'B1 Nonfire Bearing Length', b1_nonfire_bearing_length, True)
calc_df.insert(3, 'B1 Fire Bearing Width', b1_fire_bearing_width, True)
calc_df.insert(4, 'B1 Fire Bearing Length', b1_fire_bearing_length, True)

calc_df.insert(5, 'B2 Nonfire Bearing Width', b2_nonfire_bearing_width, True)
calc_df.insert(6, 'B2 Nonfire Bearing Length', b2_nonfire_bearing_length, True)
calc_df.insert(7, 'B2 Fire Bearing Width', b2_fire_bearing_width, True)
calc_df.insert(8, 'B2 Fire Bearing Length', b2_fire_bearing_length, True)


output_df = node_df.copy()

st.write('You can click on the check box in the left most column to see the specific column node.')
event = st.dataframe(
    capacities_df,
    on_select='rerun',
    selection_mode='single-row'
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]

    beam1_width = node_df.iloc[selected_row]['B1 Width']
    beam2_width = node_df.iloc[selected_row]['B2 Width']
    beam1_route_length = node_df.iloc[selected_row]['B1 Route Length']
    beam2_route_length = node_df.iloc[selected_row]['B2 Route Length']
    column_width = node_df.iloc[selected_row]['C Width']
    column_depth = node_df.iloc[selected_row]['C Depth']
    char_depth = node_df.iloc[selected_row]['Char Depth']
    
    b1_nonfire_width = calc_df.iloc[selected_row]['B1 Nonfire Bearing Width']
    b1_nonfire_length = calc_df.iloc[selected_row]['B1 Nonfire Bearing Length']
    b2_nonfire_width = calc_df.iloc[selected_row]['B2 Nonfire Bearing Width']
    b2_nonfire_length = calc_df.iloc[selected_row]['B2 Nonfire Bearing Length']

    b1_fire_width = calc_df.iloc[selected_row]['B1 Fire Bearing Width']
    b1_fire_length = calc_df.iloc[selected_row]['B1 Fire Bearing Length']
    b2_fire_width = calc_df.iloc[selected_row]['B2 Fire Bearing Width']
    b2_fire_length = calc_df.iloc[selected_row]['B2 Fire Bearing Length']
    
    col1, col2 = st.columns(2)

    
    #NONFIRE CASE
    
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

    
    b1_nf_bearing_area = Rectangle([b1_nf_rect_x_pos, column_depth-b1_nonfire_length], b1_nonfire_width, b1_nonfire_length, angle=0, facecolor='magenta', edgecolor='red')
    b2_nf_bearing_area = Rectangle([b2_nf_rect_x_pos, 0], b2_nonfire_width, b2_nonfire_length, angle=0, facecolor='magenta', edgecolor='red')
    
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
    nf.text(column_width/2, column_depth*1.75, ("Beam 1 Effective Bearing Area = " + str(round(b1_nonfire_width,3)) + " inch wide x " + str(round(b1_nonfire_length,3)) + " inch long."), fontsize = 5, ha = 'center')
    nf.text(column_width/2, -column_depth*0.8, ("Beam 2 Effective Bearing Area = " + str(round(b2_nonfire_width,3)) + " inch wide x " + str(round(b2_nonfire_length,3)) + " inch long."), fontsize = 5, ha = 'center')

    with col1:
        if beam1_route_length + beam2_route_length > column_depth:
            st.write('Your beam routing is overlapping. Please reduce one side.')

        fig

    #FIRE CASE
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
    
    b1_f_bearing_area = Rectangle([b1_f_rect_x_pos, column_depth-beam1_route_length],b1_fire_width,b1_fire_length, angle=0, facecolor='magenta', edgecolor='black')
    b2_f_bearing_area = Rectangle([b2_f_rect_x_pos, char_depth],b2_fire_width,b2_fire_length, angle=0, facecolor='magenta', edgecolor='black')
    
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
    
    f.text(-column_width*0.6,column_depth*1.9, ('Fire Case'), fontsize = 5, ha = 'center')
    f.text(column_width/2, column_depth*1.75, ("Beam 1 Effective Bearing Area = " + str(round(b1_fire_width,3)) + " inch wide x " + str(round(b1_fire_length,3)) + " inch long."), fontsize = 5, ha = 'center')
    f.text(column_width/2, -column_depth*0.8, ("Beam 2 Effective Bearing Area = " + str(round(b2_fire_width,3)) + " inch wide x " + str(round(b2_fire_length,3)) + " inch long."), fontsize = 5, ha = 'center')

    with col2:
        fig




    
  




