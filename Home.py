import streamlit as st
import db as DataBase
import plotly.express as px
import ast
import staticData as userData

st.set_page_config(layout="wide")


col1, col2 = st.columns(2)

with col1:
    productNameSelect = st.selectbox( "Select Product", ("AGrid", "User 360", "Media Manager", "Snap Data"),  index=None, placeholder="Select Product method...") 

with col2:
    featureList = userData.featureList()
    print('productNameSelect :::::::;', productNameSelect)
    # print('featureList :::::::::', featureList)
    if(productNameSelect and featureList):
        customEntitySelect = st.multiselect('select Feature',featureList[0].keys() )

submitButton = st.button('Submit')

if(submitButton):
    print('start.....')

    dbConnect = DataBase.connectSnowflake()
    if(productNameSelect != None and len(productNameSelect) > 0 and len(customEntitySelect) == 0 ):
        getProductDetails = DataBase.getProductDetails(dbConnect, productNameSelect)
        packageVersion = DataBase.getPackageVersion(dbConnect, productNameSelect)
        # print(' customEntitySelect ::::::::::::', customEntitySelect)
        if(getProductDetails != None and len(getProductDetails) > 0 and packageVersion != None and len(packageVersion) > 0 ):
            title = 'Over all Usage of ' + productNameSelect
            fig = px.bar(getProductDetails[0], x = "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE", labels={"OVER_ALL_USAGE" : "Total Usage", 'LOG_CREATED_MONTH' : 'Months'},
                        title = title, hover_data=["OVER_ALL_USAGE"],
                        template="gridon",height=500)
            st.plotly_chart(fig,use_container_width=True)

            # ## # 3
            title = 'Package Version Usage of ' + productNameSelect
            fig = px.bar(packageVersion[0], x = "VERSION_NAME", y = "TOTAL", labels={"TOTAL" : "Total Usage", "VERSION_NAME" : 'Package Version Name'},
                        title = title, hover_data=["TOTAL"],
                        template="gridon",height=500)
            st.plotly_chart(fig,use_container_width=True)

    elif(productNameSelect != None and len(productNameSelect) > 0 and len(customEntitySelect) > 0 ):
        if len(customEntitySelect) == 1:
            isSingleValue = True
            customEntitySelectList = customEntitySelect[0]
            filteredLits = featureList[0][customEntitySelectList]
        else:
            isSingleValue = False
            # filteredLits = ()
            finaldata = []
            for item in customEntitySelect:
                customEntitySelectList = featureList[0][item]
                
                finaldata.append(customEntitySelectList)
            filteredLits =  tuple(finaldata)

        filtedData = DataBase.getFeatureDetails(dbConnect, productNameSelect,isSingleValue, filteredLits)
        if(filtedData != None and len(filtedData) > 0):
            title = 'Feature'
            fig = px.bar(filtedData[0], x = "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE", labels={"OVER_ALL_USAGE" : "Total Usage", 'LOG_CREATED_MONTH' : 'Months'},
                        title = title, hover_data=["OVER_ALL_USAGE"],
                        template="gridon",height=500)
            st.plotly_chart(fig,use_container_width=True)






