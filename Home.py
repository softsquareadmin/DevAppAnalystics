import streamlit as st
import db as DataBase
import plotly.express as px
import ast
import staticData as userData

st.set_page_config(layout="wide")

# st.markdown("""
#         <style>
#                .block-container {
#                     padding-top: 1rem;
#                     padding-bottom: 0rem;
#                     padding-left: 5rem;
#                     padding-right: 5rem;
#                 }
#         </style>
#         """, unsafe_allow_html=True)

# container = st.container()

# with container:

#     col1, col2 = st.columns(2)

#     with col1:
#         productNameSelect = st.selectbox( "Select Product", ("AGrid", "User 360", "Media Manager", "Snap Data"),  index=None, placeholder="Select Product method...") 

col1, col2, col3 = st.columns(3)
with col2:
    st.write("Softsquare's Products : Dev App Analytics")
col1, col2 = st.columns(2)

with col1:
    productNameSelect = st.selectbox( "Select Product", ("AGrid", "User 360", "Media Manager", "Snap Data"),  index=None) 

# productButton = st.button("Submit", key = "product")

# with col2:
#     submitButton = st.button('Submit')

# with col2:
#     if(productNameSelect == 'AGrid'):
#         featureList = userData.getAgridFeatureList()
#     elif(productNameSelect == 'Media Manager'):
#         featureList = userData.getMediaManagerFeatureList()
#     print('productNameSelect :::::::;', productNameSelect)
#     # print('featureList :::::::::', featureList)
#     if(productNameSelect and featureList):
#         customEntitySelect = st.multiselect('select Feature',featureList[0].keys() )

# submitButton = st.button('Submit')

isInitialRun = False
# productButton = True and productButton
if(productNameSelect != None ):
    print('start.....')
    isInitialRun = True
    dbConnect = DataBase.connectSnowflake()
    packageVersion = DataBase.getPackageVersion(dbConnect, productNameSelect)
    orgNames = DataBase.getOrganizationName(dbConnect, productNameSelect)
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        # with col2:
        #     filterButton = st.button("Submit", key = "org")
        with col3:
            if(orgNames and len(orgNames) > 0):
                orgNames[0]['combined'] = orgNames[0]['ORGANIZATION_NAME'] + '-' + orgNames[0]['ORGANIZATION_ID']
                # print('orgNames :::::::::::::::::::', orgNames)
                
                filterOrgName = st.selectbox("select Org", (orgNames[0]['combined'] ), index=None)

        print('filterOrgName ::::::::::::::::', filterOrgName)
        if(filterOrgName != None and len(filterOrgName) > 0 ):
            getProductDetails = DataBase.getProductDetails(dbConnect, productNameSelect, True, filterOrgName)
        else:
            getProductDetails = DataBase.getProductDetails(dbConnect, productNameSelect, False, None)

        #### Over All Usage
        if(getProductDetails != None and len(getProductDetails) > 0 and packageVersion != None and len(packageVersion) > 0 ):
            title = 'Over all Usage of ' + productNameSelect
            fig = px.bar(getProductDetails[0], x = "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE", labels={"OVER_ALL_USAGE" : "Total Usage", 'LOG_CREATED_MONTH' : 'Months'},
                        title = title, hover_data=["OVER_ALL_USAGE"],
                        template="gridon",height=500)
            st.plotly_chart(fig,use_container_width=True)

        #### Top 10 and least 10 features
        if(productNameSelect == 'AGrid'):
            featureList = userData.getAgridFeatureList()
        elif(productNameSelect == 'Media Manager'):
            featureList = userData.getMediaManagerFeatureList()

        if(len(featureList) > 0):
            featureListValues = featureList[0].values()
            # print('featureList :::::::', featureListValues)
            featureListValuesList = tuple(featureListValues)

            if(filterOrgName != None and len(filterOrgName) > 0):
                getFeaturesDetails = DataBase.getFeatureDetails(dbConnect, productNameSelect, featureListValuesList, True, filterOrgName)
            else:
                getFeaturesDetails = DataBase.getFeatureDetails(dbConnect, productNameSelect, featureListValuesList, False, None)

            
            if(len(getFeaturesDetails) > 0):
                title = 'Most Used ' + productNameSelect + ' Features'
                fig = px.bar(getFeaturesDetails[0], x = "CUSTOM_ENTITY", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'CUSTOM_ENTITY' : 'CUSTOM_ENTITY'},
                            title = title, hover_data=["TOTAL"],
                            template="gridon",height=500)
                st.plotly_chart(fig,use_container_width=True)


    with st.container(border=True):
        title = 'Package Version Usage of ' + productNameSelect
        fig = px.bar(packageVersion[0], x = "VERSION_NAME", y = "TOTAL", labels={"TOTAL" : "Total Usage", "VERSION_NAME" : 'Package Version Name'},
                    title = title, hover_data=["TOTAL"],
                    template="gridon",height=500)
        st.plotly_chart(fig,use_container_width=True)

    

    
#     if(productNameSelect != None and len(productNameSelect) > 0 and len(customEntitySelect) == 0 ):
#         getProductDetails = DataBase.getProductDetails(dbConnect, productNameSelect)
#         packageVersion = DataBase.getPackageVersion(dbConnect, productNameSelect)
#         # print(' customEntitySelect ::::::::::::', customEntitySelect)
#         if(getProductDetails != None and len(getProductDetails) > 0 and packageVersion != None and len(packageVersion) > 0 ):
#             title = 'Over all Usage of ' + productNameSelect
#             fig = px.bar(getProductDetails[0], x = "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE", labels={"OVER_ALL_USAGE" : "Total Usage", 'LOG_CREATED_MONTH' : 'Months'},
#                         title = title, hover_data=["OVER_ALL_USAGE"],
#                         template="gridon",height=500)
#             st.plotly_chart(fig,use_container_width=True)

#             # ## # 3
#             title = 'Package Version Usage of ' + productNameSelect
#             fig = px.bar(packageVersion[0], x = "VERSION_NAME", y = "TOTAL", labels={"TOTAL" : "Total Usage", "VERSION_NAME" : 'Package Version Name'},
#                         title = title, hover_data=["TOTAL"],
#                         template="gridon",height=500)
#             st.plotly_chart(fig,use_container_width=True)

#     elif(productNameSelect != None and len(productNameSelect) > 0 and len(customEntitySelect) > 0 ):
#         if len(customEntitySelect) == 1:
#             isSingleValue = True
#             customEntitySelectList = customEntitySelect[0]
#             filteredLits = featureList[0][customEntitySelectList]
#         else:
#             isSingleValue = False
#             # filteredLits = ()
#             finaldata = []
#             for item in customEntitySelect:
#                 customEntitySelectList = featureList[0][item]
                
#                 finaldata.append(customEntitySelectList)
#             filteredLits =  tuple(finaldata)

#         filtedData = DataBase.getFeatureDetails(dbConnect, productNameSelect,isSingleValue, filteredLits)
#         if(filtedData != None and len(filtedData) > 0):
#             title = 'Feature'
#             fig = px.bar(filtedData[0], x = "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE", labels={"OVER_ALL_USAGE" : "Total Usage", 'LOG_CREATED_MONTH' : 'Months'},
#                         title = title, hover_data=["OVER_ALL_USAGE"],
#                         template="gridon",height=500)
#             st.plotly_chart(fig,use_container_width=True)






