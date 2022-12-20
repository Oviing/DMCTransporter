import streamlit as st
import pandas as pd
import requests
import json
st.set_page_config(page_title="Resource Types")
st.sidebar.header("Transport resource Types")


bearer_token = st.text_area("Insert header")
headers= { 'Authorization': 'Bearer ' + bearer_token, 'Content-Type': 'application/json'}
apiendpoint = st.selectbox(
    'Select region',
    ('https://api.test.eu20.dmc.cloud.sap', 'https://api.eu20.dmc.cloud.sap'))


uploaded_files = st.file_uploader("Insert Document", accept_multiple_files=False)

if uploaded_files != None:
    df = pd.read_csv(uploaded_files, sep =";", dtype= {"plant": str, "resourceType": str, "description": str})
    df.head()
    st.dataframe(df)
else:
    st.info("No file is uploaded")



if st.button("Transport"):
    targetUrl = apiendpoint + "/resourcetype/v1/resourcetypes"
    data = df
    headers = headers

    print("Token was generated")

    for i in range(0, len(data)):

        plant = data["plant"].iloc[i]
        resourceType = data["resourceType"].iloc[i]
        description = data["description"].iloc[i]
        
        st.write(plant)
        st.write(resourceType)
        st.write(description)

        payload = json.dumps({
            "plant": str(plant),
            "resourceType": str(resourceType),
            "description": str(description),
            "createdOn": "2022-05-24T07:33:43Z",
            "modifiedOn": "2022-05-24T07:33:43Z"
            })
        
        print("Payload generated with following values:", payload, type(payload))
        response = requests.request("POST", targetUrl, headers=headers, data=payload)

        print(resourceType, "with respopnse code", response.status_code)
        st.progress(i / len(data))
        if response.status_code == 201:
            st.success("200")

        else:
            a = "Problem occured with resource type " + resourceType
            st.error(a)
     
    print("All resource types were uploaded")
    

