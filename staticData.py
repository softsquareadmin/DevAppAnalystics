def getAgridFeatureList():

    data = [{
        'Column Filters' : 'agrid:columnFilter', 'Multi Column Sorting , Sorting' : 'agrid:defaultSorting', 'Inline edit' : 'agrid:inlineEdit', 'Preference(End user)' : 'agrid:userPreference', 
        'Preference Sharing' : 'agrid:preferenceSharing', 'Managed Preference' : 'PreferenceController',
        'Actions (Row, List)' : 'agrid:pubsub', 'Standard actions (Create, Delete, View)' : 'agrid:listViewNewRecord', 'Conditional Rendering': 'ConditionalFormattingRuleController', 
        'Intelligent Related List' : 'RelatedObjectController', 'Import Configuration' : 'agrid:importConfigurations', 
        'Bulk Create' : 'BlukRecordCreate', 'Configuration Group' : 'ConfigurationGroupController', 'Mobile version': 'agrid:cardView', 'Summary' : 'agrid:summary',
        'Group By' : 'agrid:groupByListView'
    }]
    return data

def getMediaManagerFeatureList():
    
    data = [{
        'List View':'mdia:listView', 'Tile View' : 'mdia:tileView', 'column Filter': 'mdia:columnFilter', 'File Share' : 'fileShare',  'Import Configuration' : 'mdia:importConfigurations', 
        'Upload Files' : 'mdia:fileUpload', 'List View, Tile View - Gloabl Search' : 'mdia:viewHeader', 'Slider - Global Search' : 'mdia:sliderHeader', 'File Type Filter' : 'mdia:viewHeader',
        'File Browser' : 'mdia:fileBrowser', 'Configuration Filter/column/Action [Add, update and delete Actions]' : 'mdia:mmConfiguration', 'FileBrowser Configuration - Filters/Column' : 'FileBrowserConfigurationController'
    }]

    return data