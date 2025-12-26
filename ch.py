# 第10章/final_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

def get_dataframe_from_excel():
    # 读取Excel文件数据（建议使用完整路径避免找不到文件）
    # 若文件和脚本同目录，保持原文件名；否则替换为实际路径，例如：r"D:\your_path\supermarket_sales.xlsx"
    df = pd.read_excel(
        "supermarket_sales.xlsx",  # 若找不到文件，替换为完整路径
        sheet_name='销售数据',
        skiprows=1,
        index_col='订单号'
    )
    # 提取交易小时数
    df['小时数'] = pd.to_datetime(df["时间"], format="%H:%M:%S").dt.hour
    return df

def add_sidebar_func(df):
    # 创建侧边栏
    with st.sidebar:
        st.header("请筛选数据：")
        
        # 城市筛选
        city_unique = df["城市"].unique()
        city = st.multiselect(
            "请选择城市：",
            options=city_unique,
            default=city_unique
        )
        
        # 顾客类型筛选
        customer_type_unique = df["顾客类型"].unique()
        customer_type = st.multiselect(
            "请选择顾客类型：",
            options=customer_type_unique,
            default=customer_type_unique
        )
        
        # 性别筛选
        gender_unique = df["性别"].unique()
        gender = st.multiselect(
            "请选择性别：",
            options=gender_unique,
            default=gender_unique
        )
        
        # 数据筛选逻辑
        df_selection = df.query(
            "城市 == @city & 顾客类型 == @customer_type & 性别 == @gender"
        )
        return df_selection

def product_line_chart(df):
    # 按产品类型分组计算总价（修复sort_values参数错误：Series无需by参数）
    sales_by_product_line = (
        df.groupby(by=["产品类型"])["总价"].sum().sort_values()  # 移除了无效的by="总价"参数
    )
    # 生成横向条形图
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>"
    )
    return fig_product_sales

def hour_chart(df):
    # 按小时数分组计算总价
    sales_by_hour = df.groupby(by=["小时数"])["总价"].sum()
    # 生成条形图
    fig_hour_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时数划分的销售额</b>"
    )
    return fig_hour_sales

def main_page_demo(df):
    # 设置主页面标题
    st.title(":bar_chart: 销售仪表板")
    
    # 创建关键指标展示区
    left_key_col, middle_key_col, right_key_col = st.columns(3)
    
    # 计算核心指标
    total_sales = int(df["总价"].sum())
    average_rating = round(df["评分"].mean(), 1)
    star_rating_string = ":star:" * int(round(average_rating, 0))
    average_sale_by_transaction = round(df["总价"].mean(), 2)
    
    # 展示核心指标
    with left_key_col:
        st.subheader("总销售额：")
        st.subheader(f"RMB ¥ {total_sales:,}")
    
    with middle_key_col:
        st.subheader("顾客评分的平均值：")
        st.subheader(f"{average_rating} {star_rating_string}")
    
    with right_key_col:
        st.subheader("每单的平均销售额：")
        st.subheader(f"RMB ¥ {average_sale_by_transaction}")
    
    st.divider()  # 水平分割线
    
    # 创建图表展示区
    left_chart_col, right_chart_col = st.columns(2)
    
    with left_chart_col:
        hour_fig = hour_chart(df)
        st.plotly_chart(hour_fig, use_container_width=True)
    
    with right_chart_col:
        product_fig = product_line_chart(df)
        st.plotly_chart(product_fig, use_container_width=True)

def run_app():
    # 页面配置
    st.set_page_config(
        page_title="销售仪表板",
        page_icon=":bar_chart:",
        layout="wide"
    )
    # 读取数据
    sale_df = get_dataframe_from_excel()
    # 侧边栏筛选数据
    df_selection = add_sidebar_func(sale_df)
    # 渲染主页面
    main_page_demo(df_selection)

# 程序入口
if __name__ == "__main__":
    run_app()
