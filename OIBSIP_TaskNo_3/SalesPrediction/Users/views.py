from django.shortcuts import render

def index(request):
    if request.method == "POST":
       
        weight = float(request.POST['Item_Weight'])  
        fat = request.POST['Item_Fat_Content']
        visibility = float(request.POST['Item_Visibility'])
        itemType = request.POST['Item_Type']
        mrp = float(request.POST['Item_MRP'])
        outletSize = request.POST['Outlet_Size']

      
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LinearRegression
        
        df = pd.read_csv(r"static/datasets/salesPrediction.csv")
        df.dropna(inplace=True)

        from sklearn.preprocessing import LabelEncoder
        l = LabelEncoder()

        
        fat1 = l.fit(df["Item_Fat_Content"]).transform([fat])[0]
        df["Fat_Content"] = l.transform(df["Item_Fat_Content"])
        itemType1 = l.fit(df["Item_Type"]).transform([itemType])[0]
        df["item_type"] = l.transform(df["Item_Type"])
        outletSize1 = l.fit(df["Outlet_Size"]).transform([outletSize])[0]
        df["outlet_size"] = l.transform(df["Outlet_Size"])

        
        X = df.drop(["Item_Identifier", "Item_Fat_Content", "Item_Type", "Outlet_Identifier", 
                     "Outlet_Establishment_Year", "Outlet_Size", "Outlet_Location_Type", 
                     "Outlet_Type", "Item_Outlet_Sales"], axis=1)
        y = df["Item_Outlet_Sales"]

       
        
        model = LinearRegression()
        model.fit(X, y)

      
        
        pred_input = np.array([[weight, fat1, visibility, itemType1, mrp, outletSize1]])
        pred_outcome = model.predict(pred_input)
        
        
        return render(request, "predict.html", {
            "Item_Weight": weight,
            "Item_Fat_Content": fat,
            "Item_Visibility": visibility,
            "Item_Type": itemType,
            "Item_MRP": mrp,
            "Outlet_Size": outletSize,
            "prediction": pred_outcome[0]  
        })

    return render(request, "index.html")

def predict(request):
    return render(request,"predict.html")