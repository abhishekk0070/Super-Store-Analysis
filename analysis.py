import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# import data file
df = pd.read_csv("cleanedSuperStore2.csv")

# Convert 'Order Date' and 'Ship Date' to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# df.info()

# styling
st.markdown("""
  <style>
  .fontSize{
  font-size: 18px 
  }
  .fontSize2{
  font-size: 20px
  }
  </style>
  """, unsafe_allow_html=True)


def projectOverview():
    st.header("Project Overview")
    # Introduction paragraph with custom font size
    st.markdown(
        '<p class="fontSize">This application provides a comprehensive analysis of sales and performance data from a '
        'retail superstore.'
        'By examining key metrics and trends, we uncover insights that can drive strategic decision-making, '
        'improve operational efficiency, and enhance customer satisfaction.</p>',
        unsafe_allow_html=True)
    st.markdown("""
    ## Objectives
    1. <b class="fontSize"> *Sales Performance Analysis* </b>: Evaluate overall sales performance and identify
                                                               top-performing products, categories, and time periods.
    2. <b class="fontSize">*Customer Insights*</b>: Understand customer demographics,purchasing behavior
                                                    ,and preferences.
    3. <b class="fontSize">*Regional Performance*</b>: Analyze sales data by region to identify high-performing areas
                                                       and regions that need improvement.
    4. <b class="fontSize">*Profitability Analysis*</b>: Assess profitability across different products, categories,
                                                         and regions.
    5. <b class="fontSize">*Trend Identification*</b>: Identify trends and patterns in sales data over time.
    6. <b class="fontSize">*Recommendations*</b>: Provide actionable recommendations based on the analysis to optimize
                                                  sales, marketing strategies, and inventory management.
    """, unsafe_allow_html=True)


def datasetInfo():
    st.header("Dataset Overview")
    st.markdown(
        '''<p class="fontSize">The dataset contains sales data from a retail superstore, capturing various aspects of 
           transactions,customer information, and product details. Here's a brief overview of the key components of the 
           dataset:</p>''', unsafe_allow_html=True)
    st.markdown("""
    <b class="fontSize2">Order Information</b>

    * <b>*Order ID*:</b> Unique identifier for each order.
    * <b>*Order Date*:</b> Date when the order was placed.
    * <b>*Ship Date*:</b> Date when the order was shipped.
    * <b>*Ship Mode*:</b> Mode of shipping for the order (e.g., Second Class, Standard Class).
    
    <b class="fontSize2">Customer Information</b>
    
    * <b>*Customer ID*:</b> Unique identifier for each customer.
    * <b>*Customer Name*:</b> Name of the customer.
    * <b>*Segment*:</b> Customer segment (e.g., Consumer, Corporate).
    
    <b class="fontSize2">Geographical Information</b>
    
    * <b>*Country*:</b> Country of the customer.
    * <b>*City*:</b> City of the customer.
    * <b>*State*:</b> State of the customer.
    * <b>*Postal Code*:</b> Postal code of the customer.
    * <b>*Region*:</b> Region of the customer (e.g., South, West).
    
    <b class="fontSize2">Product Information</b>
    
    * <b>*Product ID*:</b> Unique identifier for each product.
    * <b>*Category*:</b> Category of the product (e.g., Furniture, Office Supplies).
    * <b>*Sub-Category*:</b> Sub-category of the product (e.g., Bookcases, Chairs).
    * <b>*Product Name*:</b> Name of the product.
    
    <b class="fontSize2">Transaction Details</b>
    
    * <b>*Sales*:</b> Sales amount for the transaction.
    * <b>*Quantity*:</b> Quantity of the product ordered.
    * <b>*Discount*:</b> Discount applied to the transaction.
    * <b>*Profit*:</b> Profit earned from the transaction.""", unsafe_allow_html=True)

    st.header("First 5 Rows of the Super Store Dataset")
    st.dataframe(df.head())


def overallAnalysis():
    st.header("Overall Analysis")
    total_sales = df['Sales'].sum().round(2)
    total_profit = df['Profit'].sum().round(2)
    average_sales = df["Sales"].mean().round(2)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", "$" + str(total_sales))
    with col2:
        st.metric("Total Profit", "$" + str(total_profit))
    with col3:
        st.metric("Average Sales", "$" + str(average_sales))

    # Sales and Profit Over Time
    st.subheader("Sales and Profit Over Time")
    df['YearMonth'] = df['Order Date'].dt.to_period('M')
    monthly_performance = df.groupby('YearMonth').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly_performance['YearMonth'] = monthly_performance['YearMonth'].astype(str)
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.lineplot(data=monthly_performance, x='YearMonth', y='Sales', ax=ax, label='Sales')
    sns.lineplot(data=monthly_performance, x='YearMonth', y='Profit', ax=ax, label='Profit')
    ax.set_title('Monthly Sales and Profit')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Sales and Profit by Region
    st.subheader("Sales and Profit by Region")
    region_performance = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=region_performance, x='Region', y='Sales', ax=ax)
    ax.set_title('Sales by Region')
    st.pyplot(fig)
    fig, ax = plt.subplots()
    sns.barplot(data=region_performance, x='Region', y='Profit', ax=ax)
    ax.set_title('Profit by Region')
    st.pyplot(fig)

    # Customer Segmentation
    st.subheader("Customer Segmentation")
    segment_performance = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=segment_performance, x='Segment', y='Sales', ax=ax)
    ax.set_title('Sales by Customer Segment')
    st.pyplot(fig)

    plt.figure(figsize=(5, 4))
    catCustomerSegment = sns.countplot(x="Segment", data=df, hue="Category")
    for bar in catCustomerSegment.containers:
        catCustomerSegment.bar_label(bar)
    plt.title("Category wise Customer Segment")
    st.pyplot(plt)

    fig, ax = plt.subplots()
    sns.barplot(data=segment_performance, x='Segment', y='Profit', ax=ax)
    ax.set_title('Profit by Customer Segment')
    st.pyplot(fig)

    # Product Category Analysis
    st.subheader("Product Category Analysis")
    category_performance = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=category_performance, x='Category', y='Sales', ax=ax)
    ax.set_title('Sales by Product Category')
    st.pyplot(fig)
    fig, ax = plt.subplots()
    sns.barplot(data=category_performance, x='Category', y='Profit', ax=ax)
    ax.set_title('Profit by Product Category')
    st.pyplot(fig)




def furnitureAnalysis():
    sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
    furniture_sales = sales_by_category[sales_by_category['Category'] == 'Furniture']['Sales'].values[0].round(2)

    profit_by_category = df.groupby('Category')['Profit'].sum().reset_index()
    furniture_profit = profit_by_category[profit_by_category['Category'] == 'Furniture']['Profit'].values[0].round(2)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Furniture Sales", "$" + str(furniture_sales))

    with col2:
        st.metric("Furniture Profit", "$" + str(furniture_profit))

    st.header("Furniture Sub-Category")
    plt.figure(figsize=(5, 4))
    subFurniture = sns.countplot(x="Category", data=df[df["Category"] == "Furniture"], hue="Sub-Category")
    # Annotate each bar with the exact value
    for bar in subFurniture.containers:
        subFurniture.bar_label(bar)
    plt.title("Furniture Sub Category")
    st.pyplot(plt)

    furniture_df = df[df['Category'] == 'Furniture']

    # Aggregate sales by date and sub-category
    furniture_sales_time = furniture_df.groupby(['Order Year', 'Sub-Category'])['Sales'].sum().reset_index()

    # Create a line plot for sales over time by sub-category
    st.subheader("Furniture Sub-Category Sales Over Time")
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=furniture_sales_time, x='Order Year', y='Sales', hue='Sub-Category')
    plt.title("Sales Over Time by Furniture Sub-Category")
    plt.xlabel("Date")
    plt.ylabel("Total Sales")
    st.pyplot(plt)


def officeSupplyAnalysis():
    sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
    office_supplies_sales = sales_by_category[sales_by_category['Category'] == 'Office Supplies']['Sales'].values[
        0].round(2)

    profit_by_category = df.groupby('Category')['Profit'].sum().reset_index()
    office_supplies_profit = profit_by_category[profit_by_category['Category'] == 'Office Supplies']['Profit'].values[
        0].round(2)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Office Supply Sales", "$" + str(office_supplies_sales))

    with col2:
        st.metric("Office Supply Profit", "$" + str(office_supplies_profit))

    st.header("Office Supply Sub-Category")
    plt.figure(figsize=(5, 4))
    subOfficeSupply = sns.countplot(x="Category", data=df[df["Category"] == "Office Supplies"], hue="Sub-Category")
    # Annotate each bar with the exact value
    for bar in subOfficeSupply.containers:
        subOfficeSupply.bar_label(bar)
    plt.title("office Supply Sub Category")
    st.pyplot(plt)

    officeSupply_df = df[df['Category'] == 'Office Supplies']

    # Aggregate sales by date and sub-category
    officeSupply_sales_time = officeSupply_df.groupby(['Order Year', 'Sub-Category'])['Sales'].sum().reset_index()

    # Create a line plot for sales over time by sub-category
    st.subheader("Office Supply Sub-Category Sales Over Time")
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=officeSupply_sales_time, x='Order Year', y='Sales', hue='Sub-Category')
    plt.legend(loc='upper left')
    plt.title("Sales Over Time by Office Supply Sub-Category")
    plt.xlabel("Date")
    plt.ylabel("Total Sales")
    st.pyplot(plt)


def technologyAnalysis():
    sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
    technology_sales = sales_by_category[sales_by_category['Category'] == 'Technology']['Sales'].values[0].round(2)

    profit_by_category = df.groupby('Category')['Profit'].sum().reset_index()
    technology_profit = profit_by_category[profit_by_category['Category'] == 'Technology']['Profit'].values[0].round(2)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Technology Sales", "$" + str(technology_sales))

    with col2:
        st.metric("Technology Profit", "$" + str(technology_profit))

    st.header("technology Sub-Category")
    plt.figure(figsize=(5, 4))
    subTechnology = sns.countplot(x="Category", data=df[df["Category"] == "Technology"], hue="Sub-Category")
    # Annotate each bar with the exact value
    for bar in subTechnology.containers:
        subTechnology.bar_label(bar)
    plt.title("Technology Sub Category")
    st.pyplot(plt)

    Technology_df = df[df['Category'] == 'Technology']

    # Aggregate sales by date and sub-category
    Technology_sales_time = Technology_df.groupby(['Order Year', 'Sub-Category'])['Sales'].sum().reset_index()

    # Create a line plot for sales over time by sub-category
    st.subheader("Technology Sub-Category Sales Over Time")
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=Technology_sales_time, x='Order Year', y='Sales', hue='Sub-Category')
    #plt.legend(loc='upper left')
    plt.title("Sales Over Time by Technology Sub-Category")
    plt.xlabel("Date")
    plt.ylabel("Total Sales")
    st.pyplot(plt)


def categoryWiseAnalysis():
    st.header("Analysis According to Category ")

    # List of categories
    categories = ['Furniture', 'Office Supplies', 'Technology']

    # Create a horizontal navigation bar
    selected_category = option_menu(
        menu_title=None,  # no title
        options=categories,
        icons=['archive', 'box', 'laptop'],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )
    # Display the sales value based on the selected category
    if selected_category == 'Furniture':
        furnitureAnalysis()
    elif selected_category == 'Office Supplies':
        officeSupplyAnalysis()
    elif selected_category == 'Technology':
        technologyAnalysis()

def shipModeAnalysis():
    st.header("Shipping Mode Analysis")
    x = df["Ship Mode"].value_counts().index
    y = df["Ship Mode"].value_counts().values
    plt.figure(figsize=(5, 4))
    piePlot = plt.pie(y, labels=x, startangle=45, autopct="%0.2f%%", shadow=True)
    plt.title("Shiping Mode")
    st.pyplot(plt)

    st.header("Shipping Mode Analysis by Category")
    plt.figure(figsize=(7, 5))
    shipCountPlot = sns.countplot(x="Ship Mode", data=df, hue="Category")
    for bar in shipCountPlot.containers:
        shipCountPlot.bar_label(bar)
    plt.title("Category Wise Shipping Mode")
    st.pyplot(plt)

def discountAnalysis():
    st.header("Discount Analysis")
    st.subheader("Impact of Discounts")
    discount_performance = df.groupby('Discount').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(data=discount_performance, x='Discount', y='Sales', ax=ax)
    ax.set_title('Sales by Discount')
    st.pyplot(fig)
    fig, ax = plt.subplots()
    sns.lineplot(data=discount_performance, x='Discount', y='Profit', ax=ax)
    ax.set_title('Profit by Discount')
    st.pyplot(fig)

def top_Products_and_Customers():
    st.header("Top Products and Customers")
    # Top Products
    st.subheader("Top Products")
    top_products = df.groupby('Product Name').agg({'Sales': 'sum'}).reset_index().sort_values(by='Sales',
                                                                                              ascending=False).head(10)
    st.dataframe(top_products)

    # Top Customers
    st.subheader("Top Customers")
    top_customers = df.groupby('Customer Name').agg({'Sales': 'sum'}).reset_index().sort_values(by='Sales',
                                                                                                ascending=False).head(
        10)
    st.dataframe(top_customers)



st.sidebar.title("Super Store Analysis")
option = st.sidebar.selectbox("Select One",
                              ["Project Overview", "Dataset Information", "Overall Analysis", "Category Wise Analysis",
                               "Ship Mode","Discount Analysis","Top Products and Customers"])

if option == "Project Overview":
    projectOverview()
elif option == "Dataset Information":
    datasetInfo()
elif option == "Overall Analysis":
    overallAnalysis()
elif option == "Category Wise Analysis":
    categoryWiseAnalysis()
elif option == "Ship Mode":
    shipModeAnalysis()
elif option == "Discount Analysis":
    discountAnalysis()
elif option == "Top Products and Customers":
    top_Products_and_Customers()
