import pandas as pd
import streamlit as st
import numpy as np
import requests
import json
import urllib

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="example app")


st.title("Huskalkyl v3")

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
yearslefttowork = st.sidebar.number_input("År kvar att jobba:    ", value=35)
gross_income = st.sidebar.number_input("Bruttoinkomst:    ", value=840000)

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

#Variables calculations
purchase_price = int(purchase_price)
down_payment = int(down_payment)
interestRate = float(interestRate/100)
loan_ratio = down_payment/purchase_price

interestRate_per_month = float(interestRate/12)
loanAmount = int(purchase_price - down_payment)
monthlyPayment = int(loanAmount*(interestRate/12))
monthly_amort_cost = int(loanAmount*(amortization_ptc/100/12))
tot_monthly_cost = monthly_alarm_cost + monthly_broadband_tv_cost + monthly_electricity_cost + monthly_garbage_cost + monthly_insurance_cost + monthly_utilities_cost + monthlyPayment + monthly_amort_cost

mortage_deed_cost = int((loanAmount-down_payment-mortage_deed)*0.02)
title_deed_cost = int(purchase_price*0.015)


with left_column:
    #Adress map
    adress_loc = pd.DataFrame(geolocator.geocode(obj_adress).point)
    adress_loc["lon"] = adress_loc.iloc[1]
    adress_loc.drop([1,2], inplace=True)
    adress_loc.rename(columns={0:"lat"}, inplace=True)

    st.map(adress_loc)  


                
with left_column:
    #Visualisering
    st.header("Månadskostnader")
    st.write("Pris/kvm:", int(purchase_price/sqm))
    st.write("Total kostnad/mån inkl driftkostnader", int(tot_monthly_cost))
    st.write("Total räntekostnad/mån innan ränteavdrag", monthlyPayment)
    st.write("Total räntekostnad/mån efter ränteavdrag", int(monthlyPayment*0.7))
    st.write("Total amorteringskostnad/mån", monthly_amort_cost)
    
    sum_ot_cost = mortage_deed_cost + title_deed_cost + inspection_cost + alarm_cost + total_ren_need

    st.header("Engångskostnader:")
    st.write("Pantbrev:", mortage_deed_cost)
    st.write("Lagfart:", title_deed_cost)
    st.write("Besiktning:", inspection_cost)
    st.write("Larminstallation:", alarm_cost)
    st.write("Initialt renoveringsbehov:", renovation_cost)
    st.write("Summa engångskostnader:", sum_ot_cost)


