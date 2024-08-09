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

def getProductDetails(connection, productName, filters):
    queryString = "select sum(num_events) AS OVER_ALL_USAGE, LOG_CREATED_MONTH from package_usage_summary where package_name='"+productName+"' and ORGANIZATION_EDITION != 'Developer Edition' and organization_status='Active' AND USER_TYPE in ('CspLitePortal', 'Standard' )"
    if(filters and filters['isFilter']):
        if(filters['isOrgFilter']):
            queryString = queryString + "AND concat(REPLACE(organization_name, '''', ''), '-', organization_id) = '" + filters['orgName'] + "'"

        if(filters['isDateFromFilter'] and filters['isDateToFilter']):
            fromDate = filters['fromDate']
            toDate = filters['toDate']
            queryString = queryString + "AND LOG_CREATED_MONTH >= '" + fromDate[:7] +"' AND LOG_CREATED_MONTH <= '" + toDate[:7] +"' "

        if(filters['isFeatureFilter']):
            queryString = queryString + "AND custom_entity = '" + filters['featuesName'] + "' "
        elif(filters['isFeatureFilter'] == False):
            queryString = queryString + "AND custom_entity = 'ListViewController' "


    queryString = queryString + " group by LOG_CREATED_MONTH order by LOG_CREATED_MONTH ASC;"
    print('getProductDetails :::::::: queryString ::::::::::', queryString)
    query1 = connection.execute_string(queryString)
    
    outData = resultProcess(query1)
    return outData

def getnumberOfUsers(connection, productName, filters):
    print('filters ::::::::::', filters)

    queryString = "select count(USER_COUNT) OVER_ALL_USAGE, log_created_month from( select COUNT(DISTINCT USER_ID_TOKEN) AS USER_COUNT,log_created_month from package_usage_summary where package_name='"+productName+"' and ORGANIZATION_EDITION != 'Developer Edition' and organization_status='Active' AND USER_TYPE in ('CspLitePortal', 'Standard' ) AND custom_entity = 'ListViewController'"

    
    print('queryString :::::::::', queryString)
    if(filters and filters['isFilter']):
        if(filters['isOrgFilter']):
            queryString = queryString + "AND concat(REPLACE(organization_name, '''', ''), '-', organization_id) = '" + filters['orgName'] + "'"

        if(filters['isDateFromFilter'] and filters['isDateToFilter']):
            fromDate = filters['fromDate']
            toDate = filters['toDate']
            queryString = queryString + "AND LOG_CREATED_MONTH >= '" + fromDate[:7] +"' AND LOG_CREATED_MONTH <= '" + toDate[:7] +"' "

    queryString = "group by user_id_token, log_created_month ) group by log_created_month order by log_created_month limit 2;"

    print('getnumberOfCreates :::::::: queryString ::::::::::', queryString)

    query1 = connection.execute_string(queryString)
    
    outData = resultProcess(query1)
    print('outData ::::::::::::::::::::::', outData)

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
        queryString = "select sum(num_events) AS total,custom_entity from package_usage_summary where package_name='"+ productName+"' AND concat(organization_name, '-', organization_id) =  '" + orgName+ "' AND custom_entity IN {} AND ORGANIZATION_EDITION != 'Developer Edition' group by custom_entity order by total DESC;".format(filteredLits)
    else:
        queryString = "select sum(num_events) AS total,custom_entity from package_usage_summary where package_name='"+ productName+"' AND custom_entity IN {} AND ORGANIZATION_EDITION != 'Developer Edition' group by custom_entity order by total DESC;".format(filteredLits)
    query1 = connection.execute_string(queryString)
    outData = resultProcess(query1)

    return outData

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

    queryString = "select REPLACE(organization_name, '''', '') as organization_name ,organization_id from package_usage_summary where package_name='"+ productName+"' AND ORGANIZATION_EDITION != 'Developer Edition'  and organization_status='Active' group by organization_name, organization_id order by organization_name ASC"
    query1 = connection.execute_string(queryString)
    outData = resultProcess(query1)
    return outData

def getProductDetailsWithfeature(connection, productName, filters, filteredLits):

    queryString = "select sum(num_events) AS OVER_ALL_USAGE, LOG_CREATED_MONTH, custom_entity from package_usage_summary where package_name='"+ productName+"' AND custom_entity IN {} AND ORGANIZATION_EDITION != 'Developer Edition' ".format(filteredLits)
    if(filters and filters['isFilter']):
        if(filters['isOrgFilter']):
            queryString = queryString + "AND concat(REPLACE(organization_name, '''', ''), '-', organization_id) = '" + filters['orgName'] + "'"

        if(filters['isDateFromFilter'] and filters['isDateToFilter']):
            fromDate = filters['fromDate']
            toDate = filters['toDate']
            queryString = queryString + "AND LOG_CREATED_MONTH >= '" + fromDate[:7] +"' AND LOG_CREATED_MONTH <= '" + toDate[:7] +"' "


    queryString = queryString + "group by LOG_CREATED_MONTH, custom_entity order by OVER_ALL_USAGE DESC;"
    
    print('getProductDetailsWithfeature ::::::::::::::::: queryString ::::::::::', queryString)
    query1 = connection.execute_string(queryString)
    
    outData = resultProcess(query1)
    return outData

def getFeaturesUsageWithOrg(connection, productName, filters):

    queryString = "select sum(num_events) AS OVER_ALL_USAGE, organization_name, LOG_CREATED_MONTH from package_usage_summary  where package_name='"+ productName+"' "
    if(filters and filters['isFilter']):

        if(filters['isDateFromFilter'] and filters['isDateToFilter']):
            fromDate = filters['fromDate']
            toDate = filters['toDate']
            queryString = queryString + "AND LOG_CREATED_MONTH >= '" + fromDate[:7] +"' AND LOG_CREATED_MONTH <= '" + toDate[:7] +"' "
        
        if(filters['isFeatureFilter']):
            queryString = queryString + "AND custom_entity = '" + filters['featuesName'] + "' "
        

    queryString = queryString + "group by LOG_CREATED_MONTH, organization_name order by OVER_ALL_USAGE DESC;"
    
    print('getProductDetailsWithfeature ::::::::::::::::: queryString ::::::::::', queryString)
    query1 = connection.execute_string(queryString)
    
    outData = resultProcess(query1)
    return outData
