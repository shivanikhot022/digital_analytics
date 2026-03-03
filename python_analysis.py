# %%
import pandas as pd 
import matplotlib.pyplot as plt 

# %%
orders = pd.read_csv('orders.csv')
orders.head(5)

# %%
order_items = pd.read_csv('order_items.csv')
order_items.head(5)

# %%
order_item_refunds = pd.read_csv('order_item_refunds.csv')
order_item_refunds.head(5)

# %%
website_sessions = pd.read_csv('website_sessions.csv')
website_sessions.head(5)

# %%
website_pageviews = pd.read_csv('website_pageviews.csv')
website_pageviews.head(5)

# %%
products = pd.read_csv('products.csv')
products.head(5)

# %%
### Business Overview 
Total_orders = orders['order_id'].count()
Total_Cost = orders['cogs_usd'].sum()
Total_Revenue = orders['price_usd'].sum()
Total_Refunded_Amt = order_item_refunds['refund_amount_usd'].sum()
Refunded_items_Cost = pd.merge(order_items,order_item_refunds,how = 'right',on = 'order_item_id')['cogs_usd'].sum()
Total_Net_Revenue = Total_Revenue - Total_Refunded_Amt
Total_Net_Cost = Total_Cost - Refunded_items_Cost
Profit = Total_Net_Revenue - Total_Net_Cost
Profit_Margin = (Profit/Total_Net_Revenue)*100

print(f'Total_orders : ',Total_orders)
print(f'Total_Cost :',Total_Cost)
print(f'Gross_Revenue :',Total_Revenue)
print(f'Total_Refunded_Amt :',Total_Refunded_Amt)
print(f'Refunded_items_Cost :',Refunded_items_Cost)
print(f'Total_Net_Revenue :', Total_Net_Revenue)
print(f'Total_Net_Cost :',Total_Net_Cost)
print(f'Profit :',Profit)
print(f'Profit_Margin:',Profit_Margin)

# %%
#### Business Trends 

orders['created_at'] = pd.to_datetime(orders['created_at'])
orders['year'] = orders.created_at.dt.year
orders['month'] = orders['created_at'].dt.month

# %%
starting_3_year_data = orders[orders['year'].isin([2012,2013,2014])]
starting_3_year_data

# %%
### Gross Revenue change year on year 

year_Gross_revenue = starting_3_year_data.groupby('year')['price_usd'].sum().sort_index().reset_index()
previous_year_revenue = year_Gross_revenue['price_usd'].shift(1)
YOY_change = ((year_Gross_revenue['price_usd']-previous_year_revenue)/previous_year_revenue)*100
YOY_change = YOY_change.fillna(0)
Year_wise_Revenue_change = pd.DataFrame({'Years':year_Gross_revenue['year'],'YOY_change':YOY_change})
Year_wise_Revenue_change['Years'] = Year_wise_Revenue_change['Years'].astype('int')


month_Gross_revenue = starting_3_year_data.groupby('month')['price_usd'].sum().sort_index().reset_index()
previous_month_revenue = month_Gross_revenue['price_usd'].shift(1)
MOM_change = ((month_Gross_revenue['price_usd']-previous_month_revenue)/previous_month_revenue)*100
MOM_change = MOM_change.fillna(0)
Month_wise_revenue_change = pd.DataFrame({'Months':month_Gross_revenue['month'],'MOM_change':MOM_change})
print(Year_wise_Revenue_change)
print('----------------------')
print(Month_wise_revenue_change)


# %%
### How is the Revenue is changing yearly & monthly 

# %%
fig,axes = plt.subplots(2,1,figsize = (8,8))

axes[0].plot(Year_wise_Revenue_change['Years'] , Year_wise_Revenue_change['YOY_change'],marker= 'x')
axes[0].set_xticks(Year_wise_Revenue_change['Years'])
axes[0].set_xlabel('year')
axes[0].set_ylabel('YOY% change')
axes[0].set_title('YOY% Change')

axes[1].plot(Month_wise_revenue_change['Months'],Month_wise_revenue_change['MOM_change'],marker = 'x',color = 'r' )
axes[1].set_xlabel('Months')
axes[1].set_ylabel('MOM% change')
axes[1].set_title('MOM% Change')
plt.tight_layout()
plt.show()

# %%
### from 2012 - 2013 there is a explosive growth 
### form 2013 - 2014 --- there is still growth but it is not like a
### explosive growth which we have seen in last two years 

# %%
#### year 2015 are geting compared with all others year  
orders_compare  = orders[(orders['year'] == 2014 )& (orders['month']>=1) & (orders['month']<=3) | (orders['year'] == 2015) & (orders['month']>=1) & (orders['month']<=3)| (orders['year'] == 2013)&(orders['month']>=1) & (orders['month']<=3)|(orders['year'] == 2012)&(orders['month']>=1) & (orders['month']<=3)]

# %%
orders_compare = orders_compare.groupby('year')['price_usd'].sum().reset_index(name = 'revenue')

# %%
orders_compare['previous_revenue'] = orders_compare['revenue'].shift(1)

# %%
orders_compare['change'] = (orders_compare['revenue'] - orders_compare['previous_revenue'])*100.00 / orders_compare['previous_revenue']

# %%
### How the revenue is channging also taking into consideration the year 2015

# %%
plt.plot(orders_compare['year'],orders_compare['change'],color = 'red',marker = 'o')
plt.xticks(orders_compare['year'])
plt.xlabel('Years')
plt.ylabel('Revenue_Change')
plt.title('Yearly Growth Comparison (Jan–Mar, Including 2015 Partial Data)')
plt.show()

# %%
orders_compare

# %%
#### orders by year for comparision analysis 
### 2015 having partial data of the months 1,2,3 so taken 3 months data for all years for comparision 

# %%
orders_year_month = orders.groupby(['year','month'])['order_id'].count().reset_index(name = 'order_counts')

# %%
fig,axes = plt.subplots(2,2,figsize =(10,5))

order_2012 = orders_year_month[orders_year_month['year'] == 2012]
axes[0,0].plot(order_2012['month'],order_2012['order_counts'],marker = 'o',color = 'red')
axes[0,0].set_title('Orders in Year 2012')

order_2013 = orders_year_month[orders_year_month['year'] == 2013]
axes[0,1].plot(order_2013['month'],order_2013['order_counts'],marker = 'o',color = 'red')
axes[0,1].set_title('Orders in Year 2013')

order_2014 = orders_year_month[orders_year_month['year'] == 2014]
axes[1,0].plot(order_2014['month'],order_2014['order_counts'],marker = 'o',color = 'red')
axes[1,0].set_title('Orders in Year 2014')

order_2015 = orders_year_month[orders_year_month['year'] == 2015]
axes[1,1].plot(order_2015['month'],order_2015['order_counts'],marker = 'o',color = 'red')
axes[1,1].set_xticks(order_2015['month'])
axes[1,1].set_title('Orders in Year 2015')

plt.tight_layout()


# %%
#### Monthly change in orders counts and revenue 

orders_counts_revenue = orders.groupby('month').agg(order_counts =('order_id','count'),revenue = ('price_usd','sum')).reset_index()

fig,axes = plt.subplots(figsize =(10,5))

axes.plot(orders_counts_revenue['month'],orders_counts_revenue['order_counts'],marker = 'o',label = 'order_counts')
axes.legend()
axes.set_xlabel('Order Months')
axes.set_ylabel('Order_counts')

axes1 = axes.twinx()
axes1.plot(orders_counts_revenue['month'],orders_counts_revenue['revenue'],marker = 'o',label = 'order_revenue',color = 'green')
axes1.set_ylabel('Order_revenue')
axes.set_title('Monthly Order counts & Order_Revenue Comparision')
axes1.legend(loc = 'upper right')
plt.show()

# %%
#### Month 6 is a growth take off month this is the month from where the orders traffic is going to increase 
#### There is a seasonal dip in month of march (3)
#### Month 11,12 can be considered as a peak months 
#### Month 4 are having lowest orders and revenue 
#### Month of 12 having highest orders and revenues

# %%
order_item_refunds['created_at'] = pd.to_datetime(order_item_refunds['created_at'])
order_items['created_at'] = pd.to_datetime(order_items['created_at'])

# %%
######## The growth rate is getting decreased in year 2014 compared to 2013 
### the orders,revenue,items_increased is still increasing continuously the reduce is just due to the base effect rather than effect of 
### operational issues the growth rate in 2014 is bit slow comapred to year 2013 

# %%
products['created_at'] = pd.to_datetime(products['created_at'])

# %%
#### Monthly Conversion Rate

# %%
website_sessions['created_at'] = pd.to_datetime(website_sessions['created_at'])

# %%
orders_website_sessions = pd.merge(website_sessions,orders, on = 'website_session_id',how = 'left')

# %%
import numpy as np

# %%
orders_website_sessions['session_months'] = orders_website_sessions['created_at_x'].dt.month
Monthly_Convesion_rate = orders_website_sessions.groupby('session_months')['order_id'].apply(lambda x :x.notna().mean())
orders_session_counts = orders_website_sessions.groupby('session_months')['website_session_id'].count().reset_index(name = 'session_counts')
Monthly_Convesion_rate = Monthly_Convesion_rate.reset_index(name = 'conversion_rate')
fig,axes = plt.subplots(figsize =(10,5))

axes.plot(Monthly_Convesion_rate['session_months'],Monthly_Convesion_rate['conversion_rate'],marker = 'o',color = 'b',label = 'conversion_rate')
axes.set_xlabel('Months')
axes.legend(loc = 'upper right')
axes.set_ylabel('conversion_rate')
plt.title('Monthly_Conversion_Rate & Session Counts')


axes1 = axes.twinx()
axes1.plot(orders_session_counts['session_months'],orders_session_counts['session_counts'],marker = 'o',label = 'session_counts')
axes1.legend()
axes1.set_ylabel('session_counts')
axes1.legend()

plt.show()

# %%
### Month of Feb having the highest conversions 
### In month of 11,12 there highest session counts are there but if we compare with its
### conversion rate are low which means largely the customers are not buying just scrolling
### In month of 4 there is dip in both conversion and session counts

##Month 11–12:more visitors,browsing heavy,lower intent %
##Month 2:fewer visitors,targeted/returning,higher intent %
### Month 2 having higher conversion rate as the repeat customers are also high here 

# %%
##### Waterfall Analysis 
Total_orders = orders['order_id'].count()
Total_Cost = orders['cogs_usd'].sum()
Total_Revenue = orders['price_usd'].sum()
Total_Refunded_Amt = order_item_refunds['refund_amount_usd'].sum()
Refunded_items_Cost = pd.merge(order_items,order_item_refunds,how = 'right',on = 'order_item_id')['cogs_usd'].sum()
Total_Net_Revenue = Total_Revenue - Total_Refunded_Amt
Total_Net_Cost = Total_Cost - Refunded_items_Cost
Profit = Total_Net_Revenue - Total_Net_Cost

# %%
waterfall_analysis = pd.DataFrame({'Step':['Total_Revenue','Total_Cost','Total_Refunded_Amt','Refunded_items_cost','Profit'],'Amount':[Total_Revenue,-Total_Cost,Total_Refunded_Amt,-Refunded_items_Cost,Profit]})

# %%
waterfall_analysis

# %%
waterfall_analysis['Cumulative'] = waterfall_analysis['Amount'].cumsum()

# %%
fig,ax = plt.subplots(figsize =(10,5))
plt.title('Waterfall_Analysis')
colorss = ['green' if x>0  else 'red' for x in waterfall_analysis['Amount']]
ax.bar(waterfall_analysis['Step'],waterfall_analysis['Amount'],color = colorss)
plt.xticks(waterfall_analysis['Step'],rotation = 90)

for i,val in enumerate(waterfall_analysis['Amount']):
    if val>=0 :
        ax.text(i,val,round(val,2),ha = 'center' , va = 'bottom')
    else:
        ax.text(i,val,round(val,2),ha = 'center' , va = 'top')

plt.show()

# %%
### it shows how the money actually flowing in which Total_cost contributes the most but 

# %%
gross_margin = (Total_Revenue - Total_Cost)*100.00/Total_Revenue
gross_margin

# %%
refunded_rate = (Total_Refunded_Amt)*100.00/Total_Revenue
refunded_rate

# %%
profit_margin = (Profit/Total_Revenue)*100.00
profit_margin

# %%
##The business having strong gross margin it is 62% before deducting refunds and other stuff 
##the refund rate is 4.4% which is very low 
##the business selling the products at high margin as its profit margin is about 60%

# %%
#### Revenue Decline Analysis 
order_refundsss = pd.merge(order_items,order_item_refunds,how = 'left' , on = 'order_item_id',suffixes= ('_order_items','_order_refunds'))

# %%
orders_revenue = orders.groupby('month')['price_usd'].sum().reset_index(name = 'revenue')

# %%
orders_revenue['previous_revenue'] = orders_revenue['revenue'].shift(1)

# %%
orders_revenue['revenue_%_change'] =(orders_revenue['revenue'] - orders_revenue['previous_revenue'])*100.00 / orders_revenue['previous_revenue']

# %%
orders_revenue

# %%
plt.plot(orders_revenue['month'],orders_revenue['revenue_%_change'],marker = 'x')
for x,y in zip(orders_revenue['month'],orders_revenue['revenue_%_change']):
    plt.text(x,y,str(round(y,2)))

plt.title('Month-over-Month Revenue % Change')
plt.show()

# %%
### here the revenue decline is seasonal not structural 

# %%
order_item_refunds['created_at'] = pd.to_datetime(order_item_refunds['created_at'])

# %%
order_item_refunds['year'] = order_item_refunds['created_at'].dt.year
order_item_refunds['month'] = order_item_refunds['created_at'].dt.month

# %%
order_item_refunds['month'] = order_item_refunds['created_at'].dt.month

# %%
order_items['created_at'] = pd.to_datetime(order_items['created_at'])
order_items['year'] = order_items['created_at'].dt.year
order_items['month'] = order_items['created_at'].dt.month

# %%
orders_items_order_refund = pd.merge(order_items,order_item_refunds,on = 'order_item_id' ,how = 'left',suffixes= ('_order_items','_order_items_refund'))

# %%
orders_items_order_refund

# %%
##### calculating profitss 
orders_items_order_refund['profit'] = (orders_items_order_refund['price_usd'] - np.where(orders_items_order_refund['order_item_refund_id'].notna() 
 ,orders_items_order_refund['refund_amount_usd'] , 0))-(orders_items_order_refund['cogs_usd'] - np.where(orders_items_order_refund['order_item_refund_id']
                                 .notna(), orders_items_order_refund['cogs_usd'], 0))

# %%
orders_items_order_refund_profit  = orders_items_order_refund.groupby('month_order_items')['profit'].sum().reset_index(name = 'Profit')
orders_items_order_refund_profit['previous_year_profit'] = orders_items_order_refund_profit['Profit'].shift(1)
orders_items_order_refund_profit['profit_prct']= ((orders_items_order_refund_profit['Profit']-orders_items_order_refund_profit['previous_year_profit'])*100.00
                                                  /orders_items_order_refund_profit['previous_year_profit'])

# %%
plt.plot(orders_items_order_refund_profit['month_order_items'],orders_items_order_refund_profit['profit_prct'],color = 'orange',marker = 'o')
plt.title('Month_wise_profit_prct_change%')
plt.show()

# %%
#### considering year 2012,2013,2014 only as 2015 does not having full data 
orders_items_order_refund_year_wise = orders_items_order_refund[orders_items_order_refund['year_order_items'].isin([2012,2013,2014])]

orders_items_order_refund_profit_year  = orders_items_order_refund_year_wise.groupby('year_order_items')['profit'].sum().reset_index(name = 'Profit')
orders_items_order_refund_profit_year['previous_year_profit'] = orders_items_order_refund_profit_year['Profit'].shift(1)
orders_items_order_refund_profit_year['profit_prct']= ((orders_items_order_refund_profit_year['Profit']-orders_items_order_refund_profit_year['previous_year_profit'])*100.00/orders_items_order_refund_profit_year['previous_year_profit'])

# %%
orders_items_order_refund_profit_year

# %%
#### year wise profit growth 
###  year wise profit growth change so like it is going down the reason behind it that the growth is slow down compare in 
### 2013 to year 2014 the profit has been increased by +180% from the last year but in case of growth it has been decreased 
### The growth is slow

fig,axes = plt.subplots(figsize = (10,5))

line1, = axes.plot(orders_items_order_refund_profit_year['year_order_items'],orders_items_order_refund_profit_year['profit_prct'],color = 'orange',marker = 'o'
         ,label = 'Profit% change')
axes.set_title('Year_wise_profit_prct_change%')
axes.set_xticks(orders_items_order_refund_profit_year['year_order_items'])
axes.set_xlabel('Years')
axes.set_ylabel('Profit_prct')

axes_1  = axes.twinx()
line2, = axes_1.plot(orders_items_order_refund_profit_year['year_order_items'],orders_items_order_refund_profit_year['Profit'],color = 'red',marker = 'o'
                    ,label = 'Profit')
###axes_1.set_title('Year_wise_profit')
###axes_1.set_xticks(orders_items_order_refund_profit_year['year_order_items'])
axes_1.set_ylabel('Profit')

lines = [line1,line2]
labels = [line.get_label() for line in lines]

axes.legend(lines,labels,loc = 'upper left')

plt.show()


# %%

profit_margin = orders_items_order_refund_year_wise.groupby('year_order_items')[['price_usd','profit']].sum().reset_index()

# %%
profit_margin['profit_margins'] = (profit_margin['profit']/profit_margin['price_usd'])*100.0

# %%
profit_margin

# %%
### why the growth rate of profit is slow reason behind it 
#Revenue and profit continued to grow strongly in 2014, with improving profit margins. 
#The decline in year-over-year growth rate appears to be primarily due to the base effect 
##rather than operational inefficiencies.

# %%
###There is a very low correlation (0.012) between price and order volume, 
### indicates that price is not the driver force for the purchase of customer
### there are other factors which can influence the purchase beahviour of customer 

# %%
orders_corr = orders.groupby('user_id').agg(Total_orders = ('order_id','count'),Price = ('price_usd','mean')).corr()
import seaborn as sns
sns.heatmap(orders_corr,annot = True)
plt.title('Correlation btw price & orders')

# %%
orders_order_items = orders.groupby('user_id').agg(no_items_purchased = ('items_purchased','mean'),Price = ('price_usd','mean')).corr()
sns.heatmap(orders_order_items,annot = True)
plt.title('Correlation btw items purchased & revenue')
plt.show()

# %%
#### Correlation btw items purchased & revenue is very strong about 0.92 as corr 
### that means our overall business is driven by volume not by the price as price is not influencing it much  

# %%
import seaborn as sns

# %%

price_analysis_corr = orders.groupby('user_id').agg(order_counts = ('order_id','count'),price = ('price_usd','sum')).corr()
plt.title('Correlation between order_counts & Price_usd')
sns.heatmap(price_analysis_corr,annot = True)
plt.show()

# %%
#### Segmentizing cutomer as One-Time Customer , Repeat Customer & New Customer
### customer who have ordered one time they are one_time_cust 
### customer who have ordered multiple time they are repeat_cust
### customer who have ordered in its customer_lifetime<=30 then 'new_cust' 

customer_life_time = orders.groupby('user_id')['created_at'].max() - orders.groupby('user_id')['created_at'].min()

# %%
customers_data = orders.groupby('user_id').agg(Total_Orders = ('order_id','count'),first_order_date = ('created_at','min'),last_order_date = ('created_at','max')).reset_index()

# %%
customers_data['cust_life_time_days'] = (customers_data['last_order_date'] - customers_data['first_order_date']).dt.days

# %%
customers_data['order_type'] = customers_data['Total_Orders'].apply(lambda x:'One_Time_Customer' if x ==1 else 'Repeat_Customer')

# %%
customers_data['cust_type'] = customers_data['cust_life_time_days'].apply(lambda x:'New_Customer' if x <=30 else 'Old_Customer')

# %%
customers_data

# %%
cust_type_seg = customers_data.groupby('cust_type')['user_id'].count().reset_index()
cust_type_seg

# %%
order_type_seg = customers_data.groupby('order_type')['user_id'].count().reset_index()
order_type_seg

# %%
plt.title('Customer_Type_Distributions')
plt.pie(cust_type_seg['user_id'] ,labels = cust_type_seg['cust_type'],autopct = '%1.1f%%')
plt.show()

# %%
plt.title('Order_Type_Distributions')
plt.pie(order_type_seg['user_id'] ,labels = order_type_seg['order_type'],autopct = '%1.1f%%')
plt.show()

# %%
#### the business largely running due to one time customer which means that business not able to gain customer loyalty
###  Customer Acquistion is strong but in order to retain those customer it is very low 

# %%
month_wise_cust_seg = pd.merge(orders,customers_data,on = 'user_id',how = 'left')

# %%
#### Customer_Type by order_type dist
Monthly_order_type = month_wise_cust_seg.groupby(['month','order_type'])['order_type'].count().reset_index(name = 'user_counts')
Monthly_order_type

# %%
monthly_order_pivot = Monthly_order_type.pivot(columns  = 'order_type' , index = 'month' , values = 'user_counts')

# %%
monthly_order_pivot.plot(marker='o')
plt.title('Monthly Order Type Distributions')
plt.xlabel('Months')
plt.ylabel('User_counts')
plt.show()

# %%
### New customers & One time customer are high in month dec there is accquring of new customer in that month
### repeat customer are high in month of feb that's why the conversion rate is also high in that month

# %%
#### Customer_Type by order_type dist
Monthly_cust_type = month_wise_cust_seg.groupby(['month','cust_type'])['cust_type'].count().reset_index(name = 'user_counts')
Monthly_cust_type

# %%
monthly_cust_pivot = Monthly_cust_type.pivot(columns  = 'cust_type' , index = 'month' , values = 'user_counts')
monthly_cust_pivot

# %%
monthly_cust_pivot.plot(marker='o')
plt.title('Monthly Order Type Distributions')
plt.xlabel('Months')
plt.ylabel('User_counts')
plt.show()

# %%
max_order_date = orders['created_at'].dt.normalize().max()
customers_data['last_order_date_'] = customers_data['last_order_date'].dt.normalize()

# %%
customers_data['days_after_last_purchase'] = (max_order_date - customers_data['last_order_date_']).dt.days

# %%
customers_data[customers_data['order_type']=='One_Time_Customer']['cust_life_time_days'].mean()

# %%
customers_data[customers_data['order_type']=='Repeat_Customer']['cust_life_time_days'].mean()

# %%
##Repeat customers typically make subsequent purchases within about 35 days of their first purchase,
##indicating a roughly one-month repeat 
##cycle. In contrast, one-time customers show zero lifetime span because they do not return for additional purchases.
## the repeat cycle is about of 35 days (business can give reminders after 28-30 days) in order to increase repeat rate 
### the most likely the customer who made puchase in month of jan are returning in feb to make puchases 
### that's why the return customers and conversion rate is high in that month

# %%
##The business shows a repeat purchase cycle of about 35 days. 
##Customers who purchase in one month, particularly January, are likely to return in the following month
##(February), leading to higher repeat share and conversion rates. Repeat activity is
##especially concentrated in months such as Jan, Feb, Sep, Nov, and Dec, indicating seasonal
##retention peaks aligned with the ~30-day repeat window.

# %%
customers_data['cust_lifetime_score'] = customers_data['cust_life_time_days'].apply(lambda x:0 if ((x>=0) & (x<=30)) else 40 if ((x>30) & (x<=60)) else
                                            60 if ((x>60) & (x<=90)) else 100 if x>90 else None)

customers_data['cust_lifetime_score'] = customers_data['cust_lifetime_score'].astype('int')

customers_data['days_after_last_purchase_score'] =  customers_data['days_after_last_purchase'].apply(lambda x:80 if ((x>=0) & (x<=365)) else 20 if ((x>=366) & (x<=730)) else
                                            0 if x>=731 else None )

customers_data['days_after_last_purchase_score'] = customers_data['days_after_last_purchase_score'].astype('int')

customers_data['customer_lifetime_&_last_purchase_score'] = customers_data['cust_lifetime_score'] + customers_data['days_after_last_purchase_score']
customers_data['customer_lifetime_&_last_purchase_score'] = customers_data['customer_lifetime_&_last_purchase_score'].astype('int')

customers_data['cust_retention_type'] = customers_data['customer_lifetime_&_last_purchase_score'].apply(lambda x:'Risk' if x<=40 else 'Active' if ((x>40) & (x<=80)) else 'Best' )

# %%
customers_data['cust_retention_type'].unique()

# %%
cust_retention_type = customers_data.groupby('cust_retention_type')['user_id'].count().reset_index(name = 'user_counts')

# %%
cust_retention_type

# %%
cust_retention_type['cust_retention_prcnt'] = (cust_retention_type['user_counts'])*100.00/cust_retention_type['user_counts'].sum()

# %%
plt.title('Customer Retention Analysis')
bars= plt.bar(cust_retention_type['cust_retention_type'],cust_retention_type['user_counts'])
for i,val in enumerate(bars):
    height = val.get_height()
    plt.text(i,height+0.5,str(height))
plt.show()

# %%
##customer churn and retention analysis 
##Consider loyalty and recency taken the max portion of customer_lifetime max is 100 and then the second priority given to 
##recency max of 80 
##so the range is like best customer has to be around 180 (customer is old as well as recently purchased)
## the range btw 40 to 80 has to be active  (customer is old and purchase recently )
##less than 40 then it is risky( the customer is recent and not purchased recently )

# %%
### The customer is classified into 3 Active,Best & at Risk 
### The customer largely active about 60%
### The 40% of customer are risk who just left the business a long on 
### All this indicates one thing that customer are purchasing one_time largely and then they just left the business 
### The Business is very dependent on the paid traffic which is not good for the long_term & they are larlely depending 
### on constant aqusition of customer instead they very importantely need to take measure steps in order to retain customer 

# %%
orders['Order_Time_Bin'] = orders['created_at'].dt.hour.apply(lambda x:'Early_Morning' if ((x>=0) & (x<=5)) else 'Morning' if ((x>=6) & (x<=11)) else 
                           'Afternoon' if ((x>=12) & (x<=16)) else 'Evening' if ((x>=17) & (x<=20)) else 'Night')

# %%
orders['Day_Bin']  = orders['created_at'].dt.day_name().apply(lambda x:'Weekend' if x == 'Saturday' else 'Weekend' if x == 'Sunday' else 'Weekdays')

# %%
Order_time_dist = orders.groupby('Order_Time_Bin')['order_id'].count().reset_index(name = 'Total_Orders')

# %%
Order_time_dist

# %%
### Number of orders by Order Time Bin
plt.title('Total Orders Distribution by Time Buckets')
plt.bar(Order_time_dist['Order_Time_Bin'] , Order_time_dist['Total_Orders'])
plt.xlabel('Time_Slots')
plt.ylabel('Total_Orders')
plt.show()

# %%
### Number of orders are largely being order in Afternoon and then in Morning 
### and least at night as well the customer 

# %%
website_sessions['Time_Slots'] = website_sessions['created_at'].dt.hour.apply(lambda x:'Early_Morning' if ((x>=0) & (x<=5)) else 'Morning' if ((x>=6) & (x<=11)) else 
                           'Afternoon' if ((x>=12) & (x<=16)) else 'Evening' if ((x>=17) & (x<=20)) else 'Night')

# %%
website_session_orders_time = pd.merge(website_sessions,orders,on = 'website_session_id',how = 'left',suffixes=  ('_website','_orders'))

# %%
Website_Time_wise_Conversion_rate = (website_session_orders_time.groupby('Time_Slots')['order_id'].apply(lambda x:x.notna().sum())/website_session_orders_time.groupby('Time_Slots')['website_session_id'].nunique()).reset_index(name = 'Time_wise_conversion_rate')

# %%
Website_Time_wise_Conversion_rate

# %%
### Number of orders by Order Time Bin
plt.title('Time Wise Conversion Rate')
plt.bar(Website_Time_wise_Conversion_rate['Time_Slots'] , Website_Time_wise_Conversion_rate['Time_wise_conversion_rate'])
plt.xlabel('Time_Slots')
plt.ylabel('Time_wise_conversion_rate')
plt.show()

# %%
#### Although the Traffic is high in afternoon as well as most order are lie in afternoon but in case of conversion
### rate by sessions is stable which means there is no dramatic demand is time concantrated not urgency driven
### Buying intent is same accross day 
### The buying intent is same it is just that the traffic is high on website in afternoon that why the orders are sold more in that time frame
### We can run campians in that time frame to attract more traffic 
#### intent-neutral traffic growth

# %%
website_sessions.groupby('Time_Slots')['website_session_id'].count().reset_index(name = 'session_counts')

# %%
days_bin_dist = orders.groupby('Day_Bin')['order_id'].count().reset_index(name = 'Total_Orders')

# %%
days_bin_dist

# %%
plt.title('Total_Orders_Distributions By Day Bin')
plt.pie(days_bin_dist['Total_Orders'],labels = days_bin_dist['Day_Bin'],autopct = '%1.1f%%')
plt.show()

# %%
### Number of orders on Weekdays are high compare to Weekend

# %%
orders['Order_Hour'] = orders['created_at'].dt.hour

# %%
order_Hour = orders.groupby('Order_Hour')['order_id'].count().reset_index(name = 'No_of_orders')

# %%
plt.title('No of Orders by hour')
plt.plot(order_Hour['Order_Hour'],order_Hour['No_of_orders'],marker = 'o',color = 'yellow')
plt.show()

# %%
### Peak hour of order is 11 and 12

# %%
orders['Order_Day_Name'] = orders['created_at'].dt.day_name()

# %%
orders_by_day_name = orders.groupby('Order_Day_Name')['order_id'].count().reset_index(name = 'order_counts')

# %%
plt.bar(orders_by_day_name['Order_Day_Name'],orders_by_day_name['order_counts'])
plt.xticks(orders_by_day_name['Order_Day_Name'],rotation = 90)
plt.title('No of Orders by Day_Name')
plt.show()

# %%

### Least orders on Saturday and highest on Monday

# %%
##### RFM analysis 
orders_order_item_refunds = pd.merge(orders,order_item_refunds,on = 'order_id',how = 'left',suffixes= ('_orders','order_item_refunds'))

# %%
orders_order_item_refunds['created_at_orders'].max()

# %%

orders_order_item_refunds['net_revenue'] = ((orders_order_item_refunds['price_usd']) - (np.where(orders_order_item_refunds['refund_amount_usd'].notna(),orders_order_item_refunds['refund_amount_usd'],0)))
max_order = orders_order_item_refunds['created_at_orders'].max()

rfm_analysis = orders_order_item_refunds.groupby('user_id').agg(Recency = ('created_at_orders'
                                                                           ,lambda x :(max_order -x.max()).days),Frequency = ('order_id','nunique'),Monetary = ('net_revenue','sum'))
rfm_analysis.reset_index(inplace = True)
rfm_analysis['Recency_Score'] = pd.qcut(rfm_analysis['Recency'],3,labels= [3,2,1])
rfm_analysis['Monetary_Score'] = pd.qcut(rfm_analysis['Monetary'],3,labels= [1,2,3])
rfm_analysis['Frequency_Score'] = pd.qcut(rfm_analysis['Frequency'].rank(method='first'),3,labels= [1,2,3])
rfm_analysis['Recency_Score'] = rfm_analysis['Recency_Score'].astype('int')
rfm_analysis['Monetary_Score'] = rfm_analysis['Monetary_Score'].astype('int')
rfm_analysis['Frequency_Score'] = rfm_analysis['Frequency_Score'].astype('int')
rfm_analysis['RFM_Score'] = rfm_analysis['Recency_Score']+rfm_analysis['Monetary_Score']+rfm_analysis['Frequency_Score']
rfm_analysis['RFM_Score'] = rfm_analysis['RFM_Score'].astype('int')
rfm_analysis['RFM_Segments'] = np.where(
rfm_analysis['RFM_Score'] >= 7,
    'High_Value_Cust',
    np.where(
        (rfm_analysis['RFM_Score']>=4) & (rfm_analysis['RFM_Score']<=6)   ,
        'Medium_Value_Cust',
        'Low_Value_Cust'
    )
)

# %%
rfm_segments = rfm_analysis.groupby('RFM_Segments')['user_id'].count().reset_index(name = 'user_counts')

# %%
rfm_segments

# %%
plt.title('Customer Distributions besed on RFM Scoring')
plt.pie(rfm_segments['user_counts'],labels = rfm_segments['RFM_Segments'],autopct = '%1.1f%%')
plt.show()

# %%
(rfm_analysis[rfm_analysis['RFM_Segments'] == 'High_Value_Cust'].agg({'Recency':'sum','Monetary':'sum',
                                                                  'Frequency':'sum'}))*100.00/ rfm_analysis.agg({'Recency':'sum',
                                                                                                         'Monetary':'sum','Frequency':'sum'})

# %%
(rfm_analysis[rfm_analysis['RFM_Segments'] == 'Medium_Value_Cust'].agg({'Recency':'sum','Monetary':'sum',
                                                                  'Frequency':'sum'}))*100.00/ rfm_analysis.agg({'Recency':'sum',
                                                                                                         'Monetary':'sum','Frequency':'sum'})

# %%
(rfm_analysis[rfm_analysis['RFM_Segments'] == 'Low_Value_Cust'].agg({'Recency':'sum','Monetary':'sum',
                                                                  'Frequency':'sum'}))*100.00/ rfm_analysis.agg({'Recency':'sum',
                                                                                                         'Monetary':'sum','Frequency':'sum'})

# %%
### The customer are being distributed into high,medium,low cust 
### The most customer are of High which is very good for business 
### In deep drive of these analysis the Low value customer are inavtive and low_value cust and in case of medium customer the 
### customer are active but they also low_value cust as in case of monetary and frequency are quite same not having much changes 
### so, the medium cust we can call them active_low_value_cust 
### so, the low value cust we can call them inactive_low_value_cust 

### the propotion of both low_value + medium value cust contributes around = more than 60% of total which only depicts the business need to take 
### step so that the monetary and frequency will get increase 

### the medium value cust contributes around 28.2% which means customer are active and engaging but not scaling up with the volume of orders 
### we can target them and try to increase them

### our main challenge is value expansion not the customer aquistions 

# %%
website_sessions['year'] = website_sessions['created_at'].dt.year
website_sessions['month'] = website_sessions['created_at'].dt.month

# %%
website_summary = website_sessions.groupby(['month','device_type'])['user_id'].count().reset_index(name = 'user_counts')

# %%
website_summary_pivot = website_summary.pivot(columns = 'device_type',index ='month',values = 'user_counts').reset_index()

# %%
desktop_users_prct = website_summary_pivot['desktop'].sum()/ (website_summary_pivot['desktop'] +website_summary_pivot['mobile']).sum()

# %%
mobile_users_prct = website_summary_pivot['mobile'].sum()/ (website_summary_pivot['desktop'] +website_summary_pivot['mobile']).sum()

# %%
plt.pie([desktop_users_prct,mobile_users_prct],labels =['Desktop_users','Mobile_users'],autopct = '%1.1f%%')
plt.title('Users Distributions based on Device_Type')
plt.show()

# %%
fig,axes = plt.subplots(figsize =(10,5))

line1, = axes.plot(website_summary_pivot['month'],website_summary_pivot['desktop'],color = 'green' , marker ='o',label = 'desktop')
axes.set_title('Users_Traffic By Device Type')


axes_1 = axes.twinx()
line2, = axes_1.plot(website_summary_pivot['month'],website_summary_pivot['mobile'],color = 'red',marker = 'o',label = 'mobile')

axes.legend(handles = [line1,line2],loc ='upper left')
plt.show()

# %%
website_sessino_orders_device = pd.merge(orders,website_sessions,on= 'website_session_id',how = 'left',suffixes= ('_orders','_website_sessions'))

# %%
website_sessino_orders_device.groupby('device_type')['order_id'].count()

# %%
website_avg_price = website_sessino_orders_device.groupby('device_type')['price_usd'].mean().reset_index(name = 'avg_price_usd')

plt.scatter(website_avg_price['device_type'],website_avg_price['avg_price_usd'])

for i ,row in website_avg_price.iterrows():
    plt.text(row['device_type'],row['avg_price_usd'],str(round(row['avg_price_usd'])))

# %%
website_sessino_orders_device.groupby('device_type')['order_id'].count()/website_sessino_orders_device['order_id'].count()

# %%
website_session_revenue_device = ((website_sessino_orders_device.groupby('device_type')['price_usd'].sum())*100.00/website_sessino_orders_device['price_usd'].sum()).reset_index(name = 'revenue')

# %%
website_session_revenue_device

# %%
plt.pie(website_session_revenue_device['revenue'],labels = website_session_revenue_device['device_type'],autopct = '%1.1f%%')
plt.title('Revenue Distribution by Device Type')
plt.show()

# %%
#### The sessions are being largely dominated by Desktop users compared to mobile users 
#### The orders from desktop is high as compare to mobile users 
#### 85% of revenue is contributed by desktop alone and remaning with mobile 
#### Avg order value in mobile is slighly high then desktop

# %%
orders_products = pd.merge(order_items,products,on = 'product_id',how = 'left',suffixes= ('_orders','_products'))

# %%

products_summary = orders_products.groupby('product_name').agg(Order_counts = ('order_id','count'),launch_date = ('created_at_products','min'),
                                            last_order_date = ('created_at_orders','max'),Total_revenue = ('price_usd','sum'),
                                           ).reset_index()

# %%
products_summary['products_age'] = (products_summary['last_order_date'] - products_summary['launch_date']).dt.days

# %%
products_summary

# %%
products_launch =  products_summary
products_launch['launch_datee'] = pd.to_datetime(products_launch['launch_date'],format = '%Y-%m').dt.normalize()
products_launch

# %%
plt.scatter(products_launch['product_name'] , products_launch['launch_datee'])
plt.xticks(products_launch['product_name'] ,rotation = 90)
plt.title('Products Launch TimeLine')
plt.xlabel('Product_Name')
plt.ylabel('Launch_Timeline')
plt.show()

# %%
##### which products is launched when the products the orignal mr fuzzy launched first and last product which is 
#### launched is The Hudson River Mini bear

# %%
products_summary['products_order_day'] = products_summary['Order_counts']/products_summary['products_age']

# %%
products_summary['products_revenue_day']  = products_summary['Total_revenue']/products_summary['products_age']

# %%
products_summary = products_summary.sort_values(by= 'launch_date')

# %%
products_summary['relative_growth_%'] = ((products_summary['products_revenue_day'])*100.00/products_summary['products_revenue_day'].max())

# %%
products_summary

# %%
plt.hlines(products_summary['product_name'],xmin = 0,xmax = products_summary['relative_growth_%'])
plt.plot(products_summary['relative_growth_%'],products_summary['product_name'],"o")
plt.xlabel('Relative_Growth_%')
plt.ylabel('Product_Name')
plt.title('Product Productivity Comparison')
plt.show()

# %%
### Products productivity which product is given the most growth across various products 

# %%
#### The Product The Original Mr.Fuzzy is capturing the most in orders as well as revenue per day 
#### The Product (The Birthday Sugar Panda) having a moderate growth but still the Mr.Fuzzy is at peak 
#### The Product which have launched recently is not doing well as the product age is similar for product The Birthday Sugar Panda
#### & The Hudson River Mini bear but still the product The Birthday Sugar Panda has contributed around 45% in relative growth 
#### whereas The Hudson River Mini bear only contributes around 33%
#### This The Hudson River Mini bear is the product which is sold the second most likely to be cross sell products rather than the primary

#### Most sales are driven by Mr.Fuzzy which is risky for the business which can create vulnerability for the business if the demand of this 
#### product decrease then it is going to affect the business negatively.

#### Forever love bear 

# %%
orders[orders['items_purchased'] == 1].groupby('primary_product_id')['price_usd'].min()

# %%
combo_products = pd.merge(order_items,products,on = 'product_id',suffixes= ('_orders','_products'))

# %%
### 1 is the primary item and secondary = 0
combo_products['Puchase_Type'] = combo_products['is_primary_item'].apply(lambda x:'First_Product_Purchased' if x == 1 else 'Second_Product_Purchased')

# %%
combo_productss = combo_products.groupby(['product_name','Puchase_Type'])['order_item_id'].count().reset_index(name = 'order_item_counts')

# %%

combo_products_pivot = combo_productss.pivot(columns = 'product_name',index = 'Puchase_Type',values = 'order_item_counts')
combo_products_pivot

# %%
combo_products_pivot.T.plot(kind = 'bar')
plt.title('First vs Second Purchase by Product')
plt.ylabel('Order_item_Counts')
plt.show()

# %%
#### cross_sell = which product most likely to second purchase and which one is first purchased 
#### This will show which products is being sold as cross sell and which one is sold as a single product
#### The product orignal mr.fuzzy has been contributed most in terms of first purchase 
### The product which have last launched (the hudson river mini bear) most favourable to be a cross product 


#### The business has a high chances to upsell the product (the hudson river mini bear) as it is most likely to be purchased as secondary 
### products

# %%
combo_products

# %%
#### what can be the reason behind customer gone for second product is it due to some drivers????
combo_products.groupby('Puchase_Type')['price_usd'].describe()

### here first product purchased having standard deviation is very less as most of the purchases are of product orignal fuzzy 
### for second product purchased there is so much deviation in prices which is due to products mixed range 

# %%
combo_products.boxplot(column = 'price_usd',by = 'Puchase_Type')
plt.title('Purchase type variation based on price_usd')
plt.ylabel('price_usd')
plt.show()
### The boxplot shows that first-purchase products have a concentrated price around $50, indicating a dominant
### primary product tier. In contrast, second-purchase products fall within a lower price range of 
###approximately $30–46. This confirms that customers tend to add lower-priced items as secondary purchases.
###The Hudson River Mini Bear, being among the lowest-priced products, naturally fits this add-on behavior and is 
### therefore more frequently purchased as a cross-sell item.

# %%
order_products = pd.merge(order_items,products,left_on = 'product_id',right_on = 'product_id',suffixes= ('_orders','_products'))
order_products

# %%
order_items_order = pd.merge(order_items,orders , on = 'order_id',how = 'left',suffixes=('_order_items','_orders'))
order_items_order = pd.merge(order_items_order,products,left_on = 'product_id',right_on = 'product_id',suffixes= ('_orders','_products'))

# %%

order_items_order['orders_type'] = order_items_order['is_primary_item'].apply(lambda x:'First_Purchase_Products' if x == 1 else 'Secondary_Purchase_Product')

# %%
order_items_order = order_items_order.sort_values(by = 'created_at_orders')

# %%
order_itemss = order_items_order.groupby(['user_id','orders_type','product_name'])['price_usd_order_items'].sum().reset_index(name = 'revenue')

# %%
first_purchase_product = order_itemss[order_itemss['orders_type'] == 'First_Purchase_Products']
second_purchase_product = order_itemss[order_itemss['orders_type'] == 'Secondary_Purchase_Product']
first_second = pd.merge(first_purchase_product,second_purchase_product,on = 'user_id',how = 'left',suffixes= ('_first_purchase','_second_purchase')).fillna(0)

# %%
first_second['sell_type'] = np.where(first_second['revenue_first_purchase']<first_second['revenue_second_purchase'] ,'Up_sell' , 'No_upsell')

# %%
first_second.groupby(['sell_type'])['user_id'].nunique()

# %%
order_itemss = order_items_order.groupby(['user_id','orders_type'])['price_usd_order_items'].sum().reset_index(name = 'revenue')

# %%
order_items_pivot = order_itemss.pivot_table(index = 'user_id',columns = 'orders_type',values = 'revenue')

# %%
order_items_pivot['upsell_or_not']  = np.where(order_items_pivot['First_Purchase_Products']<order_items_pivot['Secondary_Purchase_Product'],'up_sell','no_upsell')

# %%
order_items_pivot = order_items_pivot.reset_index()

# %%
order_items_pivot_products = pd.merge(order_items_pivot,order_items_order,on = 'user_id',how = 'left')

# %%
upsell_rate =order_items_pivot_products.groupby(['upsell_or_not','product_name'])['user_id'].count().unstack(fill_value = 0)

# %%
upsell_rate.loc['upsell_rate_%'] = upsell_rate.loc['up_sell'] / (upsell_rate.loc['no_upsell'] + upsell_rate.loc['up_sell'])

# %%
upsell_rate

# %%
upsell_rate_dist = upsell_rate.loc[['no_upsell','up_sell']]

# %%
upsell_ratess = upsell_rate.loc['upsell_rate_%']
upsell_ratess = upsell_ratess.reset_index(name = 'Upsell_Rates')
plt.pie(upsell_ratess['Upsell_Rates'],labels = upsell_ratess['product_name'],autopct = '%1.1f%%',textprops={'rotation': 0})
plt.title('Distributions of Products Based on Upsell_Rates')
plt.show()

# %%
### The upsell rates of product the forever love bear is the most 

# %%
upsell_rate_dist.T.plot(kind = 'barh')
plt.title('Upsell vs No-Upsell Users by First Product')
plt.xlabel('user_id_counts')
plt.ylabel('products_name')
plt.show()

# %%
order_items_pivot = order_items_pivot.reset_index().groupby('upsell_or_not')['user_id'].count().reset_index(name = 'user_counts')
order_items_pivot

# %%
plt.pie(order_items_pivot['user_counts'],labels = order_items_pivot['upsell_or_not'],autopct = '%1.1f%%')
plt.title('Distribution of Users: Upsell vs No Upsell')
plt.show()

# %%
### Python analysis measures upsell at the customer level — whether the customer
### spends more in the second purchase phase compared to the first purchase phase overall.

# %%
### Conversion Funnel Analysis

# %%
website_sessions.head()

# %%
website_orders = pd.merge(website_sessions,orders,on = 'website_session_id',how = 'left',suffixes=('_website','orders'))


# %%
website_orders_pageview = pd.merge(website_orders,website_pageviews,on = 'website_session_id',how='left')

# %%
website_orders_pageview

# %%
no_of_order_per_page = website_orders_pageview.groupby('pageview_url')['order_id'].apply(lambda x: x.notna().sum())
no_of_sessions_per_page = website_orders_pageview.groupby('pageview_url')['website_session_id'].nunique()
conversion_rate = no_of_order_per_page*100.00/no_of_sessions_per_page

# %%
conversion_rate = conversion_rate.reset_index(name = 'conversion_rate')

# %%
conversion_rate

# %%
plt.bar(conversion_rate['pageview_url'],conversion_rate['conversion_rate'])
plt.xticks(conversion_rate['pageview_url'],rotation = 90)
plt.title('Conversion_Rate Baesd on Page_Level')
plt.show()

# %%
#### Entry Page Popularity Distribution
website_orders_pageview.groupby('pageview_url')['user_id_website'].count().sort_values(ascending = False)

# %%
website_orders_pageview.info()

# %%
website_orders_pageview = website_orders_pageview.sort_values(['website_session_id','created_at_website'])
website_orders_pageview['page_sequence'] = website_orders_pageview.groupby('website_session_id').cumcount()+1
website_pageview_ss = website_orders_pageview.groupby(['page_sequence','pageview_url'])['user_id_website'].count().reset_index(name = 'user_traffic')

# %%
website_pageview_ss['previous_user_traffic'] = website_pageview_ss['user_traffic'].shift(1)

# %%
website_pageview_ss['user_traffic_change'] = (website_pageview_ss['user_traffic']-website_pageview_ss['previous_user_traffic'])*100.00/website_pageview_ss['previous_user_traffic']

# %%
plt.title('Entry Page Popularity Distribution')
plt.plot(website_pageview_ss['pageview_url'],website_pageview_ss['user_traffic_change'])
plt.xticks(website_pageview_ss['pageview_url'],rotation = 90)
plt.show()

# %%
website_pageview_ss

# %%
website_pageview_ss['Pages_Classified'] = np.where(website_pageview_ss['pageview_url'].isin(['/home','/lander-1','/lander-2','/lander-3','/lander-4','/lander-5']),'Landing_Page',
         np.where(website_pageview_ss['pageview_url'].isin(['/products','/the-birthday-sugar-panda','/the-forever-love-bear','/the-hudson-river-mini-bear','/the-original-mr-fuzzy']),'Product_Page',
                  np.where(website_pageview_ss['pageview_url']=='/cart' , 'Cart_Page',np.where(website_pageview_ss['pageview_url']=='/shipping','Shipping_Page',
                                                                                               np.where(website_pageview_ss['pageview_url'].isin(['/billing','/billing-2']),'Billing_Page',
                                                                                              np.where(website_pageview_ss['pageview_url']=='/thank-you-for-your-order','Thankyou_Page','Other_Page'))))))

# %%
funnel_traffic = website_pageview_ss.groupby('Pages_Classified')['user_traffic'].sum()
funnel_order = ['Landing_Page','Product_Page','Cart_Page','Shipping_Page','Billing_Page','Thankyou_Page']
funnel_traffic = funnel_traffic.reindex(funnel_order)
funnel_traffic = (funnel_traffic.pct_change()*100).reset_index(name = 'pct_change')
funnel_traffic

# %%
plt.plot(funnel_traffic['Pages_Classified'],funnel_traffic['pct_change'],marker = 'o',color = 'red')
plt.title('Traffic_pct_change by Page_Type')
plt.show()

# %%
### “The funnel analysis shows that the largest user drop occurs at the cart page (~80%)
###, indicating significant cart abandonment. Product pages have minimal drop, suggesting
###high engagement with products. Drop-offs during shipping and billing are moderate, while the
###final step to conversion still loses ~38% of remaining users. Optimizing the cart experience could
###substantially increase conversions.”

# %%
### page drop analysis 

# %%
page_wise_traffic = website_orders_pageview.groupby('page_sequence')['user_id_website'].nunique().reset_index(name = 'users_traffic')

# %%
page_wise_traffic['previous_page_traffic'] = page_wise_traffic['users_traffic'].shift(1)

# %%

page_wise_traffic['prcnt_traffic_drop'] = (page_wise_traffic['users_traffic']-page_wise_traffic['previous_page_traffic'])*100.00/page_wise_traffic['previous_page_traffic']

# %%
page_wise_traffic

# %%
plt.plot(page_wise_traffic['page_sequence'],page_wise_traffic['prcnt_traffic_drop'])
plt.title('Page_Wise Traffic Drop')
plt.show()

# %%
np.where(website_orders['order_id'].notna(),1,0).sum()

# %%
website_orders['website_session_id'].count()

# %%
##### Time To Conversion Analysis 

last_date_user_website_sessions = website_sessions.groupby('user_id')['created_at'].max().reset_index(name = 'last_website_session_date')
last_date_user_order_date = orders.groupby('user_id')['created_at'].max().reset_index(name = 'last_order_date')

# %%
time_conversion = pd.merge(last_date_user_website_sessions,last_date_user_order_date,on = 'user_id',how = 'left')

# %%
time_conversion['days_btw_session_order'] = (time_conversion['last_website_session_date'] - time_conversion['last_order_date']).dt.days.fillna(99999).astype(int)

# %%
time_conversion['Converted_Type'] = time_conversion['days_btw_session_order'].apply(lambda x:'Fast_Converted' if x<10 else 
                                                'Moderate_Converted' if x<=30 else 'Slow_Converted' if (x>30) & (x<99999) else 'Non_Converted')

# %%
converted_type_user_counts = time_conversion.groupby('Converted_Type')['user_id'].count().reset_index(name = 'User_counts')

# %%
converted_type_user_counts['Converted_user_prct'] = (converted_type_user_counts['User_counts'])*100.00/converted_type_user_counts['User_counts'].sum()

# %%
plt.bar(converted_type_user_counts['Converted_Type'] , converted_type_user_counts['User_counts'])
plt.xticks(converted_type_user_counts['Converted_Type'],rotation = 90)
plt.show()

# %%
#### There are 91% who haven't been converted also 
#### Fast Converted the user which just converted in less than 10 days 
####Then low converted contributes to 0.6% 
#### at last moderate converters 0.4 

#### Most of user on the website are non_converted 
#### we can give some vouchers to these fast converters 
#### we can say user are actualy hesitating before buying maybe the business not able gain loyalty.
#### Moderate conerters are about 0.4%  

# %%
#### Biggest oppurtunity to gain this 91% of Non_Converted user by free first purchase,abandoned cart emails,remarketing .
#### for fast coverters we can do upsell,lowalty rewards 
#### for moderated converters reminders,limited offers

# %%
converted_type_user_counts

# %%
plt.figure(figsize = (11,5))
plt.title('Distribution of User Converted Type')
plt.pie(converted_type_user_counts['Converted_user_prct'],labels = converted_type_user_counts['Converted_Type'],autopct = '%1.1f%%')
plt.show()

# %%
conditions = [(website_sessions['utm_source'].isin(['gsearch','bsearch'])),
(website_sessions['utm_source']=='socialbook'),
((website_sessions['utm_source']== 'not applicable') & (website_sessions['http_referer'].str.contains('gsearch',na = False))),
((website_sessions['utm_source']== 'not applicable') & (website_sessions['http_referer'].str.contains('bsearch',na = False))),
((website_sessions['utm_source']== 'not applicable') & (website_sessions['http_referer'].str.contains('socialbook',na = False)))]

choices = ['Paid_Search','Paid_Social','Organic_Search','Organic_Search','Organic Social']

website_sessions['channel_name'] = np.select(conditions,choices,default = 'Direct')

# %%
website_sessions[(website_sessions['utm_source']== 'not available') & (website_sessions['http_referer'].str.contains('gsearch',na = False))]

# %%
website_sessions.head()

# %%
website_sessions.info()

# %%
website_sessions['utm_source'].unique()

# %%
website_sessions['channel_name'].unique()

# %%
#### Channel Attributions 

website_sessions['channel_type'] = website_sessions['utm_source'].apply(lambda x: 'Paid' if x in ['gsearch','socialbook','bsearch'] else 'Free')

# %%
website_sessions_orders = pd.merge(website_sessions,orders,on = 'website_session_id',how = 'left',suffixes= (['_website_session','_orders']))

# %%
website_channel_summary = website_sessions_orders.groupby(['channel_type','channel_name']).agg(website_user_counts = ('user_id_website_session','nunique'),website_session_counts = ('website_session_id','nunique')
                                                                    ,orders_counts= ('order_id' , lambda x :x.notna().sum())).reset_index()

# %%
website_channel_summary['conversion_rate'] = (website_channel_summary['orders_counts']*100.00)/website_channel_summary['website_session_counts']

# %%
website_channel_summary

# %%
fig,axes = plt.subplots(figsize = (10,5))

x= np.arange(len(website_channel_summary['channel_name']))
width = 0.35

bar1 = axes.bar(x+width / 2 ,website_channel_summary['website_session_counts'],width,label = 'Sessions')
bar2 = axes.bar(x-width / 2 ,website_channel_summary['orders_counts'],width,label = 'Orders')

axes2 = axes.twinx()

axes2.plot(website_channel_summary['channel_name'],website_channel_summary['conversion_rate'],color = 'red',marker = 'o',label = 'Conversion_Rate')

axes.legend(loc = 'upper left')
axes2.legend(loc = 'upper right')
plt.title('Channel Perfomance Overview')
plt.show()

# %%
##### The business largely dependedent on paid channel_type about 84.7% and then free channel about 15.3% 
#### but for early business it is fine 
#### But the large dependent on paid channel will result in increase in customer acqustion and also 
#### it is not good for long term sustanibility.
#### Conversion rate of Organic search which is free channel type is high as compare to paid_search 
#### which means business is creating awarness and consideration by paid but with low intent of purchase whereas 
#### Organic search are with high intent to do purchase 
#### this means that customer are get first influenced by paid_channel then get converted by organi search 

# %%

website_session_channel = ((website_sessions.groupby('channel_type')['user_id'].nunique())*100.00/website_sessions['user_id'].nunique()).reset_index(name = 'cust_counts')

# %%
plt.pie(website_session_channel['cust_counts'],labels = website_session_channel['channel_type'],autopct = '%1.1f%%')
plt.title('Ditribution of Traffic by channel_type')
plt.show()

# %%
### Path Analysis
path_analysis_summ = website_sessions[website_sessions.groupby('user_id')['channel_name'].transform('nunique')>1]

# %%
path_analysis_summ['row_no'] = path_analysis_summ.groupby('user_id')['created_at'].cumcount()+1

# %%
path_analysis_summ =path_analysis_summ[path_analysis_summ['row_no'].isin([1,2])]

# %%
path_pivot = path_analysis_summ.pivot(index = 'user_id',columns = 'row_no' ,values = 'channel_name')

# %%
path_pivot = path_pivot.reset_index()

# %%
path_pivot

# %%
path_pivot['channel_shift'] = path_pivot[1] +'_to_'+ path_pivot[2]

# %%
### Path_Pivot 
path_pivots = path_pivot.groupby('channel_shift')['user_id'].count().reset_index(name = 'channel_counts')

# %%
plt.bar(path_pivots['channel_shift'],path_pivots['channel_counts'])
plt.xticks(path_pivots['channel_shift'],rotation = 90)
plt.title('Path Analysis to Channel_Shift')
plt.show()

# %%
path_analysis_summ = website_sessions[website_sessions.groupby('user_id')['channel_name'].transform('nunique')>1]
path_analysis_summ['row_no'] = path_analysis_summ.groupby('user_id')['created_at'].cumcount()+1

# %%
path_analysis_summ['row_no'] = path_analysis_summ['row_no'].astype('int')

# %%
website_sessions['row_no'] = website_sessions.groupby('user_id')['created_at'].cumcount()+1

# %%
websites_sessions_orders = pd.merge(orders,website_sessions,on = 'user_id',how = 'left',suffixes=('_orders','_website_session'))

# %%
orders_channel = websites_sessions_orders.groupby('channel_name').agg(orders_count = ('order_id','count')).reset_index()

# %%
plt.barh(orders_channel['channel_name'],orders_channel['orders_count'])
plt.title('Orders count By Channel_Name')
plt.show()

# %%
#### Bounce Rate Analysis 
landing = website_pageviews.groupby('website_session_id').first().reset_index()
landing

# %%
counts = website_pageviews.groupby('website_session_id').size().reset_index(name = 'pages')

# %%
counts

# %%
counts['is_bounce'] = (counts['pages'] == 1).astype('int')
sessions = pd.merge(counts,landing,how = 'left',on ='website_session_id')
page_wise_bounce_rates = sessions.groupby('pageview_url')['is_bounce'].mean().reset_index(name = 'bounce_rates')
page_wise_bounce_rates

# %%
plt.pie(page_wise_bounce_rates['bounce_rates'],labels=page_wise_bounce_rates['pageview_url'],autopct = '%1.1f%%')
plt.title('Page_view distributions based on bounce rates')
plt.show()

# %%
plt.bar(page_wise_bounce_rates['pageview_url'],page_wise_bounce_rates['bounce_rates'])
plt.title('Pageview_urls by bounce rates')
plt.show()

# %%
### Here , it is been observed the bounce rate at lander - 1 is highest that means after just veiwing this page 
### people left that means the landing page not effectively managing or matching the customer expectations 
### the bounce rate is least at landing page 5 that means there is a chance for these users that they may continue bowse more 

# %%
#### Campaign Performance Analysis 
website_orders = pd.merge(website_sessions,orders,on = 'website_session_id',how = 'left',suffixes= ('_website','_orders'))
campian_performance  = ((website_orders.groupby(['channel_name','utm_campaign'])['order_id'].apply(lambda x:x.notna().sum()))*100.00/website_orders.groupby(['channel_name','utm_campaign'])['website_session_id'].count()).reset_index(name = 'conversion_rate')

# %%
campian_performance

# %%
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(len(campian_performance))

fig, ax1 = plt.subplots(figsize=(10,5))

# bottom axis (channel)
ax1.plot(x, campian_performance['conversion_rate'], marker='o')
ax1.set_xticks(x)
ax1.set_xticklabels(campian_performance['channel_name'], rotation=45)
ax1.set_ylabel("Conversion Rate")

# top axis (campaign)
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(x)
ax2.set_xticklabels(campian_performance['utm_campaign'], rotation=45)

plt.show()


# %%
### Paid search of utm_campaign as brand having conversion rate the highest 
### Orgain_search & Direct free channels having conversion rate around 7%

# %%
#### the dependency of business of which channel_type 

website_sessions[website_sessions['channel_type'] == 'Paid']['user_id'].nunique()

# %%
#### users coming from channel type paid 
((website_sessions[website_sessions['channel_type'] == 'Paid']['user_id'].nunique())*100.00/website_sessions['user_id'].nunique())

# %%
#### users coming from channel type free
((website_sessions[website_sessions['channel_type'] == 'Free']['user_id'].nunique())*100.00/website_sessions['user_id'].nunique())

# %%
#### number of sessions by channel type paid 
((website_sessions[website_sessions['channel_type'] == 'Paid']['website_session_id'].nunique())*100.00/website_sessions['website_session_id'].nunique())

# %%
#### number of sessions by channel type free 
((website_sessions[website_sessions['channel_type'] == 'Free']['website_session_id'].nunique())*100.00/website_sessions['website_session_id'].nunique())

# %%
channel_paid_conversion = website_orders[website_orders['channel_type'] == 'Paid']

# %%

(channel_paid_conversion[channel_paid_conversion['order_id'].notna()]['order_id'].nunique())*100.00/channel_paid_conversion['website_session_id'].nunique() 

# %%
channel_free_conversion = website_orders[website_orders['channel_type'] == 'Free']
(channel_free_conversion[channel_free_conversion['order_id'].notna()]['order_id'].nunique())*100.00/channel_free_conversion['website_session_id'].nunique() 

# %%

channel_type_summary = website_orders.groupby('channel_type').agg(Total_orders = ('order_id',lambda x:x.notna().sum()),
                                           Total_sessions = ('website_session_id','nunique'),
                                           Total_revenue = ('price_usd','sum')).reset_index()

# %%
channel_type_summary['Total_orders_pct'] = channel_type_summary['Total_orders']*100.00/channel_type_summary['Total_orders'].sum()
channel_type_summary['Total_sessions_pct'] = channel_type_summary['Total_sessions']*100.00/channel_type_summary['Total_sessions'].sum()
channel_type_summary['Total_revenue_pct'] = channel_type_summary['Total_revenue']*100.00/channel_type_summary['Total_revenue'].sum()

# %%
channel_type_summary

# %%
fig,axes = plt.subplots(figsize = (10,5))

x = np.arange(len(channel_type_summary['channel_type']))
width = 0.34

axes.bar(x-width/2,channel_type_summary['Total_orders_pct'],width,label = 'Total_orders_pct')
axes.bar(x+width/2,channel_type_summary['Total_sessions_pct'],width,label = 'Total_sessions_pct')

axes2 = axes.twinx()

axes2.plot(x,channel_type_summary['Total_revenue_pct'],marker = 'o',color = 'green',label = 'Total_Revenue_prcnt')
axes.set_xticks(x)
axes.set_xticklabels(channel_type_summary['channel_type'])

lines1,labels1 = axes.get_legend_handles_labels()
lines2,labels2 = axes2.get_legend_handles_labels()
axes.legend(lines1 +lines2 , labels1 +  labels2)

plt.title('Channel Contribution: Orders vs Sessions vs Revenue')
axes.set_xlabel('Channel_Type')
axes.set_ylabel('Total_orders_pct /Total_sessions_pct ')
axes2.set_ylabel('Total_Revenue_prcnt')
plt.show()

# %%
### the customer can have multiple channels paid or free 
### the business largely dependent on paid channel as the Total_sessions and Total_orders is comparitively larger
### than free channel that's why revenue drive by paid is more 
### in case of conversion rate free channels converts faster than paid one whereas traffic acquistion is largely influenced by
### paid channel

##Paid channels dominate traffic, orders, and revenue
##Free channels generate fewer sessions but higher conversion
##Business relies on Paid for scale, Free for efficiency

# %%
website_sessions_device = website_sessions

# %%
website_session_device_orders = pd.merge(website_sessions_device,orders , on = 'website_session_id',how = 'left',suffixes= ('_website_session','_orders'))

# %%
website_session_device_orders = website_session_device_orders.sort_values('created_at_website_session')

# %%
#### where device is more than 1 and distinct devices 
website_session_device_orders = website_session_device_orders[website_session_device_orders.groupby('user_id_website_session')['device_type'].transform('nunique')>1]

# %%
website_session_device_orders = website_session_device_orders[~website_session_device_orders.duplicated(['user_id_website_session','device_type'])]
website_session_device_orders['device_count_type'] = website_session_device_orders.groupby('user_id_website_session')['device_type'].cumcount()+1
website_session_device_orders['device_type_usage'] = np.where(website_session_device_orders['device_count_type'] == 1,'First_Device_Type','Second_Device_Type')

# %%
website_session_device_orders['converted_into_order'] =np.where(website_session_device_orders['order_id'].notna(),'Converted','Not_Converted')

# %%
website_session_device_orders_pivot = website_session_device_orders.pivot(index ='user_id_website_session',columns = 'device_type_usage',values = 'device_type')
website_session_device_orders_pivot['device_shift'] = website_session_device_orders_pivot['First_Device_Type'] + '_to_' + website_session_device_orders_pivot['Second_Device_Type']

# %%
device_shift_counts = website_session_device_orders_pivot.groupby('device_shift').size().reset_index(name = 'user_counts')

# %%
plt.bar(device_shift_counts['device_shift'],device_shift_counts['user_counts'])
plt.title('User counts based of Device shift')
plt.show()

# %%
#### here in case of traffic most customer started off with desktop then shifted to mobile 
#### then some of them started off with mobile then shifted to desktop

# %%
conversion_or_not = pd.merge(website_session_device_orders_pivot,website_session_device_orders,on = 'user_id_website_session',how= 'left')

# %%
conversion_or_not = conversion_or_not.groupby(['converted_into_order','device_shift'])['user_id_website_session'].count().reset_index(name = 'user_counts')

# %%
fig,axes = plt.subplots(2,1,figsize = (10,6))

converted_orders = conversion_or_not[conversion_or_not['converted_into_order'] == 'Converted']
axes[0].bar(converted_orders['device_shift'],converted_orders['user_counts'])
axes[0].set_title('Converted Order Device By Shift')

for i,val in enumerate(converted_orders['user_counts']):
    axes[0].text(i,val,str(val),ha = 'center' , va = 'bottom')

non_converted_orders = conversion_or_not[conversion_or_not['converted_into_order'] == 'Not_Converted']
axes[1].bar(non_converted_orders['device_shift'],non_converted_orders['user_counts'])

for i,val in enumerate(non_converted_orders['user_counts']):
    axes[1].text(i,val,str(val),ha = 'center' , va = 'bottom')

axes[1].set_title('Non_Converted Order By Device Shift')

plt.tight_layout()

# %%
converted_orders['conversion_rate'] = (converted_orders['user_counts'])*100.00/converted_orders['user_counts'].sum()

# %%
converted_orders

# %%
plt.pie(converted_orders['conversion_rate'] , labels = converted_orders['device_shift'],autopct = '%1.1f%%')
plt.title('Contribution to Total Conversions by Device Shift')
plt.show()

# %%
### It is very evidient from the above chart that the customer
### who the desktop to mobile have higher contribution to total_conversion by device shift

# %%
conversion_ratesss = ((conversion_or_not[conversion_or_not['converted_into_order'] == 'Converted'].groupby('device_shift')['user_counts'].sum())*100.00/conversion_or_not.groupby('device_shift')['user_counts'].sum()).reset_index(name  = 'conversion_rate')

# %%
plt.pie(conversion_ratesss['conversion_rate'],labels = conversion_ratesss['device_shift'],autopct = '%1.1f%%')
plt.title('Total_Conversion Rate by Device_Shift')
plt.show()

# %%
### there is a high chances of user to get converted whose first device is mobile then shiting to deskstop 
### The business itself having a high traffic for the customer who are using desktop about more than 80% .
### That means the users who are login with mobile have high chances to get converted as compare to desktop 

# %%
products

# %%
#### cart abandoment or not / funnel stage / cart journey stage

# %%
cart_abandonment = website_pageviews

# %%
cart_abandonment['created_at'] = cart_abandonment['created_at'].sort_values()

# %%
cart_abandonment['pageviews_row_no'] = cart_abandonment.groupby('website_session_id')['pageview_url'].cumcount()+1

# %%
cart_abandonment['pageview_url'].unique()

# %%
cart_abandonment['last_page_viewed'] = cart_abandonment.groupby('website_session_id')['pageviews_row_no'].max().astype('int')

# %%
cart_abandonment = cart_abandonment.drop(columns = 'last_page_viewed')

# %%
last_page = cart_abandonment.groupby('website_session_id')['pageviews_row_no'].max().reset_index(name = 'last_page_viewed')

# %%
last_page['funnel_stage'] = np.where(last_page['last_page_viewed'] == 4 ,'Cart_Abandonment',np.where (last_page['last_page_viewed'] <4 ,'Not_Yet_Reached_To_Cart','Beyond_Cart_Page'))

# %%
funnel_stage = last_page.groupby('funnel_stage')['website_session_id'].nunique().reset_index(name = 'sessions_counts')
funnel_stage

# %%
plt.bar(funnel_stage['funnel_stage'],funnel_stage['sessions_counts'])
plt.title('Last Page Stage')
plt.xticks(funnel_stage['funnel_stage'],rotation = 90)

for i,val in enumerate(funnel_stage['sessions_counts']):
    plt.text(i,val+0.05,val,ha ='center',va = 'bottom')
plt.show()

# %%
plt.pie(funnel_stage['sessions_counts'],labels = funnel_stage['funnel_stage'],autopct = '%1.1f%%')
plt.title('Funnel Stage Distributions')
plt.show()

# %%
### about 79.9% sessions where user haven't reached till the cart .
### about 6.4% of users left at the cart page and about 13.6% goes beyond it .
### this tell where the traffic drop off at what page helps in funnel optimizations .

# %%
### is there is any change after launching the product in revenue orders??

products

# %%

orders_products = pd.merge(orders,products, left_on = 'primary_product_id',right_on = 'product_id',how ='left',suffixes=('_orders','_products'))

# %%
(products['created_at'] - products['created_at'].shift(1)).dt.days

# %%
next_product_launch =products.copy()

# %%
next_product_launch

# %%
next_product_launch['next_product_launch_date'] = products['created_at'].shift(-1)
next_product_launch

# %%
orders_products_ = pd.merge(orders_products,next_product_launch,on = ['product_id','product_name'],how = 'left')

# %%
orders_products_['orders_pre_launch_date'] = orders_products_['created_at_orders']<orders_products_['next_product_launch_date']

# %%
orders_products_['orders_pre_launch_date'].unique()

# %%
pre_product_launch_next = orders_products_[orders_products_['orders_pre_launch_date']==True].groupby('product_name').agg(Total_orders = ('order_id','count'),Revenue=('price_usd','sum'))

# %%
post_product_launch_next = orders_products_[orders_products_['orders_pre_launch_date']==False].groupby('product_name').agg(Total_orders = ('order_id','count'),Revenue=('price_usd','sum'))

# %%
pre_product_launch_next

# %%
post_product_launch_next

# %%
prct_change_after_launch_second = ((post_product_launch_next - pre_product_launch_next)*100.00/pre_product_launch_next).reset_index()

# %%
prct_change_after_launch_second

# %%
fig,axes = plt.subplots(figsize = (10,5))
axes.bar(prct_change_after_launch_second['product_name'],prct_change_after_launch_second['Total_orders'],label = 'orders_prct_change')
axes.set_xticks(prct_change_after_launch_second['product_name'])
axes.set_ylabel('orders_prct_change')

axes2 = axes.twinx()
axes2.plot(prct_change_after_launch_second['product_name'],prct_change_after_launch_second['Revenue'],label = 'revenue_prct_change',color = 'green',marker = 'o')
axes2.set_ylabel('revenue_prct_change')

lines,labels = axes.get_legend_handles_labels()
lines2,labels2 = axes2.get_legend_handles_labels()

axes.legend(lines+lines2,labels+labels2)

plt.title('%Change in Revenue & Orders After Launching Second Product')
plt.show()

# %%
### There is a positive change in revenue and orders after launching next products 
### the product the birthday sugar panda have the highest change in revenue prct_change

# %%
#### before official launch of product how is the orders and revenue
orders_products = orders_products.rename(columns = {'created_at_products':'launch_product_day'})
orders_products['created_at_orders'] =orders_products['created_at_orders'].dt.normalize()
orders_products['launch_product_day'] =orders_products['launch_product_day'].dt.normalize()

orders_products['Launch_Phase'] = np.where(orders_products['created_at_orders']<=orders_products['launch_product_day'],'Pre_Launch','Post_Launch')

pre_post_official_launch = orders_products.groupby(['Launch_Phase','product_name']).agg(Total_orders = ('order_id','count'),Total_Revenue = ('price_usd','sum')).reset_index()

# %%
### how much time it takes to get the user_login and get converted 
orders_web = website_orders[website_orders['order_id'].notna()]
time_change = (orders_web['created_at_orders']-orders_web['created_at_website']).dt.total_seconds()/3600

# %%
plt.hist(time_change,bins = 24)
plt.title('Time Taken By User To Get Converted')
plt.show()

# %%
#### mostly customer get converted with in 15 minutes 

# %%
#### cohort_analysis 
cohort = orders.copy()
cohort['first_purchase'] = orders.groupby('user_id')['created_at'].transform('min')
cohort['cohort_month'] = cohort['first_purchase'].dt.to_period('M')
cohort['order_month'] = cohort['created_at'].dt.to_period('M')

cohort['cohort_index'] = (cohort['order_month'] - cohort['cohort_month']).apply(lambda x:x.n)

# %%
cohort_analysis = cohort.groupby(['cohort_month','cohort_index'])['user_id'].nunique().unstack(1)
sns.heatmap(cohort_analysis,cmap="YlGnBu")
plt.title('Cohort Analysis Heatmap')
plt.show()

# %%
### customer only retaining for max 4 months


