import streamlit as st
import db as DataBase
import plotly.express as px
import ast

dbConnect = DataBase.connectSnowflake()

st.set_page_config(layout="wide")
# st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


isFilter = False

with st.sidebar:

    productNameSelect = st.selectbox( "Select Product", ("AGrid", "User 360", "Media Manager", "Snap Data"),  index=None, placeholder="Select Product method...")
    print('option :::::::', productNameSelect)

    if(productNameSelect != None and len(productNameSelect) > 0):

        getProductDetails = DataBase.getProductDetails(dbConnect, productNameSelect)
    #     TopAndLeast = DataBase.getTopAndLeast(dbConnect, productNameSelect)
        packageVersion = DataBase.getPackageVersion(dbConnect, productNameSelect)

        customEntitySelect = st.multiselect('', getProductDetails[1])
        st.write('You selected:', customEntitySelect)

        submitButton = st.button('Submit')

        print('submitButton :::::', submitButton)

        if(len(productNameSelect) > 0 and submitButton and len(customEntitySelect) > 0):
            print('customEntitySelect ::::::::::::', customEntitySelect)
            isFilter = True

            if len(customEntitySelect) == 1:
                isSingleValue = True
                filteredLits = customEntitySelect[0]
            else:
                isSingleValue = False
                filteredLits = tuple(customEntitySelect)

            # tuple_str = str(filteredLitss)
            # if tuple_str.endswith(','):
            #     tuple_str = tuple_str[:-1]
            # if len(customEntitySelect) == 1:
            #     filteredLits = filteredLits[:-1]

            # filteredLits = ast.literal_eval(tuple_str)

            print('Apply Filter :::::', filteredLits)
            filtedData = DataBase.getFeatureDetails(dbConnect, productNameSelect,isSingleValue, filteredLits)

            noCreates = DataBase.getnumberOfCreates(dbConnect, productNameSelect, isSingleValue, filteredLits)
            noUpdates = DataBase.getnumberOfUpdates(dbConnect, productNameSelect, isSingleValue, filteredLits)
            noDeletes = DataBase.getnumberOfDeletes(dbConnect, productNameSelect, isSingleValue, filteredLits)

            print('filtedData ::::::::::::::::::::', filtedData)
    



if productNameSelect == None :
    st.write('Welcome !')

#     allDataUsage = DataBase.getAllProductData(dbConnect)

#     # ## # 1
#     title = 'Over all Usage'
#     fig = px.bar(allDataUsage[0], x = "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE", labels={"OVER_ALL_USAGE" : "Total Usage", 'LOG_CREATED_MONTH' : 'Months'},
#                  title = title, hover_data=["OVER_ALL_USAGE"],
#                  template="gridon",height=500)
#     st.plotly_chart(fig,use_container_width=True)
#     # col1, col2 = st.columns([10,10])

#     # with col1:
#     #     st.write('All Product Usage')

#     #     print('allDataUsage :::::', allDataUsage)

#     #     st.line_chart(data = allDataUsage[0], x= "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE")
    
#     # with col2:
#     #     st.write('User Count')

# print('productNameSelect :::::::::::::::::::::::', productNameSelect)

if(productNameSelect != None and len(productNameSelect) > 0):
    # print('getProductDetails :::::::::::::::::', getProductDetails)

#     col1, col2, col3, col4, col5, col6 = st.columns(6)
#     col1.metric("Total Installs", getProductDetails[2]['TOTAL'][0])
#     col2.metric("Production Installs", getProductDetails[3]['PRODUCTION'][0])
#     col3.metric("Sandbox Installs",getProductDetails[4]['SANDBOX'][0])
#     col4.metric("Active Accounts", getProductDetails[5]['ACTIVE_ACCOUNT'][0])
#     col5.metric("Trail Accounts",getProductDetails[6]['TRIAL_ACCOUNT'][0])
#     col6.metric("Uninstalls", getProductDetails[7]['UNINSTALL'][0])


    # ## # 1
    if isFilter and isFilter == True:
        col1, col2, col3 = st.columns(3)
        if str(noCreates[0]['SUM_OF_CREATES'][0]) != "NaN" and str(noCreates[0]['SUM_OF_CREATES'][0]) != "nan":
            numberOfCreate = str(noCreates[0]['SUM_OF_CREATES'][0])
        else:
            numberOfCreate = 0

        if str(noUpdates[0]['SUM_OF_UPDATES'][0]) != "NaN"  and str(noUpdates[0]['SUM_OF_UPDATES'][0]) != "nan":
            numberOfUpdate = str(noUpdates[0]['SUM_OF_UPDATES'][0])
        else:
            numberOfUpdate = 0

        if str(noDeletes[0]['SUM_OF_DELETES'][0]) != "NaN" and str(noDeletes[0]['SUM_OF_DELETES'][0]) != "nan" :
            numberOfdelete = str(noDeletes[0]['SUM_OF_DELETES'][0])
        else:
            numberOfdelete = 0

        col1.metric("Number of Creates",numberOfCreate )
        col2.metric("Number of Update",numberOfUpdate)
        col3.metric("Number of delete",numberOfdelete)

        title = 'Filter'
        fig = px.bar(filtedData[0], x = "LOG_CREATED_MONTH", y = "OVER_ALL_USAGE", labels={"OVER_ALL_USAGE" : "Total Usage", 'LOG_CREATED_MONTH' : 'Months'},
                    title = title, hover_data=["OVER_ALL_USAGE"],
                    template="gridon",height=500)
        st.plotly_chart(fig,use_container_width=True)
        
    else:
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


#     # ## # 2
#     col2_1, col2_2 =  st.columns(2)
#     with col2_1:
#         title = 'Top 15 components In ' + productNameSelect

#         fig = px.line(TopAndLeast[0], x = "CUSTOM_ENTITY", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'CUSTOM_ENTITY' : "Component's Name"},
#                     title = title, hover_data=["TOTAL"],
#                     template="gridon",height=500)
#         st.plotly_chart(fig,use_container_width=True)

#         title = 'Top 15 components In ' + productNameSelect

#         fig = px.bar(TopAndLeast[0], x = "CUSTOM_ENTITY", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'CUSTOM_ENTITY' : "Component's Name"},
#                     title = title, hover_data=["TOTAL"],
#                     template="gridon",height=500)
#         st.plotly_chart(fig,use_container_width=True)

#     with col2_2:
#         title = 'Least 10 components In ' + productNameSelect

#         fig = px.line(TopAndLeast[1], x = "CUSTOM_ENTITY", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'CUSTOM_ENTITY' : "Component's Name"},
#                     title = title, hover_data=["TOTAL"],
#                     template="gridon",height=500)
#         st.plotly_chart(fig,use_container_width=True)

#         title = 'Least 10 components In ' + productNameSelect

#         fig = px.bar(TopAndLeast[1], x = "CUSTOM_ENTITY", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'CUSTOM_ENTITY' : "Component's Name"},
#                     title = title, hover_data=["TOTAL"],
#                     template="gridon",height=500)
#         st.plotly_chart(fig,use_container_width=True)


    

#     # title = 'Package Version Usage of ' + productNameSelect
#     # fig = px.bar(packageVersion[1], x = "VERSION_NAME", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'Package Version Name' : 'Months'},
#     #              title = title, hover_data=["TOTAL"],
#     #              template="gridon",height=500)
#     # st.plotly_chart(fig,use_container_width=True)

#     # title = 'Package Version Usage of ' + productNameSelect
#     # fig = px.bar(packageVersion[2], x = "VERSION_NAME", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'Package Version Name' : 'Months'},
#     #              title = title, hover_data=["TOTAL"],
#     #              template="gridon",height=500)
#     # st.plotly_chart(fig,use_container_width=True)

#     # title = 'Package Version Usage of ' + productNameSelect
#     # fig = px.bar(packageVersion[3], x = "VERSION_NAME", y = "TOTAL", labels={"TOTAL" : "Total Usage", 'Package Version Name' : 'Months'},
#     #              title = title, hover_data=["TOTAL"],
#     #              template="gridon",height=500)
#     # st.plotly_chart(fig,use_container_width=True)



    






    



    
