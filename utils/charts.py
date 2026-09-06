import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_target_distribution(df: pd.DataFrame):
    if "TARGET" not in df.columns:
        raise ValueError("DataFrame must contain a 'TARGET' column")

    target_counts = df["TARGET"].value_counts().rename(index={0: "Repaid", 1: "Default"})
    target_counts = target_counts.reset_index()
    target_counts.columns = ["Target", "Count"]

    fig = px.bar(target_counts, x="Target", y="Count", title="Target Distribution")
    return fig


def plot_bar_by_category(df: pd.DataFrame, category_col: str, title: str):
    if category_col not in df.columns:
        raise ValueError(f"Column '{category_col}' not found in DataFrame")

    counts = df[category_col].value_counts().reset_index()
    counts.columns = [category_col, "Count"]
    fig = px.bar(counts, x=category_col, y="Count", title=title)
    return fig


def line_chart(df:pd.DataFrame,date_col: str,value_col:str,title:str,freq:str="ME"):
    data = df.copy()
    if hasattr(data[date_col].dtype, "kind") and data[date_col].dtype.kind=="O":
        try:
            data[date_col]=pd.to_datetime(data[date_col].astype(str))
        except:
            pass
    data = data.groupby(pd.Grouper(key=date_col,freq=freq))[value_col].sum().reset_index()
    fig = px.line(data,x=date_col,y=value_col,title=title,markers=True)
    fig.update_layout(xaxis_title="Month",yaxis_title=value_col)
    return fig



def multi_line_chart(df:pd.DataFrame,date_col: str,value_col:str,title:str,freq:str="ME"):
    data = df.copy()
    if hasattr(data[date_col].dtype, "kind") and data[date_col].dtype.kind=="O":
        try:
            data[date_col]=pd.to_datetime(data[date_col].astype(str))
        except:
            pass
    data = data.groupby(pd.Grouper(key=date_col,freq=freq))[value_col].sum().reset_index()
    fig = px.line(data,x=date_col,y=value_col,title=title,markers=True)
    return fig

def bar_chart(df:pd.DataFrame,group_col:str,value_col:str | None, title:str, top_n: int=None, aggfunc:str="sum"):
    if value_col is None:
        data= df.groupby(group_col).size().reset_index(name="value")
    elif aggfunc=="sum":
        data=df.groupby(group_col)[value_col].sum().reset_index(name=value_col)
    elif aggfunc=="count":
        data=df.groupby(group_col)[value_col].count().reset_index(name=value_col)
    elif aggfunc=="nunique":
        data=df.groupby(group_col)[value_col].nunique().reset_index(name=value_col)
    else:
        data=df.groupby(group_col)[value_col].sum().reset_index(name=value_col)

    sort_col="value" if value_col is None else value_col
    data=data.sort_values(sort_col,ascending=False)
    if top_n:
        data=data.head(top_n)
    fig=px.bar(data,x=group_col,y=sort_col,title=title,text=sort_col)
    return fig

def horizontal_bar_chart(df:pd.DataFrame,group_col:str,value_col:str,title:str,top_n:int=None):
    data=df.groupby(group_col)[value_col].sum().reset_index(name=value_col)
    data=data.sort_values(value_col,ascending=True)
    if top_n:
        data=data.tail(top_n)
        fig=px.bar(data,y=group_col,x=value_col,title=title,orientation="h")
        return fig
def scatter_chart(df:pd.DataFrame,x_col:str,y_col:str,color_col:str | None ,title:str):
    fig =px.scatter(df,x=x_col,y=y_col,color=color_col,title=title)
    return fig

def histogram_chart(df:pd.DataFrame,column:str,title:str):
    fig=px.histogram(df, x=column, nbins=30, title=title)
    return fig

def pie_chart(df:pd.DataFrame,values_col:str,names_col:str,title:str):
    data=df.groupby(names_col)[values_col].sum().reset_index()
    fig=px.pie(data,values=values_col,names=names_col,title=title)
    return fig

def box_plot(df:pd.DataFrame,x_col:str,y_col:str | None, title:str):
    fig=px.box(df,x=x_col,y=y_col,title=title)
    return fig

def heatmap(data: pd.DataFrame,title:str):
    fig=go.Figure(data=go.Heatmap(z=data.values,x=data.columns,y=data.index))
    fig.update_layout(title=title)
    return fig

def waterfall_chart(df:pd.DataFrame,category_col:str,value_col:str,title:str):
    data=df.groupby(category_col)[value_col].sum().reset_index()
    fig=go.Figure(go.waterfall(
        x=data[category_col],
        y=data[value_col],
        textposition="outside",
        text=data[value_col],
    ))
    fig.update_layout(title=title)
    return fig