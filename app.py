import streamlit as st
import json
import jwt

import pandas as pd
import requests

st.set_page_config(page_title="Token generation")

def converter(data):
    l = []
    for i in range(0, len(data)):

        plant = str(data["plant"].iloc[i])
        resourceType_raw = str(data["resourceType"].iloc[i])
        #new_string = resourceType_raw.replace(",", "." )
        resourceType = resourceType_raw + "00"
        description = str(data["description"].iloc[i])

        l.append((plant, resourceType, description))
    df = pd.DataFrame(l)
    return df

def preprocessing(path):

    data = pd.read_csv(path, sep =";")


    data_preprocessed = converter(data)
    data_preprocessed.columns =['plant', 'resourceType', 'description']

    return data_preprocessed

def transport(data, targetUrl, header):

    headers = header

    print("Token was generated")

    for i in range(0, len(data)):

        plant = data["plant"].iloc[i]
        resourceType = data["resourceType"].iloc[i]
        description = data["description"].iloc[i]

        payload = json.dumps({
            "plant": plant,
            "resourceType": resourceType,
            "description": description,
            "createdOn": "2022-05-24T07:33:43Z",
            "modifiedOn": "2022-05-24T07:33:43Z"
            })
        
        print("Payload generated with following values:", payload, type(payload))
        response = requests.request("POST", targetUrl, headers=headers, data=payload)

        print(resourceType, "with respopnse code", response.status_code)

        if response.status_code == 201:
            st.progress(i / len(data))

        else:
            print("Problem occured with resource type", resourceType)
     
    print("All resource types were uploaded")

st.title("DMC Transportation Tool")


uploaded_files = st.file_uploader("Insert Key Json ", accept_multiple_files=False)
try:
    data = json.load(uploaded_files)

    if "uaa" in data:

        clientid = data["uaa"]["clientid"]
        secret = data["uaa"]["clientsecret"]
        url = data["uaa"]["url"] + "/oauth/token"
        apiendpoint = data["public-api-endpoint"]

        st.success("Information were retrieved")
        st.write(url)

    
    else:
        st.error("Wrong file was uploaded. Please ensure that the file math the keys downloaded from SAP BTP")

except AttributeError:
    st.write("Upload file")





if st.button('Generate token'):
    if len(clientid) > 0:

        payload = {
            "cliendid" : clientid,
            "secret": secret,
            "url": url
        }
        encoded_jwt = jwt.encode(payload, "secret", algorithm="HS256")
        targetURl = "https://migrationtoolbackend.cfapps.eu20.hana.ondemand.com/token?token=" + encoded_jwt
        payload={}
        headers = {
        'apiToken': '123'
        }
        response = requests.request("GET", targetURl, headers=headers, data=payload)
        
        bearer_token = response.text

        headers= { 'Authorization': 'Bearer ' + bearer_token, 'Content-Type': 'application/json'}

        st.success("Token was generated")
        st.write({"token": bearer_token})
    else:
        st.error("No Token was generated")


