import pandas as pd
import streamlit as st
import numpy as np
import requests
import json
import urllib
import urllib.parse

st.title("Huskalkyl1")

left_column, right_column = st.beta_columns(2)

#Renoveringsbehov

with right_column:
    with st.beta_expander("Renoveringsbehov"):
        washingmachine = st.number_input("Tvättmaskin:    ", value=10000)
        dryer = st.number_input("Torktumlare:    ", value=10000)
        kitchen = st.number_input("Kök:    ", value=150000)
        refrigerator = st.number_input("Kylskåp    ", value=10000)
        freezer = st.number_input("Frys:    ", value=10000)
        dishwasher = st.number_input("dishwasher:    ", value=10000)
        Spis = st.number_input("Spis:    ", value=5000)
        bathroom1 = st.number_input("Badrum 1:    ", value=100000)
        bathroom2 = st.number_input("Badrum 2:    ", value=100000)
        Varmvattenberedare = st.number_input("Varmvattenberedare:    ", value=20000)
        roof = st.number_input("Tak:    ", value=10000)
        hangers = st.number_input("Stuprännor:    ", value=500)
        paint_facade = st.number_input("Målning fasad:    ", value=5000)
        windows = st.number_input("Fönster:    ", value=50000)
        stammar = st.number_input("Stammar:    ", value=50000)
        drainage = st.number_input("Dränering:    ", value=20000)
        WC = st.number_input("WC:    ", value=50000)
        paint_rooms = st.number_input("Målning rum:    ", value=10000)

        total_ren_need = washingmachine + dryer + kitchen + refrigerator + freezer + dishwasher + Spis + bathroom1 + bathroom2 + Varmvattenberedare + roof + hangers + paint_facade + windows + stammar + drainage + WC + paint_rooms
        st.write("Totalt renoveringsbehov:    ")
        st.write(total_ren_need)
        renovation_cost = total_ren_need

#Sidebarinputs
obj_adress = st.sidebar.text_input("Objektets adress:    ", value="Vanadisvägen 4, 113 46, Stockholm")
gross_income = st.sidebar.number_input("Bruttoinkomst hushåll/år:    ", value=1500000)

purchase_price = st.sidebar.number_input("Inköpsvärde:    ", value=11700000)
sqm = st.sidebar.number_input("Kvm:    ", value=160)
down_payment = st.sidebar.number_input("Kontantinsats:   ",value=2400000)

mortage_deed = st.sidebar.number_input("Pantbrev:    ", value=5000000)
amortization_ptc = st.sidebar.number_input("Amortering %", value=2)
monthly_operational_cost = st.sidebar.number_input("Driftkostnad/mån:   ",value=3000)

renovation_cost = st.sidebar.number_input("Renoveringskostnad:    ", value=total_ren_need, key="rencost")
alarm_cost = st.sidebar.number_input("Larminstallation:    ", value=5000, key="alarmcost")
inspection_cost = st.sidebar.number_input("Besiktning:    ", value=10000, key="besikt")


goal_monthly_savings = st.sidebar.number_input("Målsparande/mån:    ", value=5000, key="gms")
monthly_insurance_cost = st.sidebar.number_input("Försäkring/mån:    ", value=1000, key="gis")
monthly_broadband_tv_cost = st.sidebar.number_input("Bredband & TV/mån:    ", value=500, key="gbs")

monthly_garbage_cost = st.sidebar.number_input("Sophämtning/mån:    ", value=300, key="mgs")
monthly_utilities_cost = st.sidebar.number_input("Vatten och avlopp/mån:    ", value=1000, key="gus")
monthly_electricity_cost = st.sidebar.number_input("El/mån:    ", value=2000, key="ges")

monthly_alarm_cost = st.sidebar.number_input("Larmkostnad/mån:    ", value=200, key="gas")
renovation_budget = total_ren_need
road_cost = st.sidebar.number_input("Vägavgifter/mån:    ", value=200, key="rgs")
interestRate = st.sidebar.number_input("Låneränta:   ",value=1.25)
interestRate_safety1 = st.sidebar.number_input("Låneränta + %:   ",value=2.25, key="loan")
interestRate_safety2 = st.sidebar.number_input("Låneränta + %:   ",value=3.25, key="loan2")


#Variables calculations
purchase_price = int(purchase_price)
down_payment = int(down_payment)
interestRate = float(interestRate/100)
interestRate_safety1 = float(interestRate_safety1/100)
loan_ratio = down_payment/purchase_price

interestRate_per_month = float(interestRate/12)
loanAmount = int(purchase_price - down_payment)
monthlyPayment = int(loanAmount*(interestRate/12))
monthlyPayment_safety1 = int(loanAmount*(interestRate_safety1)/12*0.7)
monthly_amort_cost = int(loanAmount*(amortization_ptc/100/12))
tot_monthly_cost = monthly_alarm_cost + monthly_broadband_tv_cost + monthly_electricity_cost + monthly_garbage_cost + monthly_insurance_cost + monthly_utilities_cost + monthlyPayment + monthly_amort_cost + goal_monthly_savings
tot_monthly_cost_safety1 = monthly_alarm_cost + monthly_broadband_tv_cost + monthly_electricity_cost + monthly_garbage_cost + monthly_insurance_cost + monthly_utilities_cost + monthlyPayment_safety1 + monthly_amort_cost + goal_monthly_savings

mortage_deed_cost = int((loanAmount-down_payment-mortage_deed)*0.02)
title_deed_cost = int(purchase_price*0.015)


with left_column:
    #Adress map
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(obj_adress) +'?format=json'
    response = requests.get(url).json()
    df_mapdata = pd.DataFrame(response)
    df_mapdata2 = pd.DataFrame(columns=["lat", "lon"])
    df_mapdata2["lat"] = df_mapdata["lat"].astype(float)
    df_mapdata2["lon"] = df_mapdata["lon"].astype(float)
    # map_data = pd.DataFrame({"lat":, "lon":})
    # print(response)
    # print(response[0]["lat"])
    # print(response[0]["lon"])
    st.map(df_mapdata2)  
    
    #Visualisering
    st.header("Månadskostnader")
    st.write("Pris/kvm:", int(purchase_price/sqm))
    st.write("Total räntekostnad/mån efter ränteavdrag", int(monthlyPayment*0.7))
    st.write("Räntekostnad vid + 1% efter ränteavdrag", int(monthlyPayment_safety1))
    st.write("Total amorteringskostnad/mån", monthly_amort_cost)
    st.write("Total kostnad/mån inkl amort, drift, räntekostnader", int(tot_monthly_cost))
    st.write("Total kostnad/mån inkl amort, drift, räntekostnader" + "  " +  str(interestRate_safety1*100), int(tot_monthly_cost_safety1))
       
    sum_ot_cost = mortage_deed_cost + title_deed_cost + inspection_cost + alarm_cost + total_ren_need

    st.header("Engångskostnader:")
    st.write("Pantbrev:", mortage_deed_cost)
    st.write("Lagfart:", title_deed_cost)
    st.write("Besiktning:", inspection_cost)
    st.write("Larminstallation:", alarm_cost)
    st.write("Initialt renoveringsbehov:", renovation_cost)
    st.write("Summa engångskostnader:", sum_ot_cost)

    #Kvar varje månad
    st.header("Buffert")
    st.write("Buffert varje månad inkl sparande", (gross_income*0.65/12)-tot_monthly_cost)


