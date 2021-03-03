def outlier_report(df,vars_to_examine=df.columns,color='red',thres=4):
    '''
    Parameters
    ----------
    df : DATAFRAME
        Input dataframe
    vars_to_examine : LIST, optional
        List of variables to examine from dataframe. The default is df.columns.
    color : STRING, optional
        Color for cell highlighting. The default is 'red'.
    thres : int, optional
        Highlight cells where z score is above thres. The default is 4.

    
    Returns
    -------
    Table with distribution of z-scores of variables of interest. 
    '''
        
    def highlight_extreme(s):
        '''
        highlight the maximum in a Series yellow.
        '''
        is_extreme = abs(s) > thres
        return ['background-color: '+color if v else '' for v in is_extreme]
    
    
    return (# compute z scores
     ((df[vars_to_examine] - df[vars_to_examine].mean())/df[vars_to_examine].std())
     # output dist of z   
     .describe(percentiles=[.01,.05,.25,.5,.75,.95,.99]).T
     # add a new column = highest of min and max column
     .assign(max_z_abs = lambda x: x[['min','max']].abs().max(axis=1))
     # now sort on it
     .sort_values('max_z_abs',ascending = False)
     .style.format('{:,.2f}')
           .format({"count": '{:,.0f}'})           
           .apply(highlight_extreme, 
                  subset=['mean', 'std', 'min', '1%', '5%', '25%', '50%', '75%', '95%','99%', 'max', 'max_z_abs'])
    ) 
