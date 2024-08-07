import streamlit as st
import db as DataBase
import plotly.express as px
import ast
import staticData as userData
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

st.set_page_config(layout="wide")

# data_url = "https://i.pinimg.com/originals/5d/35/e3/5d35e39988e3a183bdc3a9d2570d20a9.gif"
# st.image(
#             data_url, 
#             width=400,
#         )

st.markdown("""
    <h1 id="chat-header" style="position: fixed;
                   top: 0;
                   left: 0;
                   width: 100%;
                   text-align: center;
                   background-color: #f1f1f1;
                   color: #008080;
                   z-index: 9">
        Softsquare's Products: Dev App Analytics
    </h1>
""", unsafe_allow_html=True)

hide_st_style = """ <style>
                    #MainMenu {visibility:hidden;}
                    footer {visibility:hidden;}
                    header {visibility:hidden;}
                    </style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)

if 'filtes' not in st.session_state:
    st.session_state['filtes'] = [
        {
            'isFilter' : False,
            'isDateFromFilter' : False,
            'isDateToFilter' : False,
            'fromDate' : '',
            'toDate' : '',
            'isOrgFilter' : False,
            'orgName' : '',
            'isFeatureFilter' : False,
            'featuesName' : ''
        }
    ]


col1, col2, col3, col4, col5 = st.columns(5)

next_month =date.today().replace(day=28) + timedelta(days=4) - relativedelta(months = 1)
toDateStandard = next_month - timedelta(days=next_month.day)  

with col1:
    productNameSelect = st.selectbox( "Select Product", ("AGrid", "Media Manager", "User 360", "Snap Data"),  index=None) 
    #  "Lightning Image Slider", "Lightning DataTable Dev", "Lead Assignment", "Response Time Tracker", "Opportunity Stage Alert" 

with col2:
    fromDate = st.date_input("From", toDateStandard - relativedelta(years = 1))
    if(fromDate != None):
        st.session_state.filtes[0]['isFilter'] = True
        st.session_state.filtes[0]['isDateFromFilter'] = True
        st.session_state.filtes[0]['fromDate'] = str(fromDate)
    
with col3:
    toDate = st.date_input("To", toDateStandard)
    if(toDate != None):
        st.session_state.filtes[0]['isFilter'] = True
        st.session_state.filtes[0]['isDateToFilter'] = True
        st.session_state.filtes[0]['toDate'] = str(toDate)

with col4:

    if(productNameSelect != None and fromDate != None  and toDate != None):
        dbConnect = DataBase.connectSnowflake()
        orgNames = DataBase.getOrganizationName(dbConnect, productNameSelect)
        if(orgNames and len(orgNames) > 0):
            orgNames[0]['combined'] = orgNames[0]['ORGANIZATION_NAME'] + '-' + orgNames[0]['ORGANIZATION_ID']
            
            filterOrgName = st.selectbox("Select Organization", (orgNames[0]['combined'] ), index=None)
            if(filterOrgName != None):
                st.session_state.filtes[0]['isFilter'] = True
                st.session_state.filtes[0]['isOrgFilter'] = True
                st.session_state.filtes[0]['orgName'] = filterOrgName
            else:
                st.session_state.filtes[0]['isOrgFilter'] = False
    else:
        filterOrgName = st.selectbox("Select Organization", ([''] ), index=None, disabled=True)

with col5:

    if(productNameSelect == 'AGrid'):
        featureList = userData.getAgridFeatureList()
    elif(productNameSelect == 'Media Manager'):
        featureList = userData.getMediaManagerFeatureList()
        
    if productNameSelect != None and len(featureList) > 0:
        featureFilter = st.selectbox("Select Feature",(featureList[0].keys()), index=None)
        if(featureFilter != None):
            st.session_state.filtes[0]['isFilter'] = True
            st.session_state.filtes[0]['isFeatureFilter'] = True
            st.session_state.filtes[0]['featuesName'] = featureList[0].get(featureFilter)
        else:
            st.session_state.filtes[0]['isFeatureFilter'] = False        

# with st.spinner('Wait for it...'):

# userCountCol, CreateCountCol = st.columns(2)

# with userCountCol:
#     dbConnect = DataBase.connectSnowflake()
#     userCount = DataBase.getnumberOfUsers(dbConnect, productNameSelect, st.session_state.filtes[0])

  
if(productNameSelect != None and fromDate != None  and toDate != None):
    print('start.....')

    with st.container(border=True):

        col_inside1, col_inside2, col_inside3 = st.columns(3)

        getProductDetails = DataBase.getProductDetails(dbConnect, productNameSelect, st.session_state.filtes[0])

        featureListValues = featureList[0].values()
        featureListValuesList = tuple(featureListValues)

        getProductDetailsFeatures = DataBase.getProductDetailsWithfeature(dbConnect, productNameSelect, st.session_state.filtes[0], featureListValuesList)

        getProductDetailsFeaturesDf = getProductDetailsFeatures[0]

        def getNameFromFeatuesList(row):
                cutomEntity = row['CUSTOM_ENTITY']
                if not pd.isna(cutomEntity) or str(cutomEntity).lower() != 'nan':
                    if(productNameSelect == 'AGrid'):
                        data = userData.getAgridFeatureList()
                    elif(productNameSelect == 'Media Manager'):
                        data = userData.getMediaManagerFeatureList()

                    return next((key for dictionary in data for key, value in dictionary.items() if value.lower() == cutomEntity.lower()), None)
                else:
                    return cutomEntity
                
        getProductDetailsFeaturesDf['NEW_CUSTOM_ENTITY'] = getProductDetailsFeaturesDf.apply(getNameFromFeatuesList, axis=1)
        
        if(getProductDetails != None and len(getProductDetails) > 0 ):

            # Dashboard 1
            title = 'Monthly Utilization Of ' + productNameSelect
            fig = px.bar(getProductDetails[0], x = "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE", labels={"OVER_ALL_USAGE" : "Total Usage", 'LOG_CREATED_MONTH' : 'Months'},
                        hover_data=["OVER_ALL_USAGE"],
                        template="gridon",height=500, title = title)
            st.plotly_chart(fig,use_container_width=True)
            
            # Dashboard 2
            if(featureFilter == None):
                figfeatures = px.bar(getProductDetailsFeaturesDf, x="LOG_CREATED_MONTH", y="OVER_ALL_USAGE", color="NEW_CUSTOM_ENTITY", title="Features Utilization")
                st.plotly_chart(figfeatures,use_container_width=True)


            # Dashboard 3
            if(featureFilter != None  and filterOrgName == None):
                featuresUsageWithOrg = DataBase.getFeaturesUsageWithOrg(dbConnect, productNameSelect, st.session_state.filtes[0])
                figfeatures = px.bar(featuresUsageWithOrg[0], x="LOG_CREATED_MONTH", y="OVER_ALL_USAGE", color="ORGANIZATION_NAME", title="Feature Usage by Organization")
                st.plotly_chart(figfeatures,use_container_width=True)
                





    # if(len(featureList) > 0):
    #     featureListValues = featureList[0].values()
    #     featureListValuesList = tuple(featureListValues)

    #     if(filterOrgName != None and len(filterOrgName) > 0):
    #         getFeaturesDetails = DataBase.getFeatureDetails(dbConnect, productNameSelect, featureListValuesList, True, filterOrgName)
    #     else:
    #         getFeaturesDetails = DataBase.getFeatureDetails(dbConnect, productNameSelect, featureListValuesList, False, None)

        
    #     if(len(getFeaturesDetails) > 0):
    #         def getNameFromFeatuesList(row):
    #             cutomEntity = row['CUSTOM_ENTITY']
    #             if not pd.isna(cutomEntity) or str(cutomEntity).lower() != 'nan':
    #                 data = userData.getAgridFeatureList()
    #                 return next((key for dictionary in data for key, value in dictionary.items() if value.lower() == cutomEntity.lower()), None)
    #             else:
    #                 return cutomEntity
            
    #         df = getFeaturesDetails[0]
    #         df['NEW_CUSTOM_ENTITY'] = df.apply(getNameFromFeatuesList, axis=1)
    #         title = 'Most Used ' + productNameSelect + ' Features'
    #         fig = px.bar(df, x = "NEW_CUSTOM_ENTITY", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'NEW_CUSTOM_ENTITY' : 'Features'},
    #                     title = title, hover_data=["TOTAL"],
    #                     template="gridon",height=500)
    #         st.plotly_chart(fig,use_container_width=True)

    packageVersion = DataBase.getPackageVersion(dbConnect, productNameSelect, st.session_state.filtes[0])
    title = 'Package Version Usage of ' + productNameSelect
    fig = px.bar(packageVersion[0], x = "VERSION_NAME", y = "TOTAL", labels={"TOTAL" : "Total Usage", "VERSION_NAME" : 'Package Version Name'},
                title = title, hover_data=["TOTAL"],
                template="gridon",height=500)
    st.plotly_chart(fig,use_container_width=True)



