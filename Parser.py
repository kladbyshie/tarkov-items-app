import pandas as pd
from datetime import date

#parser that pulls info from the barteritems xlsx and creates a dataframe for all passed itemvars. Allows partial searches due to using "in" keyword. If there are 0 matches, passes a messaage.
def parser(itemvar):
    df = pd.read_excel('barteritems.xlsx')
    itemdf = pd.DataFrame()
    for lineitem in df['Items and Quantities']:
        if itemvar.upper() in lineitem.upper():
            result = df.loc[df['Items and Quantities'] == lineitem]
            itemdf = itemdf.append(result)
    itemdf.sort_index(axis=0, inplace = True)
    if len(itemdf) == 0:
        message = 'The name is misspelled, or this item is not involved in any barter trades'
        return(message)
    else:
        return(itemdf)

#parser that pulls info from the current date csv and creates a dataframe for all passed itemvars. Allows partial searches due to using "in" keyword. If there are 0 matches, passes a message.
def marketparser(itemvar):
    today = date.today()
    itemlist = pd.read_csv(f'{today}.csv', index_col=False)
    marketdf = pd.DataFrame()
    for lineitem in itemlist['Name']:
        if itemvar.upper() in lineitem.upper():
            marketdf = marketdf.append(itemlist.loc[itemlist['Name'] == lineitem])
    if len(marketdf) == 0:
        message = 'The name is misspelled, or this item is not available on the flea market'
        return(message)
    else:
        return(marketdf)