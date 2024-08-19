from django.shortcuts import render

def index(request):
    if request.method == "POST":
        sel = request.POST['sepl']
        sew = request.POST['sepw']
        pel = request.POST['petl']
        pew = request.POST['petw']
        
        # Convert input values to float
        try:
            sel = float(sel)
            sew = float(sew)
            pel = float(pel)
            pew = float(pew)
        except ValueError:
            return render(request, "index.html", {
                "error": "Please enter valid numeric values for all fields."
            })
        
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LogisticRegression
        
        df = pd.read_csv(r"static/dataset/Iris.csv")


        #preprossing
        print(df.head())
        print(df.isnull().sum())
        df.dropna(inplace=True)

        x = df.drop(["Id", "Species"], axis=1)
        y = df["Species"]


        #train model
        model = LogisticRegression()
        model.fit(x, y)

        pred_input = np.array([[sel, sew, pel, pew]])

        pred_outcome = model.predict(pred_input)
        prediction = pred_outcome[0]

        return render(request, "find.html", {
            "SepalLength": sel,
            "SepalWidth": sew,
            "PetalLength": pel,
            "PetalWidth": pew,
            "Species": prediction
        })
    else:
        return render(request, "index.html")
def find(request):
    return render(request, "find.html")
