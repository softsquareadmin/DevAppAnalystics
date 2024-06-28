import snowflake.connector
import streamlit as st

def connectSnowflake():
    try:

        print('Database Connection Start')
        conn = snowflake.connector.connect(
                    user = st.secrets["user"],
                    password = st.secrets["password"],
                    account = st.secrets["account"],
                    warehouse = st.secrets["warehouse"],
                    database = st.secrets["database"],
                    schema = st.secrets["schema"]
                    )
        # cur = conn.cursor()
        print('Database Connection Done! ')
        return conn
    
    except Exception as err:
        print('Error on Database Connection:::')

def resultProcess(curser):
    print('data process start...')
    dataList = []
    for cursor in curser:
        df = cursor.fetch_pandas_all()
        dataList.append(df)
    return dataList


# def getAllProductData(connection):
#     print('Start...')

#     query1 = connection.execute_string(
#         "select count(*) AS Over_All_Usage, log_created_month from package_usage_summary group by log_created_month;"
#         )
#     outData = resultProcess(query1)
#     # print('outData:::::', outData)

#     return outData

def getProductDetails(connection, productName, filters):
    print('filters :::::::::', filters)
    queryString = "select count(*) AS OVER_ALL_USAGE, LOG_CREATED_MONTH from package_usage_summary where package_name='"+productName+"' and ORGANIZATION_EDITION != 'Developer Edition'"
    if(filters and filters['isFilter']):
        if(filters['isOrgFilter']):
            queryString = queryString + "AND concat(REPLACE(organization_name, '''', ''), '-', organization_id) = '" + filters['orgName'] + "'"

        if(filters['isDateFromFilter'] and filters['isDateToFilter']):
            fromDate = filters['fromDate']
            toDate = filters['toDate']
            queryString = queryString + "AND LOG_CREATED_MONTH >= '" + fromDate[:7] +"' AND LOG_CREATED_MONTH <= '" + toDate[:7] +"' "

        if(filters['isFeatureFilter']):
            queryString = queryString + "AND custom_entity = '" + filters['featuesName'] + "' "

    queryString = queryString + " group by LOG_CREATED_MONTH order by LOG_CREATED_MONTH ASC;"
    # if(isOrgFilter):
    #     queryString = "select count(*) AS OVER_ALL_USAGE, LOG_CREATED_MONTH from package_usage_summary where package_name='"+productName+"' and ORGANIZATION_EDITION != 'Developer Edition' AND concat(organization_name, '-', organization_id) =  '" + orgName+ "' group by LOG_CREATED_MONTH order by LOG_CREATED_MONTH ASC;"
    # else:
    #     queryString = "select count(*) AS OVER_ALL_USAGE, LOG_CREATED_MONTH from package_usage_summary where package_name='"+productName+"' and ORGANIZATION_EDITION != 'Developer Edition' group by LOG_CREATED_MONTH order by LOG_CREATED_MONTH ASC;"
    print('queryString ::::::::::', queryString)
    query1 = connection.execute_string(queryString)
    
    # "select custom_entity from  package_usage_summary where package_name='"+ productName+"' AND ORGANIZATION_EDITION != 'Developer Edition' group by custom_entity;"
    outData = resultProcess(query1)

    return outData

# def getFeatureDetails(connection, productName,isSingleValue, filteredLits):
#     if(isSingleValue == True):
#         query1 = connection.execute_string(
#             "select count(*) AS OVER_ALL_USAGE, log_created_month from package_usage_summary where package_name='"+ productName+"' AND custom_entity = '"+ filteredLits +"' AND ORGANIZATION_EDITION != 'Developer Edition' group by custom_entity, log_created_month order by LOG_CREATED_MONTH ASC;"
#             )
#     else: 
#         query1 = connection.execute_string(
#             "select count(*) AS OVER_ALL_USAGE, log_created_month from package_usage_summary where package_name='"+ productName+"' AND custom_entity IN {} AND ORGANIZATION_EDITION != 'Developer Edition' group by custom_entity, log_created_month order by LOG_CREATED_MONTH ASC;".format(filteredLits)
#             )
#     outData = resultProcess(query1)

#     print('outData ::::::', outData)

#     return outData

def getnumberOfCreates(connection, productName, isSingleValue, filteredLits):
    if(isSingleValue == True):
        query1 = connection.execute_string(
            "select sum(num_creates) AS SUM_OF_CREATES from package_usage_summary where package_name='"+ productName+"' AND custom_entity = '"+ filteredLits +"' AND ORGANIZATION_EDITION != 'Developer Edition';"
            )
    else: 
        query1 = connection.execute_string(
            "select sum(num_creates) AS SUM_OF_CREATES from package_usage_summary where package_name='"+ productName+"' AND custom_entity IN {} AND ORGANIZATION_EDITION != 'Developer Edition';".format(filteredLits)
            )
    outData = resultProcess(query1)

    print('outData ::::::', outData)

    return outData

def getnumberOfUpdates(connection, productName,isSingleValue, filteredLits):
    if(isSingleValue == True):
        query1 = connection.execute_string(
            "select sum(num_updates) AS SUM_OF_UPDATES from package_usage_summary where package_name='"+ productName+"' AND custom_entity = '"+ filteredLits +"';"
            )
    else: 
        query1 = connection.execute_string(
            "select sum(num_updates) AS SUM_OF_UPDATES from package_usage_summary where package_name='"+ productName+"' AND custom_entity IN {};".format(filteredLits)
            )
    outData = resultProcess(query1)

    print('outData ::::::', outData)

    return outData

def getnumberOfDeletes(connection, productName, isSingleValue, filteredLits):
    if(isSingleValue == True):
        query1 = connection.execute_string(
            "select sum(num_deletes) AS SUM_OF_DELETES from package_usage_summary where package_name='"+ productName+"' AND custom_entity = '"+ filteredLits +"';"
            )
    else: 
        query1 = connection.execute_string(
            "select sum(num_deletes) AS SUM_OF_DELETES from package_usage_summary where package_name='"+ productName+"' AND custom_entity IN {};".format(filteredLits)
            )
    outData = resultProcess(query1)

    print('outData ::::::', outData)

    return outData

def getFeatureDetails(connection, productName, filteredLits, isOrgFilter, orgName):

    if(isOrgFilter):
        queryString = "select count(*) AS total,custom_entity from package_usage_summary where package_name='"+ productName+"' AND concat(organization_name, '-', organization_id) =  '" + orgName+ "' AND custom_entity IN {} AND ORGANIZATION_EDITION != 'Developer Edition' group by custom_entity order by total DESC;".format(filteredLits)
    else:
        queryString = "select count(*) AS total,custom_entity from package_usage_summary where package_name='"+ productName+"' AND custom_entity IN {} AND ORGANIZATION_EDITION != 'Developer Edition' group by custom_entity order by total DESC;".format(filteredLits)
    query1 = connection.execute_string(queryString)
    outData = resultProcess(query1)

    # print('outData ::::::::::::::',outData)

    return outData


# def getTopAndLeast(connection, productName):
#     print('productName ::::::::::::::', productName)

#     query1 = connection.execute_string(
#         "select count(*) AS total,custom_entity from package_usage_summary where package_name='"+ productName+"'  group by custom_entity order by total DESC limit 15;"
#         "select count(*) AS total,custom_entity from package_usage_summary where package_name='"+ productName+"'  group by custom_entity order by total ASC limit 15;"
#         )
#     outData = resultProcess(query1)

#     return outData

def getPackageVersion(connection, productName, filters):
    queryString = "select count(*) AS TOTAl,VERSION_NAME  from (select VERSION_NAME,organization_name from subscriber_snapshot where package_name='"+ productName+"' AND organization_status= 'ACTIVE'"
    print('filtes ::::::::::', filters)
    if(filters and filters['isFilter']):
        if(filters['isDateFromFilter'] and filters['isDateToFilter']):
            queryString = queryString + "AND LOG_CREATED_DATE >= '" + filters['fromDate'] +"' AND LOG_CREATED_DATE <= '" + filters['toDate'] +"'"

        if(filters['isOrgFilter']):
            queryString = queryString + "AND concat(REPLACE(organization_name, '''', ''), '-', organization_id) = '" + filters['orgName'] + "'"
    
    queryString = queryString + "group by VERSION_NAME, organization_name) group by VERSION_NAME ORDER BY TOTAl DESC;"

    print('queryString :::::', queryString)



    query1 = connection.execute_string(queryString)
            # "select count(*) AS TOTAl,VERSION_NAME  from (select VERSION_NAME,organization_name from subscriber_snapshot where package_name='"+ productName+"' AND organization_status= 'ACTIVE' group by VERSION_NAME, organization_name) group by VERSION_NAME ORDER BY TOTAl DESC"
            # "select count(*) AS TOTAL,VERSION_NAME  from (select VERSION_NAME,organization_name from subscriber_snapshot where package_name='"+ productName+"' group by VERSION_NAME, organization_name) group by VERSION_NAME;"

    outData = resultProcess(query1)

    return outData


def getOrganizationName(connection, productName):

    query1 = connection.execute_string(
        "select REPLACE(organization_name, '''', '') as organization_name ,organization_id from package_usage_summary where package_name='"+ productName+"' AND ORGANIZATION_EDITION != 'Developer Edition'  group by organization_name, organization_id order by organization_name ASC"
        )
            # "select count(*) AS TOTAL,VERSION_NAME  from (select VERSION_NAME,organization_name from subscriber_snapshot where package_name='"+ productName+"' group by VERSION_NAME, organization_name) group by VERSION_NAME;"

    outData = resultProcess(query1)

    # print('outData :::::::::::', outData)

    return outData





# "select custom_entity from  package_usage_summary where package_name='"+ productName+"' group by custom_entity;"
# "select count(*) AS OVER_ALL_USAGE, LOG_CREATED_MONTH from package_usage_summary where package_name='"+productName+"' group by LOG_CREATED_MONTH order by LOG_CREATED_MONTH ASC;"
# "select count(*) AS total from (select *  from appanalytics.syncout.license where package_name='"+productName+"' AND internal_status IN ('Internal', 'Customer', 'Process', 'Lost', 'On-hold', 'Partner') AND ORG_TYPE  != 'Developer Edition');"
# "select count(*) AS production from (select *  from appanalytics.syncout.license where package_name='"+productName+"' AND internal_status IN ('Internal', 'Customer', 'Process', 'Lost', 'On-hold', 'Partner')  AND subscriber_org_is_sandbox = false AND ORG_TYPE  != 'Developer Edition');"
# "select count(*) AS sandbox from (select *  from appanalytics.syncout.license where package_name='"+productName+"' AND internal_status IN ('Internal', 'Customer', 'Process', 'Lost', 'On-hold', 'Partner')  AND subscriber_org_is_sandbox = true AND ORG_TYPE  != 'Developer Edition');"
# "select count(*) AS active_account from (select *  from appanalytics.syncout.license where package_name='"+productName+"'  AND status= 'Active' AND internal_status IN ('Internal', 'Customer', 'Process', 'Lost', 'On-hold', 'Partner') AND subscriber_org_is_sandbox = false AND ORG_TYPE  != 'Developer Edition');"
# "select count(*) AS trial_account from (select *  from appanalytics.syncout.license where package_name='"+productName+"'  AND status= 'Trial' AND internal_status IN ('Internal', 'Customer', 'Process', 'Lost', 'On-hold', 'Partner') AND subscriber_org_is_sandbox = false AND ORG_TYPE  != 'Developer Edition');"
# "select count(*) AS uninstall from (select *  from appanalytics.syncout.license where package_name='"+productName+"'   AND status= 'Uninstalled' AND internal_status IN ('Internal', 'Customer', 'Process', 'Lost', 'On-hold', 'Partner') AND ORG_TYPE  != 'Developer Edition')"

