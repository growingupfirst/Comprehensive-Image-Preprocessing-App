import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
#---CODE---
st.markdown("<h1 style='text-align: center;'> Class Balancer </h1>", unsafe_allow_html=True)
st.markdown("---")

# file = 'C:\\Users\\user\\Downloads\\Something.v9-stable.coco.v1i.coco\\train\\_annotations.coco.json'
file_bytes = st.file_uploader('Load the COCO JSON File', type=['json'])
if file_bytes:
    file_path = "data/" + file_bytes.name
    with open(file_path, 'wb') as f:
        f.write(file_bytes.read())
    with open(file_path, 'r') as f:
        coco = json.load(f)


    classes = {}
    for annotation in coco['annotations']:
        if annotation['category_id'] not in classes.keys():
            classes[annotation['category_id']] = 0
        else:
            classes[annotation['category_id']] +=1

    new_classes = {}
    for class_ in classes.keys():
        for category in coco['categories']:
            if class_ == category['id']:
                new_classes[category['name']] = classes[class_]

    fig = go.Figure(data = [go.Bar(x=list(new_classes.keys()),
                                    y=list(new_classes.values()), marker=dict(color=np.random.randn(500)))
                                    ], layout=dict(barcornerradius=15,
                                                   ))
    fig.update_layout(title='Military Data', xaxis_title='Category', yaxis_title='Count')
    fig.update_traces()
    st.plotly_chart(fig)

