def featureList():
    data = [
            {'Column Filters' : 'agrid:columnFilter', 'Multi Column Sorting , Sorting' : 'agrid:defaultSorting', 'Inline edit' : 'agrid:inlineEdit', 'Preference(End user)' : 'agrid:userPreference', 
             'Preference Sharing' : 'agrid:preferenceSharing', 'Managed Preference' : 'PreferenceController',
            'Actions (Row, List)' : 'agrid:pubsub', 'Standard actions (Create, Delete, View)' : 'agrid:listViewNewRecord', 'Conditional Rendering': 'ConditionalFormattingRuleController', 
            'Intelligent Related List' : 'RelatedObjectController', 'Import Configuration' : 'agrid:importConfigurations', 
            'Bulk Create' : 'BlukRecordCreate', 'Configuration Group' : 'ConfigurationGroupController', 'Mobile version': 'agrid:cardView', 'Summary' : 'agrid:summary',
             'Group By' : 'agrid:groupByListView', }]
    return data